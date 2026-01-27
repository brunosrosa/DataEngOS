# TOON MCP Usage Guide

## 1. Status Check

The **TOON MCP Server** is successfully installed and communicating correctly on your machine!
We verified this by sending a direct tool call request which successfully converted JSON to TOON format:

**Input JSON**:
`{"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}`

**Output TOON**:

```TOON
users[2]{id,name}:
  1,Alice
  2,Bob
```

## 2. How to Enforce TOON Usage

You asked how to force the LLM to use TOON for JSON outputs. Here are the three best methods:

### A. Via Prompt (Easiest)

You can simply instruct the model in your prompt to use the tool.

**Example Prompt:**
> "Analyze the data in `data.csv` and output the result as a JSON object. **IMPORTANT: Use the `encode_toon` tool to format your final JSON response to save tokens.**"

### B. Via System Instructions (Best for Consistency)

If you want the model to *always* use TOON without being asked every time, you should add this to your System Instruction (or "Custom Instructions").

**Instruction:**
> "You have access to a tool called `encode_toon`. Whenever you need to provide data that would normally be in JSON format (especially large datasets), you MUST use the `encode_toon` tool to compress it before outputting. Do not output raw JSON for data arrays."

**For Gemini CLI:**
You can pass a system instruction file if supported, or prepend it to your prompt.
*(Note: The `gemini` CLI is currently having API/auth issues on your machine, but this applies to any MCP client).*

### C. Workspace Rules (For Agentic IDEs)

If you are using an Agentic IDE (like Cursor, Windsurf, or a configured workspace), you can add a rule file.

**Global Rule (Recommended):**
Create or edit `~/.cursorrules` (in your home directory) to apply this to ALL projects.

**Project Rule:**
Create or edit `.cursorrules` (in your project root).

**Content:**

```markdown
# Data Formatting Rules
- Always prioritize token efficiency.
- When generating data or logs that are structured as JSON, verify if the `encode_toon` tool is available.
- If available, use `encode_toon` to format the output.
```

### D. Programmatic Usage (For `DataEngOS` CLI)

Since `DataEngOS` is your own project, you don't even need the MCP tool for your internal CLI. You can use the library directly in your code to save tokens when sending data TO the LLM.

**Installation:**
`npm install toon` or `pip install toon` (if available)

**Usage:**

1. Retrieve data from DB.
2. Encode to TOON format in your Python/Node code.
3. Send the TOON string to the LLM.
4. The LLM understands TOON natively (it's designed for this)!
