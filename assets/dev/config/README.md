# DocGen CLI Configuration Directory

This directory contains comprehensive configuration files for the DocGen CLI project, covering all aspects of development, testing, quality assurance, deployment, and workflow automation.

## 📁 Configuration Files

### Core Configuration Files

#### `development.yaml`
**Purpose**: Development environment and workflow settings
- **Python Environment**: Version requirements, virtual environment setup
- **Code Quality**: Formatting, linting, type checking configuration
- **CLI Configuration**: Entry points, command structure
- **Template Configuration**: Supported formats, directories
- **IDE Configuration**: VSCode and Cursor settings
- **Performance & Security**: Resource limits, security settings

#### `testing.yaml`
**Purpose**: Comprehensive testing strategy and configuration
- **Test Framework**: Pytest configuration with plugins
- **Test Structure**: Unit, integration, E2E test organization
- **Coverage Configuration**: Coverage targets and exclusions
- **Test Execution**: Parallel execution, test discovery
- **Performance Testing**: Benchmarks and load testing
- **CI/CD Integration**: GitHub Actions, quality gates

#### `quality.yaml`
**Purpose**: Quality assurance standards and validation rules
- **Code Quality**: Python standards, formatting, linting, type checking
- **Security Standards**: Input validation, output sanitization, dependencies
- **Performance Standards**: Response times, resource limits, scalability
- **Accessibility Standards**: WCAG compliance, CLI accessibility
- **Documentation Standards**: Code docs, API docs, user docs
- **Quality Gates**: Pre-commit, pre-push, pre-release validation

#### `deployment.yaml`
**Purpose**: Deployment strategies and environment configurations
- **Environments**: Development, testing, staging, production
- **Package Distribution**: PyPI, GitHub releases, Docker
- **Build Configuration**: Python build system, artifacts
- **Installation Methods**: PyPI, development, system installation
- **Monitoring & Logging**: Application logging, error tracking
- **Security & Updates**: Package signing, dependency security

#### `workflow.yaml`
**Purpose**: Complete development workflow and automation
- **Development Phases**: Setup, development, testing, deployment
- **Daily Workflow**: Morning setup, development sessions, end-of-day
- **Feature Workflow**: Planning, implementation, testing, documentation
- **Git Workflow**: Branching strategy, commit format, PR process
- **Automation**: CI/CD, scheduled tasks, monitoring
- **Collaboration**: Code review, communication, maintenance

### MCP Integration Configuration

#### `mcp/mcp_config.yaml`
**Purpose**: Model Context Protocol server configuration
- **Server Configuration**: Byterover, TestSprite, Context7, Browser Tools
- **Workflow Settings**: Knowledge-first development, automated testing
- **Quality Gates**: Test coverage, performance, accessibility thresholds
- **Integration Settings**: Parallel execution, caching, error recovery

#### `mcp/` Directory
Contains comprehensive MCP integration documentation:
- **MCP_DEVELOPMENT_RULES.md**: Mandatory development rules
- **MCP_IMPLEMENTATION_GUIDE.md**: Practical implementation guide
- **MCP_INTEGRATION_RULES.md**: Integration rules and patterns
- **MCP_SERVERS_GUIDE.md**: Complete server reference
- **MCP_SERVER_SPECIFICATIONS.md**: Detailed server documentation

### Memory and Constitution

#### `memory/constitution.md`
**Purpose**: Project constitution and core principles
- **Core Principles**: Development standards and guidelines
- **Governance**: Constitution enforcement and amendments
- **Version Control**: Constitution versioning and history

#### `memory/constitution_update_checklist.md`
**Purpose**: Constitution maintenance and consistency
- **Update Checklist**: Required updates when amending constitution
- **Template Sync**: Ensuring consistency across all documentation
- **Validation Steps**: Pre-commit and post-update validation

## 🚀 Quick Start

### 1. Development Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Setup development environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
```

### 2. Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test categories
pytest tests/unit -m unit
pytest tests/integration -m integration
```

### 3. Code Quality Checks
```bash
# Format code
black .
isort .

# Lint code
flake8 src tests

# Type checking
mypy src

# Security scan
bandit -r src
```

