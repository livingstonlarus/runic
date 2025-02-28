# ᛤ Runic

Runic is a lightweight framework for parallel development with multiple AI agents. It provides structured memory management, specialized agent roles, and workflow guidance to maximize development velocity. Inspired by frameworks like Cline Memory Bank, Runic enhances Large Language Models (LLMs) with Long-Term Memory (LTM) capabilities and structured knowledge retention.

## Key Features

- 🧠 **Persistent Project Memory**: Stores and manages project-specific context across sessions
- 👥 **Parallel Multi-Agent Development**: Run multiple agents simultaneously on different tracks
- 🔄 **Workflow Guidance**: Natural division of planning and implementation through specialized roles
- 📚 **Documentation Integration**: Optional integration with documentation fetching tools
- 🔍 **Token Efficiency**: Minimizes framework overhead to maximize available context

## Installation

```bash
# Install from PyPI
pip install runic

# Or install from source
git clone https://github.com/livingstonlarus/runic.git
cd runic
pip install -e .
```

## Core Concept: Parallel Development

Runic enables true parallel development by running multiple agents simultaneously:

- **Orchestrator**: Manages overall project coordination and architecture (planning focus)
- **Specialists**: Focus on specific domains with deep expertise (implementation focus)

This approach delivers enterprise-grade development at startup speed by simulating a well-coordinated engineering team. The natural division between Orchestrator (planning) and Specialists (implementation) creates an efficient workflow without requiring explicit mode switching.

## Understanding Runic in the AI Coding Ecosystem

Runic operates within a layered ecosystem of AI coding tools:

### Layer 1: AI Models
- **Claude Sonnet 3.7** (Anthropic)
- **o3-mini** (OpenAI)
- Other large language models

