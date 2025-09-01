# 🧩 API Endpoint Usage Checker

A developer tool to **analyze API endpoint usage across multiple projects** (React, Next.js, Flutter, etc.) by scanning your source code against an **OpenAPI spec (JSON/YAML)** or a simple `endpoints.txt` file.  

This helps teams quickly identify which endpoints are **used**, which are **unused**, and where they appear in the codebase.  

---

## ✨ Features

- 📂 **Multi-project support** – scan multiple frontend/mobile projects at once.  
- 📑 **OpenAPI & text file input** – load endpoints from `.json`, `.yaml`, `.yml`, or plain `endpoints.txt`.  
- 🔍 **Smart matching** – supports `{param}` and `:param` placeholders (wildcard matching).  
- 📊 **Interactive dashboard** – filter by Used/Unused, search endpoints, view counts.  
- 📄 **Detailed report** – shows file + line number + project where an endpoint is used.  
- 📥 **Export to CSV** – download a complete endpoint usage report.  

---

## 🛠️ Requirements

- Python **3.12+**
- See [`requirements.txt`](requirements.txt)

---

## 🚀 Installation

Clone the repo:

```bash
git clone https://github.com/YOUR_USERNAME/api-endpoint-usage-checker.git
cd api-endpoint-usage-checker
```
---
## ▶️ Usage

Run the tool with:

```bash
python start.py
```
This will:  
1. Create and activate a virtual environment (if missing).  
2. Install dependencies from `requirements.txt`.  
3. Launch the app in your browser (default: [http://localhost:8501](http://localhost:8501)).  

---

## 📜 License & Copyright

[MIT License](LICENSE)  

© 2025 Usama Bakry (ubakry@solvytix.com). All rights reserved.