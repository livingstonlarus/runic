# Codex - AI-Powered Context & Memory Toolset

Codex is a powerful toolset designed to enhance AI-assisted development by providing intelligent documentation management and persistent project memory capabilities. It helps AI coding assistants better understand your project context by automatically fetching, processing, and organizing documentation from various sources, while maintaining a structured memory of project-specific preferences and decisions.

It's inspired by [Cursor Docs Symbol](https://docs.cursor.com/context/@-symbols/@-docs) and by [Cline Memory Bank](https://github.com/nickbaumann98/cline_docs/blob/main/prompting/custom%20instructions%20library/cline-memory-bank.md).

## Key Features
- 📚 **Smart Documentation Fetching**: Automatically crawls and processes documentation from a base URL (multithreaded)
- 🧠 **Persistent Project Memory**: Stores and manages project-specific context and preferences
- 🤖 **AI-Assistant Integration**: Seamlessly works with your favorite AI coding assistants

## Usage
1. Initialize Codex in your project:
```sh
codex init
```
This will create a `.codex` directory in your project with all necessary configuration files.

2. Set up your AI coding assistant:
   - Open your preferred AI coding assistant (Cursor, Cody, or any other assistant with file editing capabilities)
   - Start a new chat session
   - First prompt your assistant with:
     ```
     Follow your instructions in .codex/instruct.md
     ```
   Your AI assistant will now be configured with Codex's enhanced context and memory capabilities.

## 🤝 Contributing
### Using Docker
You can develop using Docker to ensure a consistent environment:

```sh
# Clone the repository
git clone https://github.com/livingstonlarus/codex.git
cd codex

# Build the Docker image
docker build -t codex .

# Run the container with the current directory mounted
docker run -it -v .:/app codex shell

# Install Codex from inside the container
pip install -e .

# Test the Codex initialization
codex init
```

This will give you a shell inside the container with the local project files mounted at `/app`. Any changes you make locally will be reflected inside the container, and vice-versa.

To contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📜 License
**Codex** is open-source under the **MIT License**.
