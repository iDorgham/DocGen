# DocGen CLI - Architecture Documentation

## Overview

This document provides a comprehensive overview of the DocGen CLI project architecture, including detailed descriptions of the system design, component relationships, and implementation patterns.

## Current Project Structure

```text
DocGen/
├── assets/                    # Project assets and resources
│   ├── contracts/                     # API and data contracts
│   │   ├── api_contracts.md          # API endpoint contracts
│   │   ├── data_contracts.md         # Data structure contracts
│   │   └── template_contracts.md     # Template contracts
│   ├── data/                         # Sample data files
│   │   ├── sample_project_data.yaml  # Sample project data
│   │   ├── simple_risks.yaml         # Simple risk data
│   │   └── temp_risks.yaml           # Temporary risk data
│   ├── docs/                         # Documentation
│   │   ├── archive/                  # Historical documentation
│   │   │   ├── PHASE2_WEEK2_SUMMARY.md
│   │   │   ├── REORGANIZATION_SUMMARY.md
│   │   │   ├── SPEC_DRIVEN_DEVELOPMENT_PLAN.md
│   │   │   └── SPEC_VALIDATION_CHECKLIST.md
│   │   ├── generated/                # Generated documentation
│   │   │   ├── marketing.md          # Generated marketing docs
│   │   │   ├── project_plan.md       # Generated project plan
│   │   │   └── technical_spec.md     # Generated technical spec
│   │   ├── COMMANDS_REFERENCE.md     # CLI commands reference
│   │   ├── DEVELOPER_QUICK_REFERENCE.md
│   │   ├── PROJECT_ORGANIZATION_SUMMARY.md
│   │   ├── PROJECT_REORGANIZATION_SUMMARY.md
│   │   └── PROJECT_STRUCTURE.md      # This file
│   ├── mcp/                          # MCP server configurations
│   │   ├── MCP_DEVELOPMENT_RULES.md
│   │   ├── MCP_IMPLEMENTATION_GUIDE.md
│   │   ├── MCP_INTEGRATION_RULES.md
│   │   ├── MCP_SERVER_SPECIFICATIONS.md
│   │   └── MCP_SERVERS_GUIDE.md
│   ├── memory/                       # Project memory and constitution
│   │   ├── constitution.md           # Project constitution
│   │   └── constitution_update_checklist.md
│   ├── scripts/                      # Development scripts and tools
│   │   ├── generate_docs.py          # Documentation generator
│   │   ├── setup_dev.sh              # Development setup script
│   │   ├── tests/                    # Test files
│   │   │   ├── commands/             # Command tests
│   │   │   ├── models/               # Model tests
│   │   │   │   ├── test_document.py
│   │   │   │   ├── test_project.py
│   │   │   │   └── test_template.py
│   │   │   ├── templates/            # Template tests
│   │   │   ├── utils/                # Utility tests
│   │   │   │   └── test_validation.py
│   │   │   ├── test_generator.py
│   │   │   ├── test_new_structure.py
│   │   │   ├── test_project_manager.py
│   │   │   ├── test_template_manager.py
│   │   │   └── test_validation.py
│   │   └── tools/                    # Development tools
│   │       ├── continuous_validation.py
│   │       ├── doc_sync_validator.py
│   │       ├── quality_assurance.py
│   │       └── spec_validator.py
│   ├── specs/                        # Specification documents
│   │   ├── requirements.md           # Project requirements
│   │   ├── tasks.md                  # Task specifications
│   │   └── tech.md                   # Technical specifications
│   └── templates/                    # Template specifications
│       ├── agent-file-template.md
│       ├── plan-template.md
│       ├── spec-template.md
│       └── tasks-template.md
├── src/                              # Source code
│   ├── cli/                          # CLI interface
│   │   ├── __init__.py
│   │   └── main.py                   # Main CLI entry point
│   ├── commands/                     # CLI commands
│   │   ├── __init__.py
│   │   ├── generate.py               # Generate command
│   │   ├── project.py                # Project management command
│   │   └── validate.py               # Validation command
│   ├── core/                         # Core functionality
│   │   ├── __init__.py
│   │   ├── error_handler.py          # Error handling
│   │   ├── generator.py              # Document generator
│   │   ├── git_manager.py            # Git integration
│   │   ├── project_manager.py        # Project management
│   │   ├── template_manager.py       # Template management
│   │   └── validation.py             # Validation logic
│   ├── models/                       # Data models
│   │   ├── __init__.py
│   │   ├── document.py               # Document model
│   │   ├── error_handler.py          # Error model
│   │   ├── project.py                # Project model
│   │   └── template.py               # Template model
│   ├── templates/                    # Jinja2 templates
│   │   ├── marketing.j2              # Marketing template
│   │   ├── marketing_loose.j2        # Loose marketing template
│   │   ├── plan.j2                   # Plan template
│   │   ├── project_plan.j2           # Project plan template
│   │   ├── spec.j2                   # Specification template
│   │   └── technical_spec.j2         # Technical spec template
│   ├── utils/                        # Utility functions
│   │   ├── __init__.py
│   │   ├── file_io.py                # File I/O utilities
│   │   ├── formatting.py             # Formatting utilities
│   │   └── validation.py             # Validation utilities
│   ├── __init__.py
│   ├── __main__.py                   # Package entry point
│   ├── cli_main.py                   # CLI main module
│   └── generate_docs.py              # Documentation generator
├── venv/                             # Virtual environment
├── pyproject.toml                    # Project configuration
├── requirements.txt                  # Python dependencies
└── README.md                         # Project README
```