### 4. MCP Integration
```bash
# Run complete MCP integration
cd assets/dev/scripts
python run_mcp_integration.py

# Run specific components
python mcp_master_integration.py --component testing
```

## 📊 Configuration Overview

### Quality Gates
- **Test Coverage**: ≥ 80%
- **Performance**: Document generation < 5 seconds
- **Accessibility**: Score ≥ 90
- **Security**: No critical vulnerabilities
- **Code Quality**: Score ≥ 85

### Development Standards
- **Python Version**: ≥ 3.8
- **Code Style**: PEP 8 with Black formatting
- **Type Hints**: Required for all functions
- **Documentation**: Google-style docstrings
- **Testing**: TDD with comprehensive coverage

### Workflow Automation
- **Pre-commit Hooks**: Formatting, linting, type checking
- **Pre-push Hooks**: Full test suite, coverage check
- **CI/CD Pipeline**: Automated testing and deployment
- **MCP Integration**: Knowledge-first development

## 🔧 Customization

### Environment-Specific Configuration
Each configuration file supports environment-specific overrides:

```yaml
# development.yaml
environment:
  development:
    debug_mode: true
    log_level: "DEBUG"
  production:
    debug_mode: false
    log_level: "WARNING"
```

### Quality Gate Adjustment
Modify quality thresholds based on project needs:

```yaml
# quality.yaml
quality_gates:
  coverage_threshold: 85  # Increase from 80%
  performance_threshold: 3  # Decrease from 5 seconds
```

### Workflow Customization
Adapt workflows to team preferences:

```yaml
# workflow.yaml
git_workflow:
  branching:
    main: "production_ready"
    develop: "integration_branch"
    feature: "feature/*"
```

## 📈 Monitoring and Metrics

### Key Metrics Tracked
- **Code Coverage**: Test coverage percentage
- **Performance**: Response times and resource usage
- **Quality Score**: Code quality assessment
- **Security Score**: Vulnerability assessment
- **Documentation Coverage**: Documentation completeness

### Reporting
Configuration files generate comprehensive reports:
- **Test Reports**: HTML, XML, JSON formats
- **Coverage Reports**: Detailed coverage analysis
- **Quality Reports**: Code quality metrics
- **Performance Reports**: Benchmark results

## 🛠️ Maintenance

### Regular Updates
- **Dependencies**: Weekly security and feature updates
- **Configuration**: Monthly review and optimization
- **Documentation**: Continuous updates with code changes
- **Quality Gates**: Quarterly assessment and adjustment

### Configuration Validation
```bash
# Validate all configurations
python -m docgen config validate

# Check configuration consistency
python -m docgen config check
```

## 📚 Best Practices

### Configuration Management
1. **Version Control**: All configurations in version control
2. **Environment Separation**: Clear environment boundaries
3. **Documentation**: Keep configurations well-documented
4. **Validation**: Regular configuration validation
5. **Backup**: Regular configuration backups

### Development Workflow
1. **Knowledge-First**: Always retrieve context before starting
2. **Test-Driven**: Write tests before implementation
3. **Quality Gates**: Never bypass quality checks
4. **Documentation**: Update docs with code changes
5. **Continuous Integration**: Use automated workflows

### MCP Integration
1. **Context Awareness**: Leverage knowledge base
2. **Automated Testing**: Use TestSprite for comprehensive testing
3. **Quality Assurance**: Run browser tools audits
4. **Project Management**: Use Dart for task tracking
5. **Documentation**: Use Context7 for library references

## 🔍 Troubleshooting

### Common Issues
1. **Configuration Conflicts**: Check environment-specific overrides
2. **Quality Gate Failures**: Review thresholds and requirements
3. **MCP Server Issues**: Verify server configuration and connectivity
4. **Test Failures**: Check test environment and dependencies
5. **Build Issues**: Validate build configuration and dependencies

### Support Resources
- **Documentation**: Comprehensive guides in each configuration file
- **MCP Integration**: Detailed MCP server documentation
- **Quality Standards**: Clear quality gate definitions
- **Workflow Guides**: Step-by-step workflow instructions

---

*This configuration directory provides a comprehensive foundation for high-quality, automated development of the DocGen CLI project.*
