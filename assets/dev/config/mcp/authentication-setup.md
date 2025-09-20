# MCP Authentication Setup Guide

## Overview
This guide provides comprehensive instructions for setting up authentication for all MCP servers in the DocGen CLI project. Proper authentication is essential for full MCP integration functionality.

## Authentication Status

### ✅ Ready to Use (No Setup Required)
- **Context7**: Public API access - no authentication required
- **Browser Tools**: Local browser access - no authentication required  
- **Dart**: Workspace-based authentication - automatically configured

### ⚠️ Requires Setup
- **Byterover**: Extension-based authentication required
- **TestSprite**: API key authentication required
- **Playwright**: Local installation required

## Setup Instructions

### 1. Byterover Extension Authentication

**Status**: Requires Setup  
**Method**: Extension-based authentication

#### Setup Steps:
1. **Install Byterover Extension**
   - Open your IDE (VS Code, Cursor, etc.)
   - Go to Extensions marketplace
   - Search for "Byterover" extension
   - Install the extension

2. **Login Through Extension**
   - Open the Byterover extension panel
   - Click "Login" or "Connect"
   - Follow the authentication flow
   - Complete the login process

3. **Connect to Workspace**
   - Ensure the extension is connected to your current workspace
   - Verify workspace connection in extension settings
   - Check that the extension shows "Connected" status

4. **Verify Authentication**
   - Open extension settings
   - Confirm authentication status shows "Authenticated"
   - Test by using Byterover features in your IDE

#### Troubleshooting:
- If extension doesn't appear, restart your IDE
- Check internet connection for authentication
- Verify extension permissions in IDE settings
- Contact Byterover support if login fails

### 2. TestSprite API Key Authentication

**Status**: Requires Setup  
**Method**: API key authentication

#### Setup Steps:
1. **Get API Key**
   - Visit: https://www.testsprite.com/dashboard/settings/apikey
   - Sign up or login to your TestSprite account
   - Navigate to API Keys section
   - Create a new API key
   - Copy the generated API key

2. **Set Environment Variable**
   ```bash
   # Linux/macOS
   export TESTSPRITE_API_KEY="your_api_key_here"
   
   # Windows (Command Prompt)
   set TESTSPRITE_API_KEY=your_api_key_here
   
   # Windows (PowerShell)
   $env:TESTSPRITE_API_KEY="your_api_key_here"
   ```

3. **Add to .env File**
   ```bash
   # Add to your project's .env file
   echo "TESTSPRITE_API_KEY=your_api_key_here" >> .env
   ```

4. **Restart Terminal/IDE**
   - Close and reopen your terminal
   - Restart your IDE to pick up new environment variables
   - Verify the variable is set: `echo $TESTSPRITE_API_KEY`

#### Troubleshooting:
- Ensure API key is correctly copied (no extra spaces)
- Check that .env file is in project root
- Verify environment variable is set: `env | grep TESTSPRITE`
- Test API key validity on TestSprite dashboard

### 3. Playwright Installation

**Status**: Requires Installation  
**Method**: Local installation

#### Setup Steps:
1. **Install Playwright**
   ```bash
   pip install playwright
   ```

2. **Install Browsers**
   ```bash
   playwright install chromium
   ```

3. **Verify Installation**
   ```bash
   playwright --version
   ```

4. **Test Browser Launch**
   ```bash
   playwright codegen
   ```

#### Troubleshooting:
- Ensure Python and pip are properly installed
- Check internet connection for browser downloads
- Verify system permissions for browser installation
- Try installing specific browser: `playwright install chromium --with-deps`

## Authentication Verification

### Run Authentication Check
```bash
# Run the authentication setup script
python3 assets/dev/scripts/mcp_authentication_setup.py --verbose
```

### Expected Output
```
MCP Authentication Status:
  byterover: ✅ authenticated - Extension connected
  testsprite: ✅ authenticated - API key found
  context7: ✅ authenticated - API accessible
  browser_tools: ✅ authenticated - Browser accessible
  playwright: ✅ authenticated - Playwright installed
  dart: ✅ authenticated - Workspace accessible
```

