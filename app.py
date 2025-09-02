
# ======================================================
#  API Endpoint Usage Checker
#  Main app
#  Copyright (c) 2025 Usama Bakry (ubakry@solvytix.com)
#  Licensed under the MIT License
# ======================================================

import os
import re
import csv
import json
import yaml
import pandas as pd
import streamlit as st

# ---------------- Utility Functions ----------------

def load_endpoints(endpoint_file):
    """Load endpoints from OpenAPI (JSON/YAML) or plain text"""
    filename = endpoint_file.name

    # Case 1: JSON OpenAPI spec
    if filename.endswith(".json"):
        spec = json.load(endpoint_file)
        endpoints = []
        for path, methods in spec.get("paths", {}).items():
            for method in methods.keys():
                endpoints.append((path, method.upper()))
        return endpoints

    # Case 2: YAML OpenAPI spec
    elif filename.endswith((".yaml", ".yml")):
        spec = yaml.safe_load(endpoint_file)
        endpoints = []
        for path, methods in spec.get("paths", {}).items():
            for method in methods.keys():
                endpoints.append((path, method.upper()))
        return endpoints

    # Case 3: Plain text file (no methods)
    else:
        content = endpoint_file.read().decode("utf-8")
        return [(line.strip(), "") for line in content.splitlines() if line.strip()]


def endpoint_to_regex(endpoint: str):
    """Convert REST-style endpoint with {param} or :param to regex"""
    # Escape everything first
    pattern = re.escape(endpoint)

    # Replace :param → match one path segment
    pattern = re.sub(r"\\:([a-zA-Z_][a-zA-Z0-9_]*)", r"[^/]+", pattern)

    # Replace {param} → match one path segment
    pattern = re.sub(r"\\{[a-zA-Z_][a-zA-Z0-9_]*\\}", r"[^/]+", pattern)

    # Allow optional trailing slash + query params
    pattern = pattern.rstrip("/") + r"/?(\\?.*)?$"

    return re.compile(pattern, re.IGNORECASE)


def find_endpoints_in_code(project_dir, endpoints):
    """Search project files for endpoint usage"""
    used = {}
    project_name = os.path.basename(os.path.abspath(project_dir))

    endpoint_patterns = [((ep, method), endpoint_to_regex(ep)) for ep, method in endpoints]

    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith((".js", ".jsx", ".ts", ".tsx", ".vue", ".dart")):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        for i, line in enumerate(f, start=1):
                            for (ep, method), pattern in endpoint_patterns:
                                if pattern.search(line):
                                    if (ep, method) not in used:
                                        used[(ep, method)] = []
                                    used[(ep, method)].append((file_path, i, project_name))
                except Exception as e:
                    st.warning(f"⚠️ Could not read {file_path}: {e}")
    return used


def export_to_csv(endpoints, used):
    """Write report to CSV"""
    rows = []
    for ep, method in endpoints:
        if (ep, method) in used:
            locations = "; ".join([f"{fp}:{ln}" for fp, ln, _ in used[(ep, method)]])
            projects = ", ".join(sorted(set(p for _, _, p in used[(ep, method)])))
            rows.append([ep, method, "used", locations, projects])
        else:
            rows.append([ep, method, "unused", "", ""])
    csv_file = "endpoint_usage.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Endpoint", "Method", "Status", "Files", "Projects"])
        writer.writerows(rows)
    return csv_file, rows


# ---------------- Streamlit UI ----------------

st.set_page_config(page_title="API Endpoint Usage Checker", layout="wide")
st.title("API Endpoint Usage Checker")

st.markdown(
    "Upload an **OpenAPI spec (JSON/YAML)** or a simple `endpoints.txt` file, "
    "then enter one or more project directories (React, Next.js, Flutter). "
    "We will show which endpoints are **used**, with HTTP method, file locations, "
    "and which project(s) use them."
)

endpoint_file = st.file_uploader("📂 Upload API spec (JSON/YAML) or endpoints.txt",
                                 type=["json", "yaml", "yml", "txt"])
project_dirs_input = st.text_area("📁 Enter project directories (one per line)")

if endpoint_file and project_dirs_input:
    # Load endpoints
    endpoints = load_endpoints(endpoint_file)
    st.success(f"Loaded {len(endpoints)} endpoints.")

    # Process multiple projects
    project_dirs = [d.strip() for d in project_dirs_input.splitlines() if d.strip()]
    used_map = {}
    for pdir in project_dirs:
        partial_used = find_endpoints_in_code(pdir, endpoints)
        for key, val in partial_used.items():
            if key not in used_map:
                used_map[key] = []
            used_map[key].extend(val)

    # Prepare DataFrame
    rows = []
    for ep, method in endpoints:
        if (ep, method) in used_map:
            locations = "; ".join([f"{fp}:{ln}" for fp, ln, _ in used_map[(ep, method)]])
            projects = ", ".join(sorted(set(p for _, _, p in used_map[(ep, method)])))
            rows.append([ep, method, "used", locations, projects])
        else:
            rows.append([ep, method, "unused", "", ""])
    df = pd.DataFrame(rows, columns=["Endpoint", "Method", "Status", "Files", "Projects"])

    # Counts
    all_count = len(df)
    used_count = (df["Status"] == "used").sum()
    unused_count = (df["Status"] == "unused").sum()

    # Filters with counts in labels
    status_filter = st.radio(
        "Filter by Status:",
        [
            f"All ({all_count})",
            f"Used ({used_count})",
            f"Unused ({unused_count})"
        ],
        horizontal=True
    )
    if status_filter.startswith("Used"):
        df = df[df["Status"] == "used"]
    elif status_filter.startswith("Unused"):
        df = df[df["Status"] == "unused"]

    # Search box
    search = st.text_input("🔎 Search endpoint")
    if search:
        df = df[df["Endpoint"].str.contains(search, case=False)]

    # Display table
    st.dataframe(df, use_container_width=True)

    # Export CSV
    csv_file, rows = export_to_csv(endpoints, used_map)
    with open(csv_file, "rb") as f:
        st.download_button("📄 Download Full CSV", f,
                           file_name="endpoint_usage.csv", mime="text/csv")
