# Codex - AI-Powered Context & Memory Toolset

## 🚀 Overview
**Codex** is an **IDE-agnostic AI toolset** that enhances coding assistants by providing **dynamic documentation ingestion** and **long-term memory management**. It allows AI coding assistants to fetch up-to-date docs, retain project memory, and work more efficiently across different IDEs.

## ✨ Features
- **📖 Dynamic Documentation Ingestion** – Uses **Crawl4AI** to fetch and format documentation for AI.
- **🧠 AI Long-Term Memory** – Manages AI assistant memory with **Mem0**, enabling persistent knowledge.
- **🔄 Local & Offline** – Runs fully on your local machine, no API keys or cloud dependencies required.
- **📂 Per-Project Context** – Initializes a `.codex/` folder in each project to store configurations, memory, and docs.
- **🛠️ CLI for AI Assistants** – Provides an interface for LLM-powered assistants to fetch relevant data on demand.

## 📥 Installation
```sh
# Clone the repo
git clone git@github.com:livingstonlarus/codex.git
cd codex

# Set up virtual environment (optional, recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Codex as a CLI tool
pip install .
```

## 🔧 Usage
### Initialize Codex in a project
```sh
cd my_project
codex init
```
This creates a `.codex/` folder containing:
```
.codex/
│── spec.md          # AI-generated project specification (User-defined)
│── spec.example.md  # AI Architect prompt template (Reference only)
│── memory.json      # AI assistant’s dynamic memory (Managed by Codex)
│── config.yaml      # Codex configuration (optional)
```

> **Note:** You may want to add `.codex/memory.json`, `.codex/docs.md`, or `.codex/config.yaml` to your project's `.gitignore`, as these files contain dynamically updated data or local configuration settings.

### Fetch documentation from a website
```sh
codex fetch-docs https://example.com/docs
```
This scrapes the website and stores structured docs in `.codex/docs.md`.

### Store project memory
```sh
codex add-memory "User prefers TypeScript over JavaScript."
```
This persists project-specific AI memory to `memory.json`.

## 🛠 Development
```sh
git clone git@github.com:livingstonlarus/codex.git
cd codex
git remote add origin git@github.com:livingstonlarus/codex.git

# Install dependencies
pip install -r requirements.txt
```

To contribute, submit a pull request!

## 📜 License
**Codex** is open-source under the **MIT License**.
