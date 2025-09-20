# DocGen CLI Commands Reference

## Overview
This document provides a comprehensive reference for all DocGen CLI commands, organized by functionality and linked to specifications. Each command includes usage examples, validation rules, and traceability to requirements.

## Command Structure

### Simple CLI (docgen_cli.py)
```
python docgen_cli.py [COMMAND] [OPTIONS]
```

### Full CLI (src/cli/main.py)
```
python src/cli/main.py [GROUP] [COMMAND] [OPTIONS] [ARGUMENTS]
```

## Project Management Commands

### `docgen project create`
**Spec Reference**: `requirements.md` - FR-01 (Project Creation and Management)
**Purpose**: Create a new DocGen project with interactive prompts

**Usage**:
```bash
docgen project create [OPTIONS]
```

**Options**:
- `--name, -n TEXT`: Project name
- `--path, -p PATH`: Project directory path
- `--description, -d TEXT`: Project description
- `--skip-validation`: Skip input validation (not recommended)

**Examples**:
```bash
# Interactive creation
docgen project create

# Direct creation with options
docgen project create --name "My Project" --path ./my-project --description "A sample project"
```

**Validation Rules**:
- Project name: 3-50 characters, alphanumeric and spaces only
- Path: Valid directory path, writable by user
- Description: Optional, max 500 characters

**Output**:
- Creates project directory structure
- Generates `project_data.yaml` with default template
- Sets as current project
- Shows success message with next steps

### `docgen project switch`
**Spec Reference**: `requirements.md` - FR-01 (Project Creation and Management)
**Purpose**: Switch to a different project

**Usage**:
```bash
docgen project switch [OPTIONS]
```

**Options**:
- `--project-id TEXT`: Project ID to switch to

**Examples**:
```bash
# Show available projects
docgen project switch

# Switch to specific project
docgen project switch --project-id project_name_1234567890
```

**Validation Rules**:
- Project ID must exist in project registry
- Project directory must exist and be accessible

### `docgen project status`
**Spec Reference**: `requirements.md` - FR-01 (Project Creation and Management)
**Purpose**: Show current project status and information

**Usage**:
```bash
docgen project status [OPTIONS]
```

**Options**:
- `--project-id TEXT`: Specific project ID to show status for

**Examples**:
```bash
# Show current project status
docgen project status

# Show specific project status
docgen project status --project-id project_name_1234567890
```

**Output**:
- Project name, ID, and path
- Creation and last accessed dates
- Directory existence status
- Generated documents count
- Current project indicator

### `docgen project recent`
**Spec Reference**: `requirements.md` - FR-01 (Project Creation and Management)
**Purpose**: Show recently accessed projects

**Usage**:
```bash
docgen project recent
```

**Output**:
- Table of recent projects with names, paths, last accessed dates
- Current project indicator
- Quick access commands

## Document Generation Commands

### `docgen generate spec`
**Spec Reference**: `requirements.md` - FR-02 (Document Generation)
**Purpose**: Generate technical specification document

**Usage**:
```bash
docgen generate spec [OPTIONS]
```

**Options**:
- `--format, -f [markdown|html|pdf]`: Output format (default: markdown)
- `--output, -o PATH`: Output file path
- `--validate-data`: Validate project data before generation

**Examples**:
```bash
# Generate in default format (markdown)
docgen generate spec

# Generate in HTML format
docgen generate spec --format html

# Generate with custom output path
docgen generate spec --output ./docs/my-spec.html --format html

# Generate with data validation
docgen generate spec --validate-data
```

**Validation Rules**:
- Current project must be set
- Project data file must exist and be valid YAML
- Output format must be supported
- Output path must be writable

**Performance**: Must complete in under 5 seconds for standard projects

### `docgen generate plan`
**Spec Reference**: `requirements.md` - FR-02 (Document Generation)
**Purpose**: Generate project plan document

**Usage**:
```bash
docgen generate plan [OPTIONS]
```

**Options**:
- `--format, -f [markdown|html|pdf]`: Output format (default: markdown)
- `--output, -o PATH`: Output file path

**Examples**:
```bash
# Generate project plan
docgen generate plan

# Generate in PDF format
docgen generate plan --format pdf
```

### `docgen generate marketing`
**Spec Reference**: `requirements.md` - FR-02 (Document Generation)
**Purpose**: Generate marketing materials document

**Usage**:
```bash
docgen generate marketing [OPTIONS]
```

**Options**:
- `--format, -f [markdown|html|pdf]`: Output format (default: markdown)
- `--output, -o PATH`: Output file path

**Examples**:
```bash
# Generate marketing materials
docgen generate marketing

# Generate in HTML format
docgen generate marketing --format html
```

### `docgen generate all`
**Spec Reference**: `requirements.md` - FR-02 (Document Generation)
**Purpose**: Generate all available documents for the current project

**Usage**:
```bash
docgen generate all [OPTIONS]
```

**Options**:
- `--format, -f [markdown|html|pdf]`: Output format for all documents (default: markdown)
- `--output-dir, -d PATH`: Output directory for all documents

