# TestSprite API Key Setup Guide

## Overview
This guide will help you configure the TestSprite API key for the DocGen CLI project to enable automated testing capabilities.

## 🚀 Quick Setup

### Step 1: Get Your TestSprite API Key
1. Visit [TestSprite Dashboard](https://www.testsprite.com/dashboard/settings/apikey)
2. Sign in to your TestSprite account
3. Navigate to Settings → API Keys
4. Create a new API key
5. Copy the API key (keep it secure!)

### Step 2: Configure the API Key
Run the setup script to configure your TestSprite API key:

```bash
# Run the TestSprite API setup script
python scripts/setup_testsprite_api.py
```

This script will:
- Prompt you for your TestSprite API key
- Create a `.env` file with the configuration
- Set up the environment variables

### Step 3: Verify Configuration
Test your TestSprite configuration:

```bash
# Test the TestSprite configuration
python scripts/test_testsprite_config.py
```

### Step 4: Run TestSprite Tests
Once configured, run TestSprite tests:

```bash
# Run TestSprite tests
python scripts/run_testsprite_tests.py
```

## 📋 Detailed Setup Instructions

### Manual Setup (Alternative)

If you prefer to set up the API key manually:

1. **Create .env file** in the project root:
   ```bash
   touch .env
   ```

2. **Add your API key** to the .env file:
   ```env
   # TestSprite API Configuration
   TESTSPRITE_API_KEY=your_actual_api_key_here
   
   # Development Configuration
   DEBUG=false
   LOG_LEVEL=INFO
   ```

3. **Restart your terminal/IDE** to load the new environment variables

4. **Verify the setup**:
   ```bash
   echo $TESTSPRITE_API_KEY
   ```

## 🧪 Testing Your Setup

### Test Configuration
```bash
python scripts/test_testsprite_config.py
```

This will test:
- ✅ Environment variables are set
- ✅ TestSprite MCP tools are available
- ✅ API key is valid
- ✅ Project configuration is correct

### Run TestSprite Tests
```bash
python scripts/run_testsprite_tests.py
```

This will run:
- 🚀 Bootstrap tests
- 📊 Code summary generation
- 📋 Test plan generation
- 🧪 Test execution

## 🔧 Troubleshooting

### Common Issues

#### 1. API Key Not Found
**Error**: `TESTSPRITE_API_KEY environment variable not found`

**Solution**:
- Make sure you've created the `.env` file
- Restart your terminal/IDE
- Verify the API key is in the `.env` file

#### 2. Invalid API Key
**Error**: `Please replace the placeholder API key`

**Solution**:
- Replace `your_testsprite_api_key_here` with your actual API key
- Make sure the API key is copied correctly from TestSprite dashboard

#### 3. TestSprite MCP Tools Not Available
**Error**: `TestSprite MCP tools not available`

**Solution**:
- Make sure you're running in the correct environment
- Check if TestSprite MCP server is properly configured
- Verify MCP server is running

#### 4. API Connection Failed
**Error**: `Error testing TestSprite API connection`

**Solution**:
- Check your internet connection
- Verify the API key is valid and active
- Check TestSprite service status

### Getting Help

1. **TestSprite Documentation**: [https://www.testsprite.com/docs](https://www.testsprite.com/docs)
2. **TestSprite Dashboard**: [https://www.testsprite.com/dashboard](https://www.testsprite.com/dashboard)
3. **TestSprite Support**: Contact TestSprite support for API-related issues

## 📊 TestSprite Features

Once configured, TestSprite provides:

### Automated Testing
- **Bootstrap Tests**: Initialize testing environment
- **Code Analysis**: Analyze project structure and code
- **Test Plan Generation**: Generate comprehensive test plans
- **Test Execution**: Run automated tests

### Integration Capabilities
- **MCP Integration**: Seamless integration with MCP servers
- **CI/CD Pipeline**: Integrate with continuous integration
- **Report Generation**: Detailed test reports and analytics
- **Performance Testing**: Automated performance validation

### Test Types
- **Backend Testing**: API and server-side testing
- **Frontend Testing**: UI and user interaction testing
- **Integration Testing**: End-to-end workflow testing
- **Performance Testing**: Load and performance validation

## 🔐 Security Best Practices

### API Key Security
- **Never commit API keys** to version control
- **Use environment variables** for API keys
- **Rotate API keys** regularly
- **Monitor API key usage** in TestSprite dashboard

### Environment Security
- **Keep .env file private** (already in .gitignore)
- **Use different API keys** for different environments
- **Revoke unused API keys** immediately
- **Monitor API access logs** regularly

## 📈 Usage Examples

### Basic Test Execution
```bash
# Run all TestSprite tests
python scripts/run_testsprite_tests.py

# Test specific functionality
python scripts/test_testsprite_config.py
```

### Integration with Development Workflow
```bash
# Run before committing code
python scripts/test_testsprite_config.py && python scripts/run_testsprite_tests.py

# Run in CI/CD pipeline
export TESTSPRITE_API_KEY=$TESTSPRITE_API_KEY
python scripts/run_testsprite_tests.py
```

### Custom Test Configuration
```bash
# Run with specific test scope
python scripts/run_testsprite_tests.py --scope=codebase

# Run with specific test type
python scripts/run_testsprite_tests.py --type=backend
```

## 🎯 Next Steps

After setting up TestSprite:

1. **Explore TestSprite Dashboard**: Familiarize yourself with the interface
2. **Run Initial Tests**: Execute the test suite to understand capabilities
3. **Integrate with Workflow**: Add TestSprite tests to your development process
4. **Customize Tests**: Configure tests for your specific project needs
5. **Monitor Results**: Track test results and improve test coverage

## 📚 Additional Resources

- **TestSprite Documentation**: [https://www.testsprite.com/docs](https://www.testsprite.com/docs)
- **MCP Integration Guide**: `assets/dev/config/mcp/MCP_INTEGRATION_GUIDE.md`
- **TestSprite API Reference**: [https://www.testsprite.com/docs/api](https://www.testsprite.com/docs/api)
- **TestSprite Community**: [https://www.testsprite.com/community](https://www.testsprite.com/community)

## 🆘 Support

If you encounter issues:

1. **Check this guide** for common solutions
2. **Run diagnostic scripts** to identify problems
3. **Check TestSprite status** at [https://www.testsprite.com/status](https://www.testsprite.com/status)
4. **Contact TestSprite support** for API-related issues
5. **Check project documentation** for MCP-specific issues

---

**Note**: This guide assumes you have a valid TestSprite account and API key. If you don't have an account, sign up at [https://www.testsprite.com](https://www.testsprite.com) first.
