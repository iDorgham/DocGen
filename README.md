# DocGen CLI

[![PyPI version](https://badge.fury.io/py/docgen-cli.svg)](https://badge.fury.io/py/docgen-cli)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI/CD](https://github.com/docgen-cli/docgen-cli/workflows/CI%2FCD/badge.svg)](https://github.com/docgen-cli/docgen-cli/actions)
[![Test Coverage](https://codecov.io/gh/docgen-cli/docgen-cli/branch/main/graph/badge.svg)](https://codecov.io/gh/docgen-cli/docgen-cli)

> **A powerful command-line tool for generating professional project documentation from specifications using spec-driven development principles.**

DocGen CLI transforms your project specifications into comprehensive, professional documentation including technical specifications, project plans, and marketing materials. Built with modern Python and following best practices, it's designed for developers, project managers, and teams who need high-quality documentation quickly and consistently.

## ✨ Features

### 🚀 **Core Capabilities**
- **📋 Technical Specifications**: Generate comprehensive technical documentation with architecture, requirements, and implementation details
- **📅 Project Plans**: Create detailed project planning with timelines, resource allocation, and risk management
- **📢 Marketing Materials**: Produce professional marketing content with value propositions and competitive analysis
- **✅ Project Validation**: Comprehensive validation of project data and structure with automatic fixes

### 🎨 **Output Formats**
- **Markdown**: Clean, readable documentation perfect for GitHub and wikis
- **HTML**: Professional web-ready documentation with styling
- **PDF**: Print-ready documents for presentations and reports

### 🛠️ **Developer Experience**
- **Interactive CLI**: User-friendly command-line interface with guided prompts
- **Rich Formatting**: Beautiful console output with progress indicators and colored text
- **Error Recovery**: Advanced error handling with actionable suggestions
- **Cross-Platform**: Full compatibility with Windows, macOS, and Linux

### 🔒 **Quality & Security**
- **Input Validation**: Comprehensive validation using Pydantic models
- **Security Scanning**: Built-in vulnerability scanning with Safety and Bandit
- **Template Security**: Secure template rendering with input sanitization
- **Error Handling**: Robust error recovery and user guidance

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI
pip install docgen-cli

# Or install from source
git clone https://github.com/docgen-cli/docgen-cli.git
cd docgen-cli
pip install -e .
```

### Basic Usage

```bash
# Create a new project
docgen create my-awesome-project
cd my-awesome-project

# Generate documentation
docgen spec          # Technical specification
docgen plan          # Project plan
docgen marketing     # Marketing materials

# Validate your project
docgen validate
```

### Advanced Usage

```bash
# Generate with specific formats
docgen spec --format html --output docs/spec.html
docgen plan --format pdf --output docs/plan.pdf

# Use custom templates
docgen marketing --template custom

# Validate and fix issues automatically
docgen validate --fix
```

## 📚 Documentation

### User Guides
- **[📖 User Guide](USER_GUIDE.md)** - Comprehensive guide for all users
- **[🔧 Installation Guide](INSTALLATION.md)** - Detailed installation instructions
- **[📋 API Reference](API_REFERENCE.md)** - Complete command and option reference

### Developer Resources
- **[🏗️ Architecture Guide](docs/ARCHITECTURE.md)** - Technical architecture and design
- **[🧪 Testing Guide](docs/TESTING.md)** - Testing strategies and best practices
- **[🤝 Contributing Guide](CONTRIBUTING.md)** - How to contribute to the project

### Examples
- **[📁 Example Projects](examples/)** - Real-world project examples
- **[🎯 Use Cases](docs/USE_CASES.md)** - Common use cases and scenarios
- **[🔧 Templates](src/templates/)** - Customizable document templates

## 🏗️ Architecture

DocGen CLI is built with a clean, modular architecture:

```
src/
├── cli/           # Command-line interface
├── commands/      # CLI commands and handlers
├── core/          # Core functionality and business logic
├── models/        # Data models and validation
├── templates/     # Jinja2 document templates
└── utils/         # Utility functions and helpers
```

### Key Components

- **CLI Interface**: Built with Click for professional command-line experience
- **Template Engine**: Jinja2-based templating with custom filters and functions
- **Validation System**: Pydantic models for robust data validation
- **Error Handling**: Comprehensive exception hierarchy with recovery mechanisms

## 🧪 Testing

DocGen CLI includes comprehensive testing:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test types
pytest tests/unit/          # Unit tests
pytest tests/integration/   # Integration tests
pytest tests/cli/           # CLI tests
```

### Test Coverage
- **Unit Tests**: 95%+ coverage of core functionality
- **Integration Tests**: End-to-end workflow testing
- **CLI Tests**: Command-line interface testing
- **Template Tests**: Document generation validation

## 🔧 Development

### Prerequisites
- Python 3.8+
- Git
- Virtual environment (recommended)

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/docgen-cli/docgen-cli.git
cd docgen-cli

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev,test,docs]"

# Install pre-commit hooks
pre-commit install
```

### Development Commands

```bash
# Code formatting
black src/ tests/
isort src/ tests/

# Linting
flake8 src/ tests/
mypy src/

# Testing
pytest tests/ -v
pytest tests/ --cov=src --cov-report=html

# Documentation
mkdocs serve
```

## 🚀 Deployment

### CI/CD Pipeline

DocGen CLI uses GitHub Actions for automated CI/CD:

- **Testing**: Automated testing on multiple Python versions
- **Quality**: Code quality checks with linting and formatting
- **Security**: Security vulnerability scanning
- **Deployment**: Automated deployment to PyPI and Docker Hub

### Docker Support

```bash
# Build development image
docker build -f Dockerfile -t docgen-cli:dev .

# Build production image
docker build -f Dockerfile.prod -t docgen-cli:latest .

# Run with Docker
docker run -v $(pwd):/workspace docgen-cli:latest create my-project
```

## 📊 Performance

### Benchmarks
- **Document Generation**: < 5 seconds for typical projects
- **Memory Usage**: < 50MB for standard operations
- **Startup Time**: < 1 second for CLI initialization
- **Template Rendering**: < 2 seconds for complex documents

### Optimization
- **Parallel Processing**: Multi-threaded operations where applicable
- **Caching**: Template and configuration caching
- **Lazy Loading**: On-demand resource loading
- **Memory Management**: Efficient memory usage with proper cleanup

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Ways to Contribute
- **🐛 Bug Reports**: Report issues and bugs
- **✨ Feature Requests**: Suggest new features and improvements
- **📝 Documentation**: Improve documentation and examples
- **🧪 Testing**: Add tests and improve test coverage
- **🔧 Code**: Contribute code improvements and new features

### Development Process
1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Add** tests for new functionality
5. **Submit** a pull request

## 📄 License

DocGen CLI is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- **Click**: Professional CLI framework
- **Jinja2**: Powerful templating engine
- **Rich**: Beautiful terminal formatting
- **Pydantic**: Data validation and settings
- **pytest**: Testing framework
- **Black**: Code formatting
- **isort**: Import sorting

## 📞 Support

### Getting Help
- **📖 Documentation**: Check our comprehensive guides
- **🐛 Issues**: [Report bugs on GitHub](https://github.com/docgen-cli/docgen-cli/issues)
- **💬 Discussions**: [Join community discussions](https://github.com/docgen-cli/docgen-cli/discussions)
- **📧 Email**: support@docgen.dev

### Community
- **⭐ Star** the repository if you find it useful
- **🐦 Follow** us on Twitter for updates
- **💬 Join** our Discord community
- **📰 Subscribe** to our newsletter

---

<div align="center">

**Made with ❤️ by the DocGen CLI team**

[Website](https://docgen.dev) • [Documentation](https://docs.docgen.dev) • [GitHub](https://github.com/docgen-cli/docgen-cli) • [PyPI](https://pypi.org/project/docgen-cli/)

</div>