# 🚀 DocGen CLI Quick Start Guide

> **Get up and running with DocGen CLI in minutes**

## ⚡ 5-Minute Setup

### 1. Prerequisites
- **Python 3.8+** installed
- **Git** for version control
- **Terminal/Command Prompt** access

### 2. Environment Setup
```bash
# Clone the repository (if not already done)
git clone <repository-url>
cd DocGen

# Run quick setup script
python assets/dev/scripts/quick_dev_setup.py
```

### 3. Verify Installation
```bash
# Test the CLI
python src/cli_main.py --help

# Run basic tests
python assets/dev/scripts/run_quality_checks.py
```

### 4. Generate Your First Document
```bash
# Generate project documentation
python assets/dev/scripts/generate_docs.py

# Check generated files
ls assets/docs/generated/
```

## 🎯 Common Tasks

### 📝 Generate Documentation
```bash
# Generate all documents
python assets/dev/scripts/generate_docs.py

# Generate specific document types
python src/cli_main.py generate --type technical
python src/cli_main.py generate --type marketing
python src/cli_main.py generate --type project-plan
```

### 🧪 Run Tests
```bash
# Run all tests
python -m pytest assets/dev/tests/ -v

# Run with coverage
python -m pytest assets/dev/tests/ --cov=src --cov-report=html

# Run quality checks
python assets/dev/scripts/run_quality_checks.py
```

### 🔧 Development Workflow
```bash
# Start development session
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run project monitoring
python assets/dev/scripts/project_monitoring.py

# Check project health
python assets/dev/scripts/dev_helpers.py
```

### 📊 MCP Integration
```bash
# Run MCP integration
python assets/dev/scripts/run_mcp_integration.py

# Check MCP server status
python assets/dev/scripts/run_mcp_integration.py --status
```

## 🛠️ Development Tools

### 📁 Essential Scripts
| Script | Purpose | Usage |
|--------|---------|-------|
| `quick_dev_setup.py` | Environment setup | `python assets/dev/scripts/quick_dev_setup.py` |
| `dev_helpers.py` | Project analysis | `python assets/dev/scripts/dev_helpers.py` |
| `generate_docs.py` | Document generation | `python assets/dev/scripts/generate_docs.py` |
| `project_monitoring.py` | Health monitoring | `python assets/dev/scripts/project_monitoring.py` |
| `run_quality_checks.py` | Quality assurance | `python assets/dev/scripts/run_quality_checks.py` |
| `workflow_automation.py` | Workflow automation | `python assets/dev/scripts/workflow_automation.py` |
| `run_all_scripts.py` | Run all scripts | `python assets/dev/scripts/run_all_scripts.py` |

### 🔧 Configuration Files
- **MCP Config**: `assets/config/mcp/mcp_config.yaml`
- **Workflow Config**: `assets/config/workflow/workflow.yaml`
- **Project Config**: `pyproject.toml`
- **Dependencies**: `requirements.txt`

## 📚 Documentation Structure

### 📖 User Documentation
- [Commands Reference](documentation/user/commands.md)
- [Template Guide](templates/README.md)
- [Configuration Guide](config/README.md)

### 👨‍💻 Developer Documentation
- [Architecture Guide](documentation/developer/architecture.md)
- [Development Guide](documentation/developer/development.md)
- [API Reference](documentation/developer/quick-reference.md)

### 📋 Specifications
- [Requirements](specifications/requirements/requirements.md)
- [Technical Specs](specifications/technical/technical.md)
- [Quality Standards](specifications/quality_assurance.md)

## 🎛️ Control Panel

### 📊 Dashboard
Access the main control panel at: [DASHBOARD.md](DASHBOARD.md)

### 🔍 Project Health
```bash
# Check project health
python assets/dev/scripts/project_monitoring.py

# View health report
cat assets/reports/project_monitoring_report.json
```

### 📈 Quality Metrics
```bash
# Run quality checks
python assets/dev/scripts/run_quality_checks.py

# View quality report
cat assets/reports/quality_check_report.json
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Add src to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Or use the development script
python assets/dev/scripts/quick_dev_setup.py
```

#### 2. Missing Dependencies
```bash
# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black isort flake8 mypy bandit
```

#### 3. Template Errors
```bash
# Check template files
ls src/templates/

# Validate templates
python assets/dev/scripts/dev_helpers.py --check-templates
```

#### 4. MCP Server Issues
```bash
# Check MCP configuration
cat assets/config/mcp/mcp_config.yaml

# Test MCP integration
python assets/dev/scripts/run_mcp_integration.py --test
```

### Getting Help

#### 📚 Documentation
- [Control Panel](DASHBOARD.md) - Main dashboard
- [Development Guide](documentation/developer/development.md) - Detailed development info
- [Architecture Guide](documentation/developer/architecture.md) - System architecture

#### 🔧 Scripts
- `dev_helpers.py` - Project analysis and utilities
- `project_monitoring.py` - Health monitoring and diagnostics
- `run_quality_checks.py` - Quality assurance and validation

#### 📊 Reports
- Check `assets/reports/` for detailed execution reports
- Review error logs in `assets/logs/`
- Examine configuration in `assets/config/`

## 🎯 Next Steps

### After Setup
1. **Explore the Control Panel**: [DASHBOARD.md](DASHBOARD.md)
2. **Run Development Checklist**: [CHECKLIST.md](CHECKLIST.md)
3. **Review Architecture**: [documentation/developer/architecture.md](documentation/developer/architecture.md)
4. **Start Development**: Use the development workflow

### Development Workflow
1. **Morning**: Check project health and run tests
2. **Development**: Use MCP integration for context-aware coding
3. **Quality Gates**: Run quality checks before committing
4. **Evening**: Generate reports and update documentation

### Learning Path
1. **Basic Usage**: Generate documents and run tests
2. **Development**: Understand the codebase and architecture
3. **Advanced**: Use MCP integration and workflow automation
4. **Expert**: Contribute to the project and extend functionality

---

## 🎛️ Quick Commands Reference

```bash
# Setup
python assets/dev/scripts/quick_dev_setup.py

# Development
python assets/dev/scripts/dev_helpers.py
python assets/dev/scripts/project_monitoring.py

# Quality
python assets/dev/scripts/run_quality_checks.py
python assets/dev/scripts/workflow_automation.py

# Documentation
python assets/dev/scripts/generate_docs.py

# Integration
python assets/dev/scripts/run_mcp_integration.py

# All-in-one
python assets/dev/scripts/run_all_scripts.py
```

---

*Quick Start Guide v1.0 | Last updated: 2025-01-27*