**Examples**:
```bash
# Generate all documents in markdown
docgen generate all

# Generate all documents in PDF format
docgen generate all --format pdf

# Generate to custom directory
docgen generate all --output-dir ./output
```

**Output**:
- Table showing generated documents with sizes and paths
- Summary of generation results
- Performance metrics

## Validation Commands

### `docgen validate project`
**Spec Reference**: `requirements.md` - FR-03 (Validation and Error Handling)
**Purpose**: Validate project data and configuration

**Usage**:
```bash
docgen validate project [OPTIONS]
```

**Options**:
- `--project-id TEXT`: Specific project ID to validate
- `--fix-issues`: Attempt to fix common validation issues

**Examples**:
```bash
# Validate current project
docgen validate project

# Validate specific project
docgen validate project --project-id project_name_1234567890

# Validate and fix issues
docgen validate project --fix-issues
```

**Validation Categories**:
1. **Project Data**: YAML structure, required fields, data types
2. **Templates**: Template syntax, required variables, file existence
3. **Structure**: Directory structure, required files, permissions

**Output**:
- Detailed validation results for each category
- Error and warning messages with specific issues
- Summary with total errors and warnings
- Automatic fixes applied (if --fix-issues used)

**Error Recovery**:
- Missing directories: Automatically created
- Missing project data: Generated with defaults
- Template issues: Reported with specific fixes

## Global Options

### `--help, -h`
Show help message and exit

### `--version, -V`
Show version and exit

### `--verbose, -v`
Enable verbose output

### `--quiet, -q`
Suppress output except errors

## Error Handling

### Common Error Scenarios

#### No Current Project Set
**Error**: `Error: No current project set.`
**Solution**: 
```bash
docgen project create
# or
docgen project switch --project-id <project-id>
```

#### Project Directory Not Found
**Error**: `Error: Project directory does not exist: <path>`
**Solution**: 
```bash
docgen project switch --project-id <valid-project-id>
```

#### Invalid Project Data
**Error**: `Error: Invalid YAML in project_data.yaml`
**Solution**:
```bash
docgen validate project --fix-issues
```

#### Template Not Found
**Error**: `Error: Template 'spec.j2' not found`
**Solution**: Check template installation or reinstall DocGen

#### Permission Denied
**Error**: `Error: Permission denied writing to <path>`
**Solution**: Check directory permissions or choose different output path

### Error Recovery Commands

#### `docgen validate project --fix-issues`
Automatically fixes common issues:
- Creates missing directories
- Generates missing project data files
- Reports unfixable issues

#### `docgen project recent`
Shows available projects if current project is invalid

#### `docgen project status`
Diagnoses current project state and issues

## Performance Requirements

### Response Times
- **Project creation**: < 2 seconds
- **Project switching**: < 1 second
- **Document generation**: < 5 seconds for standard projects
- **Validation**: < 3 seconds

### Resource Usage
- **Memory**: < 100MB for standard operations
- **Disk**: < 10MB per project
- **CPU**: Minimal impact during document generation

## Security Considerations

### Input Validation
- All user inputs are sanitized to prevent template injection
- File paths are validated to prevent directory traversal
- Project names are restricted to safe characters

### Data Protection
- No sensitive information is stored in project files
- User data is stored locally only
- No network communication without explicit user action

## Platform Compatibility

### Supported Platforms
- **Linux**: Ubuntu 18.04+, CentOS 7+, Debian 9+
- **macOS**: 10.14+ (Mojave and later)
- **Windows**: Windows 10+, Windows Server 2016+

### Python Versions
- **Minimum**: Python 3.8
- **Recommended**: Python 3.9+
- **Tested**: Python 3.8, 3.9, 3.10, 3.11, 3.12

## Troubleshooting

### Common Issues

#### Import Errors
```bash
# Check Python version
python --version

# Reinstall DocGen
pip uninstall docgen-cli
pip install docgen-cli
```

#### Template Errors
```bash
# Validate templates
docgen validate project

# Check template files
ls docgen/templates/
```

#### Permission Issues
```bash
# Check directory permissions
ls -la <project-directory>

# Fix permissions
chmod 755 <project-directory>
```

### Getting Help

#### Command Help
```bash
docgen --help
docgen project --help
docgen generate --help
docgen validate --help
```

#### Verbose Output
```bash
docgen --verbose <command>
```

#### Error Reports
```bash
docgen validate project --fix-issues
```

## Examples

### Complete Workflow
```bash
# 1. Create a new project
docgen project create --name "My API Project" --description "REST API for user management"

# 2. Validate the project
docgen validate project

# 3. Generate all documents
docgen generate all --format html

# 4. Check project status
docgen project status
```

### Batch Processing
```bash
# Generate multiple formats
docgen generate spec --format markdown
docgen generate spec --format html
docgen generate spec --format pdf

# Generate to different directories
docgen generate all --output-dir ./docs/markdown --format markdown
docgen generate all --output-dir ./docs/html --format html
```

### Project Management
```bash
# List recent projects
docgen project recent

# Switch between projects
docgen project switch --project-id project1_1234567890
docgen generate spec
docgen project switch --project-id project2_1234567890
docgen generate plan
```

This command reference ensures that all CLI functionality is properly documented, validated, and traceable to the project specifications.
