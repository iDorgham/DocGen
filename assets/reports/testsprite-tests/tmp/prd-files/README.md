# DocGen CLI

A powerful command-line tool for generating project documentation from specifications using spec-driven development principles.

## Features

- **Interactive CLI Interface**: User-friendly command-line interface with guided prompts and Rich formatting
- **Multi-Document Generation**: Generate technical specifications, project plans, and marketing materials
- **Project Management**: Create, manage, and switch between multiple projects with YAML storage
- **Template-Based**: Uses Jinja2 templates for flexible document generation with custom filters
- **Multiple Output Formats**: Support for Markdown, HTML, and PDF output
- **Professional Templates**: Comprehensive templates for technical specs, project plans, and marketing materials
- **Robust Validation**: Comprehensive input validation and data integrity checks using Pydantic
- **Error Handling**: Advanced error recovery and user guidance with actionable suggestions
- **MCP Integration**: Enhanced development workflow with Byterover, TestSprite, Context7, and Browser Tools
- **Spec-Driven Development**: Automated spec compliance validation and traceable development
- **Quality Assurance**: Automated testing, performance validation, and security checks

## Installation

```bash
pip install docgen-cli
```

## Quick Start

```bash
# Create a new project
python docgen_cli.py create

# Generate documents
python docgen_cli.py spec                    # Technical specification
python docgen_cli.py plan                    # Project plan
python docgen_cli.py marketing               # Marketing materials

# Validate project data
python docgen_cli.py validate                # Validate project data and structure

# Get help
python docgen_cli.py help                    # Show available commands
```

### Advanced Usage (Full CLI)

```bash
# Using the full CLI implementation
python src/cli/main.py project create        # Create new project
python src/cli/main.py project status        # Show project status
python src/cli/main.py project switch        # Switch between projects
python src/cli/main.py project recent        # Show recent projects

# Generate documents with options
python src/cli/main.py generate spec --format html      # HTML output
python src/cli/main.py generate plan --format pdf       # PDF output
python src/cli/main.py generate marketing --format markdown  # Markdown output
python src/cli/main.py generate all                     # Generate all documents

# Advanced features
python src/cli/main.py validate              # Validate project data
python src/cli/main.py error-report          # Generate error reports
```

## Project Structure

```text
DocGen/
├── assets/                     # Project assets and resources
│   ├── data/                   # Data files and samples
│   │   ├── archive/           # Historical documentation
│   │   ├── fixtures/          # Test fixtures
│   │   └── samples/           # Sample project data
│   ├── dev/                    # Development tools and scripts
│   │   ├── config/            # Configuration files
│   │   │   ├── mcp/           # MCP server configurations
│   │   │   ├── setup/         # Setup scripts
│   │   │   └── workflow/      # Workflow configuration
│   │   └── scripts/           # Development scripts
│   ├── docs/                   # Documentation
│   │   ├── developer/         # Developer documentation
│   │   ├── generated/         # Generated documentation
│   │   └── user/              # User documentation
│   ├── management/             # Control panel files
│   │   ├── DASHBOARD.md       # Main development dashboard
│   │   ├── STATUS.md          # Project status
│   │   ├── TASKS.md           # Current tasks
│   │   └── ...                # Other control panel files
│   ├── reports/                # Generated reports and logs
│   │   ├── logs/              # Application logs
│   │   ├── mcp/               # MCP integration reports
│   │   └── workflow/          # Workflow reports
│   ├── specs/                  # Specification documents
│   │   ├── requirements/      # Requirements documents
│   │   ├── technical/         # Technical specifications
│   │   └── contracts/         # API and data contracts
│   └── templates/              # Template specifications
├── src/                        # Source code
│   ├── cli/                    # CLI interface
│   ├── commands/               # CLI commands
│   ├── core/                   # Core functionality
│   ├── models/                 # Data models
│   ├── templates/              # Jinja2 templates
│   └── utils/                  # Utility functions
├── test_project/               # Test project data
├── venv/                       # Virtual environment
├── docgen_cli.py              # Simple CLI entry point
├── pyproject.toml              # Project configuration
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Development

This project follows spec-driven development with clear phases and milestones.

### Phase 1: MVP Foundation ✅ COMPLETED

- ✅ Core infrastructure and project management
- ✅ Document generation engine with Jinja2 templates
- ✅ Basic validation system and error handling
- ✅ Working CLI with project creation and document generation

### Phase 2: Enhancement and Integration 🔄 IN PROGRESS

- 🔄 MCP server integration (Byterover, TestSprite, Context7, Browser Tools)
- 🔄 Comprehensive testing framework and quality assurance
- 🔄 Advanced error handling and user experience improvements
- 🔄 Documentation and release preparation

### Phase 3: Advanced Features 📋 PLANNED

- 📋 Advanced template system with inheritance
- 📋 Git integration and version control
- 📋 Plugin architecture and extensibility
- 📋 Enterprise features and integrations

## MCP Integration

DocGen CLI integrates with multiple MCP servers for enhanced development workflow:

- **Byterover MCP**: Knowledge management and project planning
- **TestSprite MCP**: Automated testing and quality assurance
- **Context7 MCP**: Library documentation and API reference
- **Browser Tools MCP**: Web testing and quality audits
- **Dart MCP**: Task and project management

### MCP Integration Features

- **Knowledge Management**: Persistent development context and pattern storage
- **Automated Testing**: Comprehensive test plan generation and execution
- **Quality Assurance**: Automated quality validation and performance testing
- **Documentation Access**: Real-time library documentation and best practices
- **Project Management**: Task tracking and progress monitoring

See `assets/dev/config/mcp/MCP_INTEGRATION_GUIDE.md` for comprehensive documentation.

## Quality Assurance

DocGen CLI implements comprehensive quality assurance through:

- **Automated Testing**: Unit tests, integration tests, and end-to-end testing
- **Code Quality**: Linting, formatting, and type checking with Black, isort, flake8, and mypy
- **Performance Testing**: Document generation performance validation (< 5 seconds)
- **Security Validation**: Input sanitization and security vulnerability scanning
- **Accessibility Testing**: HTML output accessibility validation
- **Cross-Platform Testing**: Windows, Linux, and macOS compatibility

### Quality Gates

- **Test Coverage**: Minimum 80% test coverage requirement
- **Performance**: Document generation < 5 seconds, project switching < 1 second
- **Security**: No critical vulnerabilities, input validation for all user inputs
- **Code Quality**: All linting checks passing, type hints for all functions
- **Documentation**: Complete API documentation and user guides

## License

MIT License
