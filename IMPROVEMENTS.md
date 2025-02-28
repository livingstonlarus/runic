# Runic Improvements

This document outlines proposed improvements to the Runic framework based on user feedback and evolving requirements.

## 1. Configuration-Based Optional Integrations

### Current Situation
- Integrations like Pinecone and Crawl4AI are mentioned in the codebase but not fully implemented
- Git platform tools are hardcoded without user preference consideration
- Integration points exist but lack configuration options

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
  crawl4ai:
    enabled: false  # Disabled by default
  
  # Git platform preference
  git:
    platform_cli: "gh"  # Options: "gh" (GitHub), "glab" (GitLab)
    
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

### Implementation Details

1. **Configuration Loading**:
   - Create a `config.py` module to load and validate the configuration
   - Support environment variable expansion
   - Provide sensible defaults

2. **Integration Detection**:
   - Check for the presence of optional dependencies
   - Warn when an integration is enabled but dependencies are missing
   - Suggest installation commands for missing dependencies

3. **CLI Updates**:
   - Add `runic config` command to view/edit configuration
   - Add `runic config init` to generate a default configuration file

## 2. Natural Language Commands vs. Structured Commands

### Current Situation
- Chat commands use a specific syntax (e.g., `$mem update`, `$branch create`)
- CLI commands have a structured format (e.g., `runic track init`)
- Users need to memorize specific command formats

### Proposed Solution: Leverage LLM Understanding

1. **Natural Language Chat Commands**:
   - Allow agents to understand natural language requests
   - Examples:
     - "Update your memory" instead of `$mem update`
     - "Create a branch for the login feature" instead of `$branch create login-feature`
     - "Mark the auth branch as ready for merge" instead of `$branch ready auth`

2. **Implementation Approach**:
   - Keep the existing command handlers but add a natural language parser
   - Use pattern matching or simple NLP to map natural language to commands
   - Maintain backward compatibility with the `$` command syntax

3. **CLI Command Execution**:
   - Allow agents to directly execute git commands and other CLI operations
   - Trust the LLM's ability to generate correct commands based on context
   - Example: Instead of wrapping `git branch -b feature`, let the agent execute it directly

### Code Example: Natural Language Command Parser

```python
def parse_natural_language(message: str) -> Optional[Tuple[str, str, List[str]]]:
    """
    Parse natural language into commands.
    
    Args:
        message: The natural language message
        
    Returns:
        A tuple of (command_type, subcommand, args) if a command is recognized,
        or None if no command is recognized
    """
    # Memory update patterns
    if re.search(r'update (?:your |the )?memory', message, re.IGNORECASE):
        return ('mem', 'update', [])
    
    # Branch creation patterns
    branch_match = re.search(r'create (?:a )?(?:new )?branch (?:called |named )?["\']?([a-zA-Z0-9_-]+)["\']?', 
                            message, re.IGNORECASE)
    if branch_match:
        return ('branch', 'create', [branch_match.group(1)])
    
    # Continue with other patterns...
    
    return None
```

## 3. Agent Communication and Coordination

### Current Situation
- Agents share memory through files in `.runic/memory/`
- Coordination happens through Git branches and merge requests
- No real-time communication between agents

### Proposed Solution: Enhanced Communication Stack

1. **Pinecone for Knowledge Management**:
   - Store internal documentation and project knowledge
   - Index progress logs and decisions for semantic search
   - Enable agents to query project history and context
   - Keep memory files as the source of truth, with Pinecone as an index

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

### Implementation Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Orchestrator   │     │  Specialist 1   │     │  Specialist 2   │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Runic Framework                           │
├─────────────────┬─────────────────┬─────────────────┬───────────┤
│  Memory Files   │    Pinecone     │  Upstash Qstash │   Redis   │
│  (Source of     │  (Knowledge     │  (Messaging)    │  (State)  │
│   Truth)        │   Index)        │                 │           │
└─────────────────┴─────────────────┴─────────────────┴───────────┘
```

### Separation of Concerns

- **Memory Files**: Long-term persistent storage (source of truth)
- **Pinecone**: Semantic search and retrieval of project knowledge
- **Qstash**: Communication and coordination between agents
- **Redis**: Ephemeral state management and real-time status

### Crawl4AI Integration

Keep Crawl4AI separate from Pinecone since it has its own vector system:

- Use Crawl4AI specifically for fetching and indexing third-party documentation
- Allow agents to query both Pinecone (for internal knowledge) and Crawl4AI (for external docs)
- Implement a unified query interface that searches both systems as needed

## 4. Implementation Roadmap

### Phase 1: Configuration System
1. Implement `.runic/config.yaml` structure
2. Add configuration loading and validation
3. Update CLI to support configuration management

### Phase 2: Natural Language Commands
1. Implement natural language command parser
2. Maintain backward compatibility with `$` commands
3. Add examples and documentation for natural language usage

### Phase 3: Pinecone Integration
1. Implement Pinecone client and indexing
2. Add memory file synchronization with Pinecone
3. Implement semantic search capabilities

### Phase 4: Messaging and State Management
1. Implement Upstash Qstash integration for messaging
2. Add Redis integration for state management
3. Update agent coordination mechanisms

## 5. Backward Compatibility Considerations

To ensure a smooth transition:

1. **Maintain Support for Existing Commands**:
   - Keep the `$` command syntax working
   - Support both CLI commands and direct execution

2. **Optional Integrations**:
   - Make all new integrations truly optional
   - Ensure core functionality works without any third-party services

3. **Migration Path**:
   - Provide migration tools for existing projects
   - Document upgrade process for users

## 6. Conclusion

These improvements aim to make Runic more flexible, natural to use, and powerful while maintaining its core philosophy of lightweight, token-efficient parallel development. By leveraging the natural language capabilities of LLMs and adding optional integrations, Runic can become even more effective without adding unnecessary complexity.

The configuration-based approach ensures that users only enable the features they need, keeping the framework lightweight for simple projects while allowing it to scale up for more complex scenarios.