# Comprehensive Authentication System Guide

## Overview

The Comprehensive Authentication System for DocGen CLI provides a complete solution for managing MCP server authentication, API keys, error recovery, and setup processes. This system integrates four main components:

1. **Real-time Authentication Tracker** - Live monitoring of authentication status
2. **Secure Key Manager** - Encrypted API key storage and management
3. **Error Recovery System** - Automatic retry mechanisms and circuit breakers
4. **Setup Wizard** - Interactive setup guidance with platform-specific instructions

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                Comprehensive Authentication System           │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ Real-time Auth  │  │ Secure Key      │  │ Error        │ │
│  │ Tracker         │  │ Manager         │  │ Recovery     │ │
│  │                 │  │                 │  │ System       │ │
│  │ • Live status   │  │ • AES-256 enc   │  │ • Retry logic│ │
│  │ • Health checks │  │ • Key rotation  │  │ • Circuit    │ │
│  │ • Notifications │  │ • Audit logging │  │   breakers   │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                Setup Wizard                             │ │
│  │                                                         │ │
│  │ • Interactive setup                                     │ │
│  │ • Platform-specific instructions                       │ │
│  │ • Automated validation                                  │ │
│  │ • Progress tracking                                     │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Run Complete Setup
```bash
# Run the comprehensive setup wizard
python3 assets/dev/scripts/comprehensive_auth_system.py --setup
```

### 2. View Live Dashboard
```bash
# Start live monitoring dashboard
python3 assets/dev/scripts/comprehensive_auth_system.py --live
```

### 3. Check System Status
```bash
# Get current system status
python3 assets/dev/scripts/comprehensive_auth_system.py --status
```

## Component Details

### 1. Real-time Authentication Tracker

**Purpose**: Monitor authentication status of all MCP servers in real-time.

**Features**:
- Live authentication status monitoring
- WebSocket-based status updates (planned)
- Health check workers with configurable intervals
- Status change notifications and alerts
- Historical authentication status logging

**Usage**:
```bash
# Check authentication status once
python3 assets/dev/scripts/real_time_auth_tracker.py --check

# Run live dashboard
python3 assets/dev/scripts/real_time_auth_tracker.py --live

# Generate status report
python3 assets/dev/scripts/real_time_auth_tracker.py --report
```

**Configuration**:
- Health check interval: 30 seconds (configurable)
- Status change threshold: 5 seconds
- History retention: Last 100 status changes

### 2. Secure Key Manager

**Purpose**: Securely store, manage, and rotate API keys for MCP servers.

**Features**:
- AES-256 encryption for API key storage
- Environment variable management with validation
- API key rotation and expiration tracking
- Secure key sharing and backup mechanisms
- Audit logging for all key operations

**Usage**:
```bash
# Display key management dashboard
python3 assets/dev/scripts/secure_key_manager.py --dashboard

# Add API key interactively
python3 assets/dev/scripts/secure_key_manager.py --setup

# Add API key for specific server
python3 assets/dev/scripts/secure_key_manager.py --add testsprite

# Get API key for server
python3 assets/dev/scripts/secure_key_manager.py --get testsprite

# Rotate API key
python3 assets/dev/scripts/secure_key_manager.py --rotate testsprite

# Set environment variable
python3 assets/dev/scripts/secure_key_manager.py --set-env testsprite
```

**Security Features**:
- Master key encryption with PBKDF2
- Encrypted storage in `assets/dev/config/mcp/keys/`
- Audit logging for all operations
- Key rotation and expiration support

### 3. Error Recovery System

**Purpose**: Provide automatic retry mechanisms and intelligent error recovery.

**Features**:
- Automatic retry with exponential backoff
- Circuit breaker pattern for failing services
- Graceful degradation when services unavailable
- Error classification and intelligent recovery strategies
- Recovery status reporting and monitoring

**Usage**:
```bash
# Display recovery dashboard
python3 assets/dev/scripts/error_recovery_system.py --dashboard

# Test recovery system
python3 assets/dev/scripts/error_recovery_system.py --test

# Generate recovery report
python3 assets/dev/scripts/error_recovery_system.py --report
```

**Recovery Strategies**:
- **Network errors**: Retry with exponential backoff
- **Authentication errors**: Manual intervention required
- **Timeout errors**: Retry with increased timeout
- **Rate limit errors**: Retry with backoff
- **Service unavailable**: Circuit breaker activation
- **Configuration errors**: Manual intervention required

### 4. Setup Wizard

**Purpose**: Provide interactive setup guidance with platform-specific instructions.

**Features**:
- Interactive setup wizard for each MCP server
- Step-by-step guided configuration
- Platform-specific setup instructions (Windows, macOS, Linux)
- Automated setup validation and testing
- Setup progress tracking and rollback capabilities

**Usage**:
```bash
# Run interactive setup wizard
python3 assets/dev/scripts/setup_wizard.py --interactive

# Setup specific server
python3 assets/dev/scripts/setup_wizard.py --server testsprite

# Validate setup for server
python3 assets/dev/scripts/setup_wizard.py --validate testsprite

# Show setup summary
python3 assets/dev/scripts/setup_wizard.py --summary
```

**Supported Platforms**:
- Windows (Command Prompt, PowerShell)
- macOS (Terminal)
- Linux (Bash, Zsh)

## MCP Server Setup Instructions

### Byterover Setup

**Method**: Extension-based authentication

**Steps**:
1. **Install Extension**
   - Open VS Code or Cursor
   - Go to Extensions (Ctrl+Shift+X / Cmd+Shift+X)
   - Search for "Byterover"
   - Click "Install"

2. **Authenticate**
   - Open Byterover extension panel
   - Click "Login" or "Connect"
   - Follow browser authentication flow
   - Complete login process