## Directory Descriptions

### R
oot Directory

The root directory contains the essential project files and configuration:

- **`pyproject.toml`**: Project configuration file defining package metadata, dependencies, and build settings

- **`requirements.txt`**: Python package dependencies list

- **`README.md`**: Project overview and documentation

- **`venv/`**: Python virtual environment (excluded from version control)


### `
assets/` Directory

This directory contains all project assets, resources, and supporting files:

#### `contracts/`
- **Purpose**: API and data contracts defining interfaces and data structures

- **Files**:

  - `api_contracts.md`: API endpoint contracts and specifications
  - `data_contracts.md`: Data structure contracts and schemas
  - `template_contracts.md`: Template contracts and specifications

#### `data/`
- **Purpose**: Sample data files for testing and development

- **Files**:

  - `sample_project_data.yaml`: Sample project data for testing
  - `simple_risks.yaml`: Simple risk data examples
  - `temp_risks.yaml`: Temporary risk data for development

#### `docs/`
- **Purpose**: Project documentation and generated content

- **Subdirectories**:

  - `archive/`: Historical documentation and summaries
  - `generated/`: Auto-generated documentation files
- **Files**: Various markdown documentation files


#### `mcp/`
- **Purpose**: MCP (Model Context Protocol) server configurations and rules

- **Files**: MCP development rules, implementation guides, and server specifications


#### `memory/`
- **Purpose**: Project memory, constitution, and persistent knowledge

- **Files**: Project constitution and update checklists


#### `scripts/`
- **Purpose**: Development scripts, tools, and test files

- **Subdirectories**:

  - `tests/`: Test files organized by module
  - `tools/`: Development and validation tools

#### `specs/`
- **Purpose**: Project specifications and requirements

- **Files**: Requirements, tasks, and technical specifications


#### `templates/`
- **Purpose**: Template specifications and documentation templates

- **Files**: Various template specification files


### `
src/` Directory

The source code directory contains all application code:

#### `cli/`
- **Purpose**: Command-line interface implementation

- **Files**: Main CLI entry point and interface code


#### `commands/`
- **Purpose**: Individual CLI command implementations

- **Files**: Generate, project management, and validation commands


#### `core/`
- **Purpose**: Core application functionality

- **Files**: Document generation, project management, template handling, and validation


#### `models/`
- **Purpose**: Data models and structures

- **Files**: Document, project, template, and error models


#### `templates/`
- **Purpose**: Jinja2 templates for document generation

- **Files**: Various document templates (marketing, plans, specifications)


#### `utils/`
- **Purpose**: Utility functions and helpers

- **Files**: File I/O, formatting, and validation utilities


## File Relationships

### I
mport Dependencies

```text
src/
├── cli/main.py → commands/* → core/* → models/* → utils/*
├── commands/* → core/* → models/* → utils/*
├── core/* → models/* → utils/*
└── models/* → utils/*
```

### T
emplate Usage

```text
src/templates/ → core/template_manager.py → commands/generate.py
```

### D
ata Flow

```text
assets/data/ → src/models/ → src/core/generator.py → src/templates/
```

## Development Workflow

### 1
. Specification-Driven Development
- Specifications in `assets/specs/`

- Requirements drive implementation in `src/`

- Documentation generated in `assets/docs/generated/`


### 2
. Testing
- Test files in `assets/dev/scripts/tests/`

- Tests organized by module structure

- Continuous validation tools in `assets/dev/scripts/tools/`


### 3
. Documentation
- Source documentation in `assets/docs/`

- Generated documentation in `assets/docs/generated/`

- Historical documentation in `assets/docs/archive/`


## Best Practices

### 1
. File Organization
- Keep related files together

- Use clear, descriptive names

- Follow Python package conventions


### 2
. Import Structure
- Use relative imports within packages

- Avoid circular dependencies

- Keep imports at the top of files


### 3
. Documentation
- Update documentation with code changes

- Use consistent formatting

- Keep generated docs separate from source docs


### 4
. Testing
- Write tests for all new functionality

- Keep tests organized by module

- Use descriptive test names


## Maintenance

### R
egular Tasks
- Update documentation when structure changes

- Clean up temporary files

- Validate import paths

- Update this structure document


### V
alidation
- Run tests regularly

- Check import paths

- Validate template rendering

- Ensure documentation is current


## Notes

- The `venv/` directory is excluded from version control

- All `__pycache__/` directories are excluded from version control

- The structure follows Python packaging best practices

- Documentation is kept separate from source code

- Tests are organized to mirror the source structure


This structure supports the project's spec-driven development approach and provides clear separation of concerns for maintainability and scalability.
