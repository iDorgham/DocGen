# Contributing to DocGen CLI

Thank you for your interest in contributing to DocGen CLI! This document provides guidelines and information for contributors.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Development Workflow](#development-workflow)
- [Testing Guidelines](#testing-guidelines)
- [Documentation Guidelines](#documentation-guidelines)
- [Code Style](#code-style)
- [Pull Request Process](#pull-request-process)
- [Release Process](#release-process)

## 🤝 Code of Conduct

This project adheres to a code of conduct that we expect all contributors to follow. Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## 🚀 Getting Started

### Prerequisites

Before contributing, ensure you have:

- **Python 3.8+** installed
- **Git** for version control
- **Virtual environment** (recommended)
- **Basic understanding** of Python, CLI tools, and documentation generation

### Ways to Contribute

- **🐛 Bug Reports**: Report issues and bugs
- **✨ Feature Requests**: Suggest new features and improvements
- **📝 Documentation**: Improve documentation and examples
- **🧪 Testing**: Add tests and improve test coverage
- **🔧 Code**: Contribute code improvements and new features
- **🎨 Templates**: Create new document templates
- **🌍 Localization**: Help with translations and internationalization

## 🛠️ Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/docgen-cli.git
cd docgen-cli

# Add upstream remote
git remote add upstream https://github.com/docgen-cli/docgen-cli.git
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install in development mode with all dependencies
pip install -e ".[dev,test,docs,performance]"

# Install pre-commit hooks
pre-commit install
```

### 4. Verify Installation

```bash
# Run tests to verify everything works
pytest tests/ -v

# Check CLI works
docgen --help
```

## 📝 Contributing Guidelines

### Issue Guidelines

Before creating an issue:

1. **Search existing issues** to avoid duplicates
2. **Use clear, descriptive titles**
3. **Provide detailed information**:
   - **Bug reports**: Steps to reproduce, expected vs actual behavior
   - **Feature requests**: Use case, proposed solution, alternatives considered
4. **Include relevant labels** when creating issues

### Pull Request Guidelines

Before submitting a pull request:

1. **Create a feature branch** from `main`
2. **Make focused changes** - one feature/fix per PR
3. **Write clear commit messages** following conventional commits
4. **Add tests** for new functionality
5. **Update documentation** as needed
6. **Ensure all checks pass**

## 🔄 Development Workflow

### Branch Strategy

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Or bugfix branch
git checkout -b bugfix/issue-number-description

# Or documentation branch
git checkout -b docs/update-user-guide
```

### Commit Message Format

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(cli): add support for custom output formats
fix(validation): resolve YAML parsing error for nested objects
docs(api): update command reference with new options
test(core): add unit tests for template engine
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

# Security scanning
safety check
bandit -r src/

# Documentation
mkdocs serve
```

## 🧪 Testing Guidelines

### Test Structure

```
tests/
├── unit/           # Unit tests for individual components
├── integration/    # Integration tests for workflows
├── cli/           # CLI command tests
├── fixtures/      # Test data and fixtures
└── conftest.py    # Pytest configuration
```

### Writing Tests

#### Unit Tests
```python
def test_template_rendering():
    """Test template rendering with valid data."""
    template = TemplateManager()
    data = {"project": {"name": "Test Project"}}
    result = template.render("spec.j2", data)
    assert "Test Project" in result
    assert "Technical Specification" in result
```

#### Integration Tests
```python
def test_full_workflow():
    """Test complete document generation workflow."""
    # Create test project
    # Generate documents
    # Validate output
    # Clean up
```

#### CLI Tests
```python
def test_create_command():
    """Test project creation command."""
    result = runner.invoke(cli, ["create", "test-project"])
    assert result.exit_code == 0
    assert "Project created successfully" in result.output
```

### Test Requirements

- **Coverage**: Minimum 80% test coverage
- **Naming**: Descriptive test names that explain what is being tested
- **Isolation**: Tests should be independent and not affect each other
- **Cleanup**: Tests should clean up after themselves
- **Documentation**: Complex tests should include docstrings

### Running Tests

```bash
# Run all tests
pytest

# Run specific test types
pytest tests/unit/
pytest tests/integration/
pytest tests/cli/

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/unit/test_template_manager.py::test_render_template

# Run with verbose output
pytest -v

# Run with parallel execution
pytest -n auto
```

## 📚 Documentation Guidelines

### Documentation Structure

```
docs/
├── user/           # User-facing documentation
├── developer/      # Developer documentation
├── api/           # API reference
└── examples/      # Usage examples
```

### Writing Documentation

#### User Documentation
- **Clear and concise** language
- **Step-by-step instructions** with examples
- **Screenshots** where helpful
- **Troubleshooting** sections

#### Developer Documentation
- **Code examples** with explanations
- **Architecture diagrams** where appropriate
- **API documentation** with type hints
- **Contributing guidelines** and workflows

#### API Documentation
- **Complete function signatures** with type hints
- **Parameter descriptions** and examples
- **Return value documentation**
- **Exception documentation**

### Documentation Commands

```bash
# Build documentation
mkdocs build

# Serve documentation locally
mkdocs serve

# Deploy documentation
mkdocs gh-deploy
```

## 🎨 Code Style

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line length**: 88 characters (Black default)
- **Import sorting**: isort configuration
- **Type hints**: Required for all functions
- **Docstrings**: Google style docstrings

### Code Formatting

```bash
# Format code with Black
black src/ tests/

# Sort imports with isort
isort src/ tests/

# Check formatting
black --check src/ tests/
isort --check-only src/ tests/
```

### Linting

```bash
# Run flake8
flake8 src/ tests/

# Run mypy for type checking
mypy src/

# Run all linting
pre-commit run --all-files
```

### Code Quality Tools

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **pre-commit**: Git hooks for quality checks

## 🔄 Pull Request Process

### Before Submitting

1. **Ensure tests pass**:
   ```bash
   pytest tests/ -v
   ```

2. **Check code quality**:
   ```bash
   black --check src/ tests/
   isort --check-only src/ tests/
   flake8 src/ tests/
   mypy src/
   ```

3. **Update documentation** if needed

4. **Add changelog entry** for significant changes

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Changelog updated
```

### Review Process

1. **Automated checks** must pass
2. **Code review** by maintainers
3. **Testing** in different environments
4. **Documentation review**
5. **Approval** and merge

## 🚀 Release Process

### Version Numbering

We use [Semantic Versioning](https://semver.org/):
- **MAJOR**: Incompatible API changes
- **MINOR**: Backwards-compatible functionality additions
- **PATCH**: Backwards-compatible bug fixes

### Release Steps

1. **Update version** in `pyproject.toml`
2. **Update changelog** with new features/fixes
3. **Create release branch** from `main`
4. **Run full test suite**
5. **Create GitHub release**
6. **Publish to PyPI**
7. **Update documentation**

### Release Commands

```bash
# Update version
bump2version patch  # or minor, major

# Run deployment script
python scripts/deploy.py --publish

# Create GitHub release
gh release create v1.0.0 --generate-notes
```

## 🆘 Getting Help

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and community discussion
- **Email**: dev@docgen.dev for private matters

### Resources

- **Documentation**: [User Guide](USER_GUIDE.md), [API Reference](API_REFERENCE.md)
- **Examples**: [Example Projects](examples/)
- **Templates**: [Template Guide](docs/templates.md)

## 🏆 Recognition

Contributors are recognized in:
- **README.md** contributors section
- **CHANGELOG.md** for significant contributions
- **GitHub contributors** page
- **Release notes** for major contributions

## 📄 License

By contributing to DocGen CLI, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to DocGen CLI! Your contributions help make this project better for everyone. 🎉
