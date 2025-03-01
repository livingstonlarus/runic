# Runic Improvements

This document outlines proposed improvements to the Runic framework based on user feedback and evolving requirements.

## 1. Configuration-Based Optional Integrations

### Current Situation
- Agents may need up to date technical documentation for the library it uses
- Agents currently store memories in flat markdown files
- Git platform tools are hardcoded without user preference consideration

### Proposed Solution: `.runic/config.yaml`

Implement a configuration file at `.runic/config.yaml` to make integrations optional and configurable:

```yaml
# Example .runic/config.yaml
integrations:
  # Vector database for memory management
  pinecone:
    enabled: true
    api_key: ${PINECONE_API_KEY}  # Use environment variable
    environment: "us-west1-gcp"
    index_name: "runic-memory"
  
  # Documentation fetching
  firecrawl:
    enabled: false  # Disabled by default
  
  # Git platform preference
  git:
    platform_cli: "gh"  # Options: "gh" (GitHub), "glab" (GitLab), etc.
    
  # Messaging between agents
  upstash:
    qstash:
      enabled: false
      api_key: ${UPSTASH_QSTASH_API_KEY}
    redis:
      enabled: false
      url: ${UPSTASH_REDIS_URL}
      token: ${UPSTASH_REDIS_TOKEN}
```

!! Would it make sense to enable Qstash or Redis only and not both? Maybe juste enable Upstash, and then individual API keys for Qstash and Redis (if not a unique key for all Upstash service).

### Implementation Details

1. **Configuration Loading**:
   - Create a `config.py` module to load and validate the configuration
   - Support environment variable expansion
   - Provide sensible defaults

2. **Integration Detection**:
   - Check for the presence of optional dependencies
   - Warn when an integration is enabled but dependencies are missing
   - Suggest installation commands for missing dependencies

## 2. Natural Language Commands vs. Structured Commands

### Current Situation
- Chat commands use a specific syntax (e.g., `$mem update`, `$branch create`)
- Users need to memorize specific command formats
- CLI commands have a structured format (e.g., `runic track init`)
- Need to maintain CLI code

### Proposed Solution: Leverage LLM Understanding

1. **Natural Language Chat Commands**:
   - Allow agents to understand natural language requests
   - Examples:
     - "Update your memory" instead of `$mem update`
     - "Create a branch for the login feature" instead of `$branch create login-feature`
     - "Mark the auth branch as ready for merge" instead of `$branch ready auth`

2. **Implementation Approach**:
   - Remove command handlers entierly
   - Define chat commands as natural language examples, that the LLM should recognize and associate to a set of commands to execute. Ie:
     - User: I think it's time to wrap up this branch
     - Agent: You're right, let's submit a PR
       command: `gh pr create`
     - In .runic/core/commands.md we may have:
       If user states the branch is complete or that it's time to submit a PR, you'll execute `<git:platform_cli> pr create`, where `<git:platform_cli>` is the Git platform CLI tool set in `.runic/config.yaml`


3. **CLI Command Execution**:
   - Allow agents to directly execute git commands and other CLI operations
   - Trust the LLM's ability to generate correct commands based on context
   - Example: Instead of wrapping `git branch -b feature`, let the agent execute it directly

## 3. Agent Communication and Coordination

### Current Situation
- Agents share memory through files in `.runic/memory/`
- No real-time communication between agents

### Proposed Solution: Enhanced Communication Stack

1. **Pinecone for Knowledge Management**:
   - Store internal documentation and project knowledge
   - Index progress logs and decisions for semantic search
   - Enable agents to query project history and context
   - Markdown file are no longer for memory, only for initial instructions
   - Private collections, per agent / track for context and progress (the Orchestrator can review them)
   - Shared collections for internal documentation and collaboration between agents

2. **Upstash Qstash for Asynchronous Messaging**:
   - Enable agents to send messages to each other
   - Implement a publish/subscribe model for track updates
   - Allow the Orchestrator to broadcast announcements
   - Support delayed/scheduled messages for coordination

3. **Upstash Redis for State Management**:
   - Track the current state of each agent and track
   - Store ephemeral data that doesn't belong in memory files
   - Implement locks to prevent conflicts in parallel operations
   - Enable real-time status updates

### Firecrawl Integration (or Firecrawl)

- Use Firecrawl specifically for fetching and indexing third-party documentation
- Upload markdown content files scrapped by Firecrawl into Pinecone Assistant, the RAG tool from Pinecone

### Separation of Concerns

- **Memory Files**: Long-term persistent storage (source of truth)
- **Pinecone**: Semantic search and retrieval of project knowledge
- **Pinecone Assistant**: Semantic search and retrieval of tech documentations
- **Qstash**: Communication and coordination between agents
- **Redis**: Ephemeral state management and real-time status

### CLIless

To save us the writing and maintenance of CLI commands, we'll document to agents in initial prompts the main basic commands to use for each tool, directly with the tool APIs, using curl. No need for a CLI wrapper. And no need for the tool's CLI or SDK.