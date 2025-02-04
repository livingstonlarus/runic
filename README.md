# Runic - LLM Memory & Documentation Enhancement Framework

Runic is an open-source framework that enhances Large Language Models (LLMs) with Long-Term Memory (LTM) and Retrieval-Augmented Generation (RAG) layers. By implementing these capabilities as distinct, interoperable layers, Runic enables LLMs to retain context, adapt over time, and access up-to-date information. While it particularly shines in enhancing AI coding assistants with intelligent documentation management and persistent project memory, its versatile architecture makes it suitable for any AI application requiring structured knowledge retention and contextual awareness - from content generation to decision support systems.

It's inspired by [Cursor Docs Symbol](https://docs.cursor.com/context/@-symbols/@-docs) and by [Cline Memory Bank](https://github.com/nickbaumann98/cline_docs/blob/main/prompting/custom%20instructions%20library/cline-memory-bank.md).

## Key Features
- 📚 **Smart Documentation Fetching**: Automatically crawls and processes documentation from a base URL (multithreaded)
- 🧠 **Persistent Project Memory**: Stores and manages project-specific context and preferences
- 🤖 **AI-Assistant Integration**: Seamlessly works with your favorite AI coding assistants

## Usage
1. Install Runic:
```sh
# Install latest pre-release version (required for beta releases until RC)
pip install --pre runic
```

2. Initialize Runic in your project:
```sh
runic init
```
This will create a `.runic` directory in your project with all necessary files and folders.

3. Initialize your AI chat or AI coding assistant:
   - Start a new chat session
   - First prompt the LLM with:
     ```
     Follow your instructions in .runic/instruct.md
     ```
   Your AI assistant will now be augmented with Runic's enhanced context and memory capabilities.

## 🤝 Contributing
To contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### TODO List
While Runic started as an AI coding assistant enhancer, it's evolving into a general-purpose framework. Our next steps:

#### Context Adaptability
- [ ] Create templates for various use cases beyond coding
- [ ] Implement context-based template selection
- [ ] Add custom template management support

#### Documentation Crawler Enhancement
- [ ] Implement max depth setting to prevent infinite crawling
- [ ] Enhance main content detection and filtering
- [ ] Add support for various documentation formats and structures
- [ ] Implement rate limiting and politeness delays

#### More Layers
- [ ] Evaluate porting our RAG layer to Crawl4AI
- [ ] Evaluate porting our LTM layer to Mem0
- [ ] Expand LLM capabilities with more layers

## 📜 License
**Runic** is open-source under the **MIT License**.