### Layer 2: Agentic Coding Interfaces
- **Claude Code** (Anthropic's agentic coding interface)
- **Roo Code** / **Cline** (VS Code / VSCodium extensions with agentic capabilities)
- **Cursor** / **Windsurf** etc. (IDEs with built-in AI capabilities)
- **GitHub Copilot** (Microsoft/OpenAI's coding assistant in VS Code)

### Layer 3: Development Frameworks
- **Runic** (framework for parallel development with multiple agents)

Runic is not an alternative to agentic coding interfaces like GitHub Copilot or Cursor. Instead, it's a complementary framework that sits on top of these interfaces, providing structure for organizing development work across multiple tracks and maintaining context across sessions.

You can use Runic with any agentic coding interface you prefer, allowing you to leverage the strengths of different AI models and interfaces while maintaining a consistent development framework.

## Directory Structure

```
.runic/
├── orchestrator.md         # Entry point for Orchestrator Agent
├── specialist.md           # Entry point for Track Specialists
├── core/
│   ├── identity.md         # Shared identity (74 tokens)
│   ├── commands.md         # Shared commands (90 tokens)
│   ├── memory-structure.md # Memory hierarchy (142 tokens)
│   ├── rules.md            # Project rules (100 tokens)
│   └── memory-updates.md   # Memory update process (174 tokens)
└── memory/
    ├── tracks/
    │   └── track-management.md # Track workflows (213 tokens)
    ├── active-context.md
    ├── product-context.md
    ├── progress.md
    ├── project-brief.md
    ├── system-patterns.md
    └── tech-context.md
```

## Token Usage

### Framework Overhead
- **Shared files**: ~406 tokens
- **Orchestrator total**: ~619 tokens
- **Specialist total**: ~599 tokens

### Memory Files
- **Project memory**: Variable size, grows with project complexity
- **Track-specific memory**: Variable size, focused on domain context

This token-efficient design minimizes framework overhead (~600 tokens) while maximizing available context for project memory files and actual development work. Agents can focus their token budget on understanding the project rather than processing framework instructions.

In real world usage, initializing the Orchestrator with a massive 10 tracks project resulted in API cost of ~$0.50. Including overhead of Cline in Plan mode with full Auto-approve and using model Claude 3.7 Sonnet Thinking (OpenRouter), with rates as of 2025-02-27. Resulting in tokens consumption ⬆ 140K ⬇ 2.5K and context window 25K.

Using Gemini 2.0 Flash Thinking Experimental 01-21 would be free but quota is exhausted too fast (rate limits of 10 RPM (1500 req/day)).

## Token Optimization Techniques

Runic agents employ several token optimization strategies when creating and maintaining memory files:

### Structural Optimization
- **Hierarchical organization**: Information flows from general to specific
- **Bullet points over paragraphs**: More token-efficient and easier to scan
- **Numbered lists for sequences**: Clear ordering with minimal tokens
- **Headings as context separators**: Reduce need for transitional phrases

### Language Optimization
- **Imperative style**: "Do X" instead of "You should do X"
- **Eliminate redundant words**: "Use X" vs "Make use of X"
- **Contractions**: Use "don't", "can't", "it's" when appropriate
- **Abbreviations**: Use common abbreviations (e.g., API, UI, DB) consistently
- **Avoid hedging phrases**: Skip "I think", "perhaps", "it seems that"

### Content Optimization
- **Prune historical context**: Summarize past work instead of detailing it
- **Focus on current state**: Emphasize what is, not what was
- **Consolidate similar information**: Avoid repeating the same concept
- **Use examples sparingly**: Include only when necessary for clarity

These techniques are applied throughout Runic's framework files and by agents when maintaining memory files. Even the initial project brief will be optimized by the Orchestrator after discussing requirements with the user.

## Getting Started

### Quick Start

1. **Initialize Runic in your project**:
   ```bash
   runic init
   ```
   This creates the `.runic` directory structure with all necessary template files.

2. **Initialize your first track**:
   ```bash
   runic track init <track-name>
   ```
   This creates a new track with the appropriate structure.

3. **Start using Runic with your AI assistant**:
   - For the Orchestrator: Use the prompt in the "Initial Prompts" section below
   - For Track Specialists: Use the track-specific prompt

## Commands

### Distinction Between `runic` CLI Commands and `$` Chat Commands

- **`runic` CLI Commands**: These are commands that users or agents can run directly in the terminal. They are used to manage the Runic framework, tracks, memory, and integrations.
- **`$` Chat Commands**: These are commands that users give to the agents within the chat interface. They instruct the agents to perform specific tasks related to the project, such as managing Git branches.

## CLI Commands

Runic provides a command-line interface for both users and agents:

### Core Commands

- `runic init`: Initialize Runic in the current project
- `runic --version`: Display the current version of Runic

### Memory Management

- `runic mem update`: Update all memory files with timestamps
- `runic mem update --track=<name>`: Update memory files for a specific track
- `runic mem next`: Analyze memory files and suggest next steps

### Track Management

- `runic track init <name>`: Create a new track with the given name
- `runic track list`: List all available tracks
- `runic track status`: Show the status of all tracks

### Integration Points (for extending functionality)

- `runic integrate docs <url> [--tool=<tool>]`: Integration point for documentation fetching
- `runic integrate vector-db [--tool=<tool>] [--action=<action>] [--query=<query>]`: Integration point for vector database tools
- `runic integrate llm --tool=<tool> --action=<action>`: Integration point for LLM framework tools

## Chat Commands

Runic provides a set of chat commands that users can give to the agents within the chat interface. These commands help manage Git branches, tracks, and memory within the project.

### Git Branch Commands

- **Create a new Git branch**:
  - Command: `$branch create <name>`
  - Description: Creates a new Git branch with the specified name. Specialists should use track-prefixed names.
  - Usage: For Orchestrator and Specialists

- **Delete a Git branch**:
  - Command: `$branch delete <name>`
  - Description: Deletes the specified Git branch. Specialists can only delete branches for their track.
  - Usage: For Orchestrator and Specialists

- **Merge a Git branch**:
  - Command: `$branch merge <name>`
  - Description: Merges the specified Git branch into the main branch.
  - Usage: For Orchestrator only

- **List all Git branches**:
  - Command: `$branch list`
  - Description: Lists all Git branches in the repository. Shows different views for Orchestrator vs Specialists.
  - Usage: For Orchestrator and Specialists

- **Update a Git branch**:
  - Command: `$branch update`
  - Description: Updates the current branch with latest changes from the main branch.
  - Usage: For Specialists

- **Mark a branch as ready for merge**:
  - Command: `$branch ready <name>`
  - Description: Signals that a branch is ready to be merged into main.
  - Usage: For Specialists

### Track Commands

- **Initialize a new track**:
  - Command: `$track init <name>`
  - Description: Initializes a new track with the given name and creates an initial Git branch for it.
  - Usage: For Orchestrator only

- **List all tracks**:
  - Command: `$track list`
  - Description: Lists all available tracks.
  - Usage: For Orchestrator and Specialists

- **Show the status of all tracks**:
  - Command: `$track status`
  - Description: Shows the status of all tracks.
  - Usage: For Orchestrator and Specialists

### Memory Commands

- **Update all memory files**:
  - Command: `$mem update`
  - Description: Updates all memory files with timestamps.
  - Usage: For Orchestrator and Specialists

- **Update memory files for a specific track**:
  - Command: `$mem update track=<name>`
  - Description: Updates memory files for a specific track.
  - Usage: For Orchestrator (any track) and Specialists (their track only)

- **Determine and execute next steps based on memory analysis**:
  - Command: `$mem next`
  - Description: Analyzes memory files and suggests next steps.
  - Usage: For Orchestrator and Specialists

## Using Runic

### Initial Prompts

#### For the Orchestrator:

```
Please read and follow the instructions in .runic/orchestrator.md.
You are the Orchestrator Agent responsible for overall project management and cross-track coordination.
```

#### For Track Specialists:

```
Please read and follow the instructions in .runic/specialist.md.
You are the specialist for the '<track-name>' track. Focus exclusively on this domain.
```

### Example Usage

Here's an excerpt of a conversation with an Orchestrator Agent enhanced with Runic:

>**User**
>Please read and follow the instructions in .runic/orchestrator.md.

>**AI Assistant**
>I'll help you manage this project using the Runic framework. I notice that the .runic directory is already initialized. Let me check the memory files to understand the current state of the project.
>
>I've reviewed the memory files and found:
>- The project is a web application using React and Node.js
>- There are two active tracks: "frontend" and "api"
>- The frontend track is focused on implementing the user interface
>- The api track is working on REST endpoints
>
>I'll coordinate between these tracks and help manage the overall architecture. What would you like to focus on today?

>**User**
>$track init database

>**AI Assistant**
>I'll create a new track for database development.
>
>Creating track "database"...
>Track "database" created successfully!
>
>I've initialized a new "database" track with the following structure:
>- Created .runic/memory/tracks/database/active-context.md
>- Created .runic/memory/tracks/database/progress.md
>
>This track will focus on database schema design, migrations, and data access layers. Would you like me to define the initial tasks for this track?

### Handling Simpler Projects

For projects that don't warrant multiple tracks, you can use a streamlined approach:

1. **Use only the Orchestrator Agent**: Initialize a single agent using the Orchestrator prompt
2. **Skip track creation**: No need to create specialized tracks
3. **Simplified memory structure**: Use only the main memory files without track subdirectories

This approach maintains the structured memory benefits of Runic while simplifying the workflow for less complex projects.

## Implementation Approach

### True Parallel Development

![more](https://media1.tenor.com/m/6QCq9E-0LiwAAAAd/star.gif)

For maximum development velocity:

1. **Clone Repository Multiple Times**:
   ```bash
   # Clone the main repository
   git clone https://github.com/user/project.git project-main

   # Clone for each track
   git clone https://github.com/user/project.git project-track1
   git clone https://github.com/user/project.git project-track2
   ```

2. **Set Up Shared Memory**:
   ```bash
   # Create a shared memory directory (e.g., in a cloud drive)
   mkdir -p /path/to/shared/memory

   # Symlink the memory directory in each clone
   ln -s /path/to/shared/memory project-main/.runic/memory
   ln -s /path/to/shared/memory project-track1/.runic/memory
   ln -s /path/to/shared/memory project-track2/.runic/memory
   ```

3. **Open Separate IDE Windows**:
   - Launch a new IDE window for each repository clone
   - Each window will have its own AI assistant session

4. **Initialize Each Agent**:
   - Use the Orchestrator prompt in the main repository
   - Use the Specialist prompt in each track repository

## Benefits

1. **Enterprise-Grade Development at Startup Speed**: The parallel multi-agent approach delivers the output quality and velocity of a large engineering team while maintaining the agility of a lean operation.

2. **Specialized Expertise Without Specialized Headcount**: Each agent can focus deeply on its specific domain, providing specialized expertise across multiple technical areas simultaneously.

3. **Seamless Integration Across Domains**: The shared memory bank and coordination mechanisms ensure that work across different tracks integrates smoothly, preventing the fragmentation that often occurs in parallel development.

4. **Scalable Development Process**: As project complexity grows, simply add more specialized agents to handle new tracks without disrupting existing workflows.

5. **Resource Optimization**: Maximize the value of AI assistants by having them work in parallel rather than sequentially, dramatically increasing development throughput.

## Economic Benefits of Parallel Development

The parallel development approach with multiple agents offers significant economic advantages:

### Cost-Efficiency

1. **Multiplied AI Productivity**: Extract maximum value from AI assistant subscriptions by running multiple instances in parallel
2. **Reduced Development Time**: Complete projects in a fraction of the time required for sequential development
3. **Specialized Expertise On-Demand**: Access domain-specific expertise across multiple areas without hiring specialists

### Resource Optimization

1. **Efficient Resource Allocation**: Assign agents to tracks based on their specialized capabilities
2. **Reduced Context Switching**: Each agent maintains focus on its domain, eliminating productivity loss from switching contexts
3. **Parallel Problem Solving**: Address multiple challenges simultaneously rather than sequentially

### Business Impact

1. **Faster Time-to-Market**: Accelerate product development cycles by working on multiple components simultaneously
2. **Competitive Advantage**: Deliver more comprehensive solutions in less time than competitors
3. **Scalable Development**: Scale development capacity by adding more agents as needed

### ROI Calculation

For a typical project with 5 development tracks:

| Approach | Development Time | Relative Cost | Features Delivered |
|----------|------------------|---------------|-------------------|
| Sequential (1 agent) | 5x | 1x | 1x |
| Parallel (5 agents) | 1x | 1.5x | 5x |

The parallel approach delivers approximately 3.3x more value per dollar invested in development resources, while dramatically reducing time-to-market.

## Troubleshooting

### Common Issues

1. **Context Loss**: If the AI seems to have lost context, use `$mem update` to refresh memory
2. **Track Confusion**: If tracks are getting mixed up, use `$track <name>` to focus
3. **Workflow Issues**: If development feels disorganized, review the Orchestrator's planning guidance

### Memory Optimization

1. **Token Efficiency**: Keep memory files concise and focused
2. **Hierarchical Structure**: Use the hierarchy to avoid duplication
3. **Regular Cleanup**: Archive completed tracks to reduce context size

## Future Development

Runic is continuously evolving. Here are some areas we're exploring for future releases:

### Context Window Management
- Improving techniques to keep Runic instructions and rules in context window
- Enhancing documentation retrieval and relevance
- Exploring vector embeddings for more efficient memory retrieval
- Evaluating integration with tools like LangChain, LlamaIndex, or ChromaDB

### Documentation Enhancement
- Implementing smarter documentation crawling and processing
- Adding support for various documentation formats and structures
- Generating navigation aids for documentation
- Automatically fetching documentation for project dependencies

### Additional Integrations
- Expanding LLM capabilities with more integration layers
- Adding support for codebase indexing and semantic search
- Implementing web search capabilities

## Contributing

To contribute to Runic:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

We welcome contributions of all kinds, including bug reports, feature requests, documentation improvements, and code changes.

### TODO

#### Optimization
- Rewrite all core files following Token Optimization Techniques
- Measure token counts before/after optimization
- Further reduce framework overhead if possible
- Recount token counts for README in Token Usage > Framework Overhead

#### CLI Commands
- ✅ `runic init`: Initialize Runic structure in a project
- ✅ `runic track init <name>`: Create a new track
- ✅ `runic track list`: List all tracks
- ✅ `runic track status`: Show status of all tracks
- ✅ `runic mem update`: Update memory files
- ✅ `runic mem update --track=<name>`: Update track-specific memory files
- ✅ `runic mem next`: Determine and execute next steps based on memory analysis
- `runic integrate docs <url>`: Integration point for documentation fetching (pending implementation)
- `runic integrate vector-db`: Integration point for vector database tools (pending implementation)
- `runic integrate llm`: Integration point for LLM framework tools (pending implementation)

#### Chat Commands
- ✅ `$track init <name>`: Initialize a new track and create its first branch
- ✅ `$track list`: List all available tracks
- ✅ `$track status`: Show the status of all tracks
- ✅ `$mem update`: Update all memory files with timestamps
- ✅ `$mem update track=<name>`: Update memory files for a specific track
- ✅ `$mem next`: Analyze memory files and suggest next steps
- ✅ `$branch create <name>`: Create a new Git branch
- ✅ `$branch delete <name>`: Delete a Git branch
- ✅ `$branch merge <name>`: Merge a Git branch into main
- ✅ `$branch list`: List all Git branches
- ✅ `$branch update`: Update feature branch with latest changes from main
- ✅ `$branch ready <name>`: Signal that a branch is ready to be merged

## Conclusion

Runic represents a paradigm shift in how development projects can be structured and executed. By implementing this framework, you can achieve the comprehensive capabilities typically associated with much larger engineering teams while maintaining the agility of a lean operation.

The true innovation of Runic lies in its ability to simulate the dynamics of a well-coordinated engineering organization through parallel agents—delivering enterprise-quality results with startup efficiency.

## License

Runic is open-source software licensed under the MIT License.

## Attribution

The Runic project would be very honored and grateful if you attribute your project with:

```
<strong>Made by 🤖 with ᛤ <a href="https://pypi.org/project/runic/">Runic</a></strong>
```

Which should render as:

**Made by 🤖 with ᛤ [Runic](https://pypi.org/project/runic/)**

## Acknowledgments

Runic was significantly influenced by the [Cline Memory Bank](https://github.com/cline/cline/blob/2e9e633cdcaa73b8985fa0cbace107352a484cd9/docs/prompting/custom%20instructions%20library/cline-memory-bank.md) approach. We'd like to thank the authors and contributors of that project:

- **Author**: [nickbaumann98](https://github.com/nickbaumann98)
- **Contributors**:
  - [SniperMunyShotz](https://github.com/SniperMunyShotz)
  - [saoudrizwan](https://github.com/saoudrizwan)

Their pioneering work on structured memory systems for AI assistants provided valuable insights for Runic's development.
