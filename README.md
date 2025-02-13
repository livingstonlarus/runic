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

## Example
Here's an except of a chat with an AI coding assistant enhanced with Runic, inside of an IDE:

>**User**
Follow your instructions in .runic/instruct.md

>**AI Assistant**
I'll help you initialize the Runic framework for this project. I notice that the .runic directory is already initialized, so I'll first check if the project brief exists and then analyze the current Next.js codebase to populate the necessary context files in the memory directory. This will help establish a solid foundation for our development process.

>Let me check if the project brief exists and examine its content to determine our next steps.

>`.runic/memory/projectBrief.md`

>Based on the project brief, I'll update the tech context to document our technology stack and requirements.

>`.runic/memory/techContext.md +33 -0`

>I'll update the product context to define the core features and requirements of our task management app.

>`.runic/memory/productContext.md +35 -0`

>I have successfully initialized the Runic system for this Next.js task management project by:
>- Verifying the existence of projectBrief.md and confirming it contains the project definition for a task management app with Next.js, NextAuth.js, and Prisma.
>- Documenting the technical context in techContext.md, including:
>-- Technology stack (Next.js, NextAuth.js, Prisma, TailwindCSS)
>-- Technical requirements for authentication, database, and frontend
>-- Current and required dependencies
>- Establishing the product context in productContext.md, detailing:
>-- Core features for authentication, task management, and UI
>-- User requirements for authentication, task features, and user experience

>The project is now properly configured with Runic, and we have a clear understanding of both technical and product requirements for the task management application.

>**User**
@docs https://nextjs.org/

>**AI Assistant**
I'll fetch the Next.js documentation to ensure we have the latest information for our task management app implementation.

###### Terminal
```sh
runic docs https://nextjs.org/docs
```
>I've successfully initialized the project context and documentation for our Next.js task management app. Here's what has been accomplished:
>- Verified the project brief in .runic/memory/projectBrief.md, which outlines a task management app using Next.js with next-auth and Prisma
>- Analyzed the existing context files in .runic/memory directory
>- Found that some context files (activeContext.md, systemPatterns.md, progress.md) are empty and need to be populated
>- Confirmed the technical stack from techContext.md includes Next.js (App Router), NextAuth.js, Prisma ORM, TailwindCSS, and TypeScript
>- Identified core features from productContext.md including user authentication and task management capabilities
>- Fetched and stored the latest Next.js documentation in .runic/docs for reference

>The project is now properly set up with Runic integration, and we have all the necessary documentation and context to proceed with development.

>**User**
Lookup Route Segment Config in the Next.js docs

>**AI Assistant**
I'll help you find information about Route Segment Config in the Next.js documentation. I notice that the Next.js documentation has already been fetched into the .runic/docs directory, so I'll look up the specific section about Route Segment Config to provide you with the relevant information.

> Let me search for information about Route Segment Config in the Next.js documentation.

`.runic/docs/Introduction _ Next_js/docs/app/api-reference/file-conventions/route-segment-config.md`

>I searched through the Next.js documentation and found that the Route Segment Config is a feature in Next.js that allows you to configure various aspects of route segments in the App Router. The documentation shows that it includes options for controlling dynamic behavior, revalidation, runtime environment, preferred regions, and more. The search revealed that this information is located in the`.runic/docs` directory, specifically in the file`/docs/app/api-reference/file-conventions/route-segment-config.md`.

>**User**
What about maxDuration? Does Next.js limit the execution of server-side logic?

>**AI Assistant**
According to the Next.js documentation, by default Next.js does not impose any limits on the execution time of server-side logic (whether it's rendering a page or handling an API request). However, you can set a`maxDuration` value in your route segments (layout.tsx, page.tsx, or route.ts) to specify execution limits. This setting requires Next.js version 13.4.10 or higher. While Next.js itself doesn't enforce limits, deployment platforms like Vercel can use this`maxDuration` configuration from the Next.js build output to implement specific execution time limits for your application.

>**User**
@docs list

>**AI Assistant**
Let me check the available documentation in the .runic/docs directory.

>`test/.runic/docs`

>I've checked the .runic/docs directory and found that there is currently one documentation set available:
>- Next.js Introduction documentation

>**User**
@mem update

>**AI Assistant**
I'll help update the project memory based on the latest changes. I notice that the project is a Next.js application using TypeScript and TailwindCSS, with a basic layout structure and routing setup. I'll record these technical details and current progress in the memory files.

>Let me check the current memory files to understand what needs to be updated.

>`.runic/memory/techContext.md`

>`.runic/memory/systemPatterns.md`

>`.runic/memory/progress.md`

>I'll update the system patterns and progress files to reflect the current state of the project.

>`.runic/memory/systemPatterns.md +26 -0`

I'll update the progress file to document the current state of the project and its implementation status.

.runic/memory/progress.md

+ 26 - 0

Review

Updated the project memory files to reflect the current state of the Next.js application. The updates include:

- Documented the system patterns including architecture, design patterns, code organization, styling approach, and performance considerations
- Recorded the development progress, marking completed tasks and outlining pending tasks
- Maintained the technical context with details about the technology stack, dependencies, and requirements
The memory now accurately reflects the project's use of Next.js with TypeScript and TailwindCSS, the implemented dark/light mode theming, and the planned features like authentication and database integration.

## 🤝 Contributing
To contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### TODO List
While Runic started as an AI coding assistant enhancer, it's evolving into a general-purpose framework. Our next steps:

#### [TOP PRIORITY] Context Window Management
- [ ] Find ways to keep initial Runic instructions and rules in context window; the AI assistant often forget them, too quickly
- [ ] As a second priority, find ways to better keep snippets of relevant docs in context window.
- [ ] Maybe as a quick fix try to breakdown in more CLI commands that would be easier to remember for the AI assistant
- [ ] Then evealute using embeddings in vector stores for both RAG and LTM (see Pinecone, Weaviate, or ChromaDB), locally or in the cloud (private or public), for advanced search and retrieval, efficient storage and enhanced contextual understanding
- [ ] And evaluate use of LangChain or LlamaIndex to facilitate integration of embeddings and vector stores (tools to manage data ingestion, embedding generation, and retrieval processes). What about Mem0?
- [ ] Evaluate using Crawl4AI and alternatives in place of our own spider

#### Context Adaptability
- [ ] Create templates for various use cases beyond coding
- [ ] Implement context-based template selection
- [ ] Add custom template management support

#### Documentation Crawler Enhancement
- [ ] Implement max depth setting to prevent infinite crawling
- [ ] Smarter naming of docs directories
- [ ] Generate table of content (outline) of each docs to help AI assistant navigate it
- [ ] Enhance main content detection and filtering
- [ ] Add support for various documentation formats and structures
- [ ] Automatically fetch documentation for the current project dependencies
- [ ] Implement rate limiting and politeness delays

#### More Layers
- [ ] Expand LLM capabilities with more layers, like files/codebase indexing and web search
- [ ] Expose more tools / functions as CLI from the various layers, for use by the AI assistant

## 📜 License
**Runic** is open-source under the **MIT License**.