3. **Connect Workspace**
   - Verify workspace connection in extension settings
   - Ensure extension shows "Connected" status

**Validation**: Check extension authentication status

### TestSprite Setup

**Method**: API key authentication

**Steps**:
1. **Create Account**
   - Visit https://www.testsprite.com
   - Sign up for account
   - Verify email address

2. **Get API Key**
   - Login to TestSprite dashboard
   - Go to Settings > API Keys
   - Create new API key
   - Copy generated key

3. **Set Environment Variable**
   ```bash
   # Linux/macOS
   export TESTSPRITE_API_KEY="your_api_key_here"
   
   # Windows
   set TESTSPRITE_API_KEY=your_api_key_here
   
   # Or add to .env file
   echo "TESTSPRITE_API_KEY=your_api_key_here" >> .env
   ```

**Validation**: Check API key in environment variables

### Playwright Setup

**Method**: Local installation

**Steps**:
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
   playwright codegen
   ```

**Validation**: Check Playwright installation and browser availability

### Context7 Setup

**Method**: Public API (no authentication required)

**Steps**:
1. **Verify Internet Connection**
   - Ensure internet connectivity
   - Context7 API is publicly accessible

**Validation**: Check API connectivity

### Browser Tools Setup

**Method**: Local browser access

**Steps**:
1. **Verify Browser Installation**
   - Check if Chrome, Firefox, or Edge is installed
   - Browser Tools will use default browser

**Validation**: Check browser availability

### Dart Setup

**Method**: Workspace-based authentication

**Steps**:
1. **Verify Workspace**
   - Ensure you're in valid project workspace
   - Dart automatically detects workspace

**Validation**: Check workspace configuration

## Configuration Files

### Main Configuration
- **Location**: `assets/dev/config/mcp/mcp_config.yaml`
- **Purpose**: Main MCP server configuration with authentication settings

### Authentication Configuration
- **Location**: `assets/dev/config/mcp/auth_config.yaml`
- **Purpose**: Authentication status and setup instructions

### Key Storage
- **Location**: `assets/dev/config/mcp/keys/`
- **Purpose**: Encrypted API key storage and audit logs

### Reports
- **Location**: `assets/reports/mcp/`
- **Purpose**: System reports and status logs

## Security Considerations

### API Key Security
- Never commit API keys to version control
- Use environment variables for sensitive data
- Rotate API keys regularly
- Monitor API key usage through audit logs

### Encryption
- Master key stored securely in `assets/dev/config/mcp/keys/master.key`
- API keys encrypted with AES-256
- PBKDF2 key derivation for additional security

### Access Control
- Proper file permissions on configuration files
- Secure storage of master encryption key
- Audit logging for all sensitive operations

## Monitoring and Maintenance

### Health Monitoring
- Continuous health checks every 60 seconds
- Real-time status updates and notifications
- Historical health data and trends

### Error Recovery
- Automatic retry with exponential backoff
- Circuit breaker pattern for failing services
- Graceful degradation and fallback strategies

### Reporting
- Comprehensive system reports
- Authentication status reports
- Key management audit logs
- Error recovery statistics

## Troubleshooting

### Common Issues

1. **Authentication Failures**
   - Check network connectivity
   - Verify credentials and API keys
   - Review extension login status

2. **Key Management Issues**
   - Ensure master key file exists
   - Check file permissions
   - Verify encryption/decryption

3. **Error Recovery Problems**
   - Review circuit breaker status
   - Check retry configuration
   - Monitor error patterns

4. **Setup Wizard Issues**
   - Verify platform detection
   - Check step validation
   - Review setup progress

### Debug Mode
```bash
# Enable verbose logging
python3 assets/dev/scripts/comprehensive_auth_system.py --verbose --dashboard
```

### Log Files
- System logs: Console output with timestamps
- Audit logs: `assets/dev/config/mcp/keys/audit_log.json`
- Status reports: `assets/reports/mcp/`

## Integration with DocGen CLI

### CLI Commands
```bash
# Check MCP status
python3 docgen_cli.py mcp status

# Test MCP integration
python3 docgen_cli.py mcp test

# Run MCP workflow
python3 docgen_cli.py mcp workflow
```

### Programmatic Usage
```python
from assets.dev.scripts.comprehensive_auth_system import ComprehensiveAuthSystem

# Initialize system
auth_system = ComprehensiveAuthSystem()

# Get system status
status = auth_system.get_system_status()

# Run setup
success = auth_system.run_complete_setup()

# Display dashboard
auth_system.display_unified_dashboard()
```

## Best Practices

### Development
1. Always use the comprehensive system for MCP operations
2. Monitor system health regularly
3. Keep API keys secure and rotated
4. Test error recovery scenarios

### Production
1. Set up monitoring and alerting
2. Implement backup and recovery procedures
3. Regular security audits
4. Performance monitoring

### Maintenance
1. Regular health checks
2. Update configurations as needed
3. Monitor audit logs
4. Review and update security measures

## Support and Resources

### Documentation
- [MCP Integration Guide](MCP_INTEGRATION_GUIDE.md)
- [Authentication Setup Guide](AUTHENTICATION_SETUP.md)
- [Error Recovery Documentation](error_recovery_system.py)

### Getting Help
- Check system logs and reports
- Run diagnostic commands with `--verbose`
- Review configuration files
- Contact development team for persistent issues

## Conclusion

The Comprehensive Authentication System provides a robust, secure, and user-friendly solution for managing MCP server authentication in the DocGen CLI project. With real-time monitoring, secure key management, intelligent error recovery, and guided setup, it ensures reliable and secure operation of all MCP integrations.

For additional support or questions, refer to the troubleshooting section or contact the development team.
