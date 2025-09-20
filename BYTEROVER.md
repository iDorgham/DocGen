# Byterover Handbook

*Generated: 2025-01-27*

## Layer 1: System Overview

**Purpose**: DocGen CLI is a powerful command-line tool for generating project documentation from specifications using spec-driven development principles. It provides an interactive CLI interface for creating technical specifications, project plans, and marketing materials from structured project data.

**Tech Stack**: 
- **Core Language**: Python 3.8+
- **CLI Framework**: Click 8.0+ for command-line interface
- **Templating**: Jinja2 3.0+ for document generation
- **Data Handling**: PyYAML 6.0+ for YAML processing
- **UI/UX**: Rich 13.0+ for beautiful console output
- **Validation**: Pydantic 2.0+ for data validation
- **Testing**: pytest 7.0+ with coverage reporting
- **Code Quality**: Black, isort, flake8, mypy for linting and formatting
- **MCP Integration**: Byterover, TestSprite, Context7, Browser Tools, Playwright, Dart

**Architecture**: Layered CLI Architecture with modular command structure
- **CLI Layer**: Click-based command interface with Rich formatting
- **Core Layer**: Document generation, project management, validation, error handling
- **Models Layer**: Pydantic data models for project and template structures
- **Utils Layer**: File I/O, formatting, and validation utilities
- **Templates Layer**: Jinja2 templates for document generation
- **MCP Integration**: Multiple MCP servers for enhanced development workflow

**Key Technical Decisions**:
- Spec-driven development approach with clear phases and milestones
- Modular CLI architecture with separate command modules
- Comprehensive error handling with user-friendly messages
- MCP server integration for enhanced development workflow
- Template-based document generation with Jinja2
- YAML-based project data storage with validation
- Rich console output for improved user experience

**Entry Points**: 
- `src/cli/main.py` - Main CLI entry point with Click commands
- `docgen_cli.py` - Simple CLI entry point for basic functionality
- `src/__main__.py` - Package entry point

---

## Layer 2: Module Map

**Core Modules**:
- **ProjectManager** (`src/core/project_manager.py`): Manages project creation, switching, and data persistence
- **DocumentGenerator** (`src/core/generator.py`): Handles document generation from templates and project data
- **TemplateManager** (`src/core/template_manager.py`): Manages Jinja2 templates and rendering
- **InputValidator** (`src/core/validation.py`): Comprehensive input validation and data integrity checks
- **ErrorHandler** (`src/core/error_handler.py`): Advanced error recovery and user guidance
- **GitManager** (`src/core/git_manager.py`): Git integration for version control

**Data Layer**:
- **ProjectModel** (`src/models/project_model.py`): Pydantic models for project data structure
- **TemplateModel** (`src/models/template_model.py`): Pydantic models for template metadata
- **Project Data**: YAML files storing project information and configuration
- **Template Data**: Jinja2 templates in `src/templates/` directory

**Integration Points**:
- **MCP Commands** (`src/commands/mcp.py`): MCP server integration commands
- **CLI Commands** (`src/commands/`): Modular command structure for different functionalities
- **Project Commands** (`src/commands/project.py`): Project management commands
- **Generate Commands** (`src/commands/generate.py`): Document generation commands
- **Validate Commands** (`src/commands/validate.py`): Validation commands

**Utilities**:
- **FileIO** (`src/utils/file_io.py`): File operations with proper error handling
- **Formatting** (`src/utils/formatting.py`): Document formatting utilities
- **Validation** (`src/utils/validation.py`): Input validation utilities

**Module Dependencies**:
- CLI Layer depends on Core Layer for business logic
- Core Layer depends on Models Layer for data structures
- All layers depend on Utils Layer for common functionality
- MCP integration provides external service connectivity

---

## Layer 3: Integration Guide

**API Endpoints**:
- **CLI Commands**: Click-based command interface with subcommands
  - `docgen create` - Create new project
  - `docgen spec` - Generate technical specification
  - `docgen plan` - Generate project plan
  - `docgen marketing` - Generate marketing materials
  - `docgen validate` - Validate project data
  - `docgen project` - Project management commands
  - `docgen template` - Template management commands
  - `docgen git` - Git integration commands
  - `docgen mcp` - MCP server integration commands

**Configuration Files**:
- **pyproject.toml**: Project configuration, dependencies, and build settings
- **requirements.txt**: Python dependencies for quick setup
- **pytest.ini**: Test configuration and coverage settings
- **.env**: Environment variables for MCP server API keys
- **project_data.yaml**: Project-specific data and configuration

**External Integrations**:
- **MCP Servers**: Byterover (knowledge management), TestSprite (testing), Context7 (documentation), Browser Tools (web testing), Playwright (browser automation), Dart (project management)
- **Git Integration**: Version control for project documents and data
- **Template System**: Jinja2 templates for flexible document generation
- **File System**: YAML-based project data storage and management

**Workflows**:
- **Project Creation**: Interactive project setup with validation
- **Document Generation**: Template-based document creation with multiple output formats
- **Project Management**: Project switching, status tracking, and data persistence
- **MCP Integration**: Enhanced development workflow with external services
- **Quality Assurance**: Automated testing, validation, and error handling

**Interface Definitions**:
- **CLI Interface**: Click-based command structure with Rich formatting
- **Data Models**: Pydantic models for type-safe data handling
- **Template Interface**: Jinja2 template system with custom filters
- **MCP Interface**: Standardized MCP server communication protocols

---

## Layer 4: Extension Points

**Design Patterns**:
- **Command Pattern**: Click-based CLI commands with modular structure
- **Template Method Pattern**: Jinja2 template inheritance and customization
- **Strategy Pattern**: Multiple output formats (Markdown, HTML, PDF)
- **Factory Pattern**: Document generation with different template types
- **Observer Pattern**: Error handling and user feedback systems
- **Repository Pattern**: Project data persistence and management

**Extension Points**:
- **Custom Templates**: Add new Jinja2 templates in `src/templates/`
- **Custom Commands**: Extend CLI with new Click commands
- **Custom Validators**: Add new validation rules in `src/core/validation.py`
- **Custom Output Formats**: Extend document generation with new formats
- **MCP Server Integration**: Add new MCP servers for enhanced functionality
- **Custom Error Handlers**: Extend error handling with new recovery strategies

**Customization Areas**:
- **Template Customization**: Modify Jinja2 templates for different document styles
- **Project Data Structure**: Extend YAML schema for additional project information
- **CLI Commands**: Add new commands for specific use cases
- **Validation Rules**: Customize input validation for specific requirements
- **Output Formatting**: Customize document formatting and styling
- **MCP Integration**: Configure and customize MCP server interactions

**Plugin Architecture**:
- **Template Plugins**: Load custom templates from external sources
- **Command Plugins**: Extend CLI with plugin-based commands
- **Validator Plugins**: Add custom validation rules as plugins
- **Output Plugins**: Extend output formats with plugin system
- **MCP Plugins**: Integrate additional MCP servers as plugins

**Recent Changes**:
- **Phase 2 Completion**: MCP integration and testing framework implementation
- **Assets Reorganization**: Consolidated project structure with `assets/` directory
- **CLI Refactoring**: Modular command structure with separate modules
- **Template Consolidation**: Moved all templates to `src/templates/`
- **Quality Assurance**: Comprehensive testing and validation framework
- **Documentation Updates**: Complete project documentation and user guides

---

*Byterover handbook optimized for agent navigation and human developer onboarding*
