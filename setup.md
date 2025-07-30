# LeetCode MCP Server Setup with Claude Code

This guide walks you through integrating the LeetCode MCP server with Claude Code for enhanced LeetCode problem-solving capabilities.

## Prerequisites

- Node.js (v20.x or above)
- Claude Code CLI installed
- Optional: LeetCode session cookie for authenticated access

## Installation Steps

### Step 1: Install the LeetCode MCP Server

```bash
npm install @jinzcdev/leetcode-mcp-server -g
```

### Step 2: Configure Claude Code MCP Settings

Add the LeetCode MCP server to your Claude Code configuration:

```bash
claude mcp add leetcode npx -- -y @jinzcdev/leetcode-mcp-server --site global
```

For LeetCode China users, use:

```bash
claude mcp add leetcode npx -- -y @jinzcdev/leetcode-mcp-server --site cn
```

### Step 3: Verify Installation

Check that the server is properly configured:

```bash
# List all configured MCP servers
claude mcp list

# Get detailed information about the LeetCode server
claude mcp get leetcode
```

## Optional: Add Authentication

To access user-specific features (submissions, progress, etc.), add your LeetCode session cookie:

### Getting Your Session Cookie

1. Log into LeetCode in your browser
2. Open Developer Tools (F12)
3. Go to Application/Storage → Cookies → https://leetcode.com
4. Copy the value of the `LEETCODE_SESSION` cookie

### Update Configuration with Authentication

```bash
# Remove existing configuration
claude mcp remove leetcode -s local

# Add with session cookie
claude mcp add leetcode npx -- -y @jinzcdev/leetcode-mcp-server --site global --session YOUR_LEETCODE_SESSION_COOKIE
```

## Alternative Configuration Methods

### Using Smithery (for Claude Desktop)

```bash
npx -y @smithery/cli install @jinzcdev/leetcode-mcp-server --client claude
```

### Manual JSON Configuration

If you prefer manual configuration, you can create a `.mcp.json` file in your project:

```json
{
  "mcpServers": {
    "leetcode": {
      "command": "npx",
      "args": ["-y", "@jinzcdev/leetcode-mcp-server", "--site", "global"],
      "env": {
        "LEETCODE_SESSION": "your_session_cookie_here"
      }
    }
  }
}
```

## Usage

Once configured, Claude Code will automatically have access to LeetCode functionality through the MCP server. You can now:

- Fetch LeetCode problems
- Access problem details and constraints
- View example test cases
- Get hints and solutions (if authenticated)
- Track your progress and submissions

## Troubleshooting

### Common Issues

1. **Permission errors**: Ensure Node.js and npm are properly installed with correct permissions
2. **Command not found**: Make sure the global npm bin directory is in your PATH
3. **Authentication issues**: Verify your session cookie is valid and not expired

### Useful Commands

```bash
# Check MCP server status
claude mcp list

# Remove a server
claude mcp remove leetcode -s local

# View server configuration
claude mcp get leetcode
```

## Additional Resources

- [LeetCode MCP Server GitHub](https://github.com/jinzcdev/leetcode-mcp-server)
- [Claude Code MCP Documentation](https://docs.anthropic.com/en/docs/claude-code/mcp)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)