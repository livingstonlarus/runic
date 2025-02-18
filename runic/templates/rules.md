# Project Rules

## Code Style
- Use consistent indentation (2 spaces)
- Follow language-specific naming conventions
- Keep functions small and focused
- Add descriptive comments for complex logic

## Git Practices
- Write clear commit messages
- Always properly quote the commit message
- Create feature branches for new work
- Keep commits atomic and focused
- Pull and rebase before pushing
- Use consistent branch naming conventions (e.g., `feature/feature-name`, `bugfix/bug-description`, `task/task-name`)

## Testing
- Write unit tests for new features
- Maintain test coverage above 80%
- Run full test suite before merging
- Mock external dependencies

## Documentation
- Update README for major changes
- Document public APIs
- Include setup instructions
- Keep docs in sync with code

## Security
- Never commit secrets or credentials
- Validate all user input
- Use secure dependencies
- Follow OWASP guidelines

## Performance
- Optimize database queries
- Cache expensive operations
- Minimize HTTP requests
- Profile before optimizing

**Rule 2: Format Responses in Markdown (Revised for AI Coding Assistants with File Editing Capacity)**

1.  **Markdown Formatting:** Continue to format responses in markdown for readability.

2.  **Code Edits for AI Coding Assistants with File Editing Capacity:** When providing code edits for AI coding assistants with file editing capacity (e.g., Cursor, Windsurf, VS Code with Copilot Edits, Trae), prioritize the following format:

    *   **"Diff-like" Presentation:** Present code edits in a way that resembles a diff or in-editor modification, clearly highlighting the changes (additions, modifications, deletions) within the context of the existing code.
    *   **Code Blocks with Language and Path:** Continue to use code blocks with language IDs and file paths to specify the target file for edits.
    *   **Explicit Edit Type and Location:** For significant structural changes (insertions, deletions of sections), explicitly indicate the type of edit and the intended location within the file using comments or instructions within `{{...}}`.
    *   **Clarity and Delimiters:** Ensure clear distinction between markdown for code edits and markdown for chat output formatting. Use code blocks, comments, and explicit instructions to avoid confusion.

3.  **Code Block Language and Path:**  Always format code blocks with a language ID and the path to the file when suggesting edits.  Example:

    ````language:path/to/file
    // existing code...
    {{ Write updated code here... }}
    // ...
    ````

**Rule 3:  File and Directory Operations - Existence Checks**

1.  **Directory Existence Check:** When instructions involve creating files in directories, always ensure that the instructions include a check for the existence of the target directory (and any necessary parent directories).

2.  **Directory Creation Instructions:** If the target directory or parent directories do not exist, provide explicit instructions to create them before proceeding with file creation.  Use standard command-line tools like `mkdir -p` for directory creation instructions where appropriate.

3.  **Robust Instructions:** Aim to provide instructions that are robust and handle cases where necessary directories might be missing, preventing errors and ensuring a smoother user experience.

**Reinforced Rules for Code Edits:**

*   **Rule:** Always double-check file paths in code blocks to ensure they are correct.
*   **Rule:**  Always use correct markdown formatting for code blocks, including language IDs and file paths.
*   **Rule:** If diff-based edits fail, be prepared to provide the full file content as a fallback.