## Integration Testing

### Test Individual Servers
```bash
# Test Byterover
python3 -c "from assets.dev.scripts.mcp_integration import MCPIntegrationCore; mcp = MCPIntegrationCore(); print(mcp.execute_mcp_call('byterover', 'test_connection'))"

# Test TestSprite
python3 -c "from assets.dev.scripts.mcp_integration import MCPIntegrationCore; mcp = MCPIntegrationCore(); print(mcp.execute_mcp_call('testsprite', 'bootstrap_tests', 3000, 'backend', '.', 'codebase'))"

# Test Context7
python3 -c "from assets.dev.scripts.mcp_integration import MCPIntegrationCore; mcp = MCPIntegrationCore(); print(mcp.execute_mcp_call('context7', 'resolve_library_id', 'click'))"
```

### Run Complete Integration
```bash
# Run complete MCP integration with authentication
python3 assets/dev/scripts/complete_mcp_integration.py --verbose
```

## Configuration Files

### Authentication Configuration
- **Location**: `assets/dev/config/mcp/auth_config.yaml`
- **Purpose**: Stores authentication status and setup instructions
- **Auto-generated**: Created by authentication setup script

### MCP Configuration
- **Location**: `assets/dev/config/mcp/mcp_config.yaml`
- **Purpose**: Main MCP server configuration with authentication settings
- **Updated**: Automatically updated with authentication status

## Security Considerations

### API Key Security
- Never commit API keys to version control
- Use environment variables for sensitive data
- Rotate API keys regularly
- Monitor API key usage

### Extension Security
- Only install trusted extensions
- Keep extensions updated
- Review extension permissions
- Use official extension sources

### Local Installation Security
- Verify package integrity before installation
- Use official package sources
- Keep installations updated
- Monitor for security vulnerabilities

## Troubleshooting Common Issues

### Authentication Failures
1. **Check Network Connection**
   - Ensure internet connectivity
   - Verify firewall settings
   - Check proxy configurations

2. **Verify Credentials**
   - Double-check API keys
   - Confirm extension login status
   - Test credentials independently

3. **Environment Issues**
   - Restart terminal/IDE
   - Check environment variables
   - Verify file permissions

### Integration Errors
1. **Check Server Status**
   - Verify MCP servers are running
   - Check server configurations
   - Review error logs

2. **Validate Configuration**
   - Check configuration file syntax
   - Verify server endpoints
   - Confirm authentication settings

3. **Test Connectivity**
   - Ping server endpoints
   - Check port availability
   - Verify network access

## Support and Resources

### Documentation
- [MCP Integration Guide](MCP_INTEGRATION_GUIDE.md)
- [MCP Configuration Reference](mcp_config.yaml)
- [TestSprite Documentation](https://www.testsprite.com/docs)
- [Byterover Documentation](https://byterover.com/docs)

### Getting Help
- Check error logs in `assets/reports/mcp/`
- Run diagnostic scripts with `--verbose` flag
- Review configuration files for issues
- Contact support for persistent problems

## Next Steps

After completing authentication setup:

1. **Run Complete Integration**
   ```bash
   python3 assets/dev/scripts/complete_mcp_integration.py
   ```

2. **Test MCP Commands**
   ```bash
   python3 docgen_cli.py mcp status
   python3 docgen_cli.py mcp test
   ```

3. **Start Development Workflow**
   ```bash
   python3 docgen_cli.py mcp workflow
   ```

4. **Monitor Integration**
   ```bash
   python3 docgen_cli.py mcp report
   ```

## Conclusion

Proper authentication setup is crucial for full MCP integration functionality. Follow the setup instructions carefully, verify authentication status, and test integration before proceeding with development workflows.

For additional support or questions, refer to the troubleshooting section or contact the development team.