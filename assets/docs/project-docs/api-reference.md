# DocGen CLI API Reference

## Overview

DocGen CLI provides a comprehensive command-line interface for generating project documentation. This reference covers all commands, options, and configuration options available in DocGen CLI.

## Command Structure

```bash
docgen <command> [options] [arguments]
```

## Global Options

These options are available for all commands:

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--version` | - | Show version information and exit | - |
| `--verbose` | `-v` | Enable verbose output | `false` |
| `--help` | `-h` | Show help message and exit | - |

## Commands

### `create`

Creates a new project with the specified name and optional path.

```bash
docgen create <project-name> [path] [options]
```

#### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `project-name` | Yes | Name of the project to create |
| `path` | No | Directory path where to create the project (default: `./<project-name>`) |

#### Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--verbose` | `-v` | Enable verbose output | `false` |

#### Examples

```bash
# Create project in current directory
docgen create my-project

# Create project in specific directory
docgen create my-project ./projects/my-project

# Create with verbose output
docgen create my-project --verbose
```

#### Generated Structure

```
<project-name>/
├── docs/                    # Generated documentation directory
├── data/                    # Project data directory
└── project_data.yaml        # Project configuration file
```

### `spec`

Generates a technical specification document.

```bash
docgen spec [options]
```

#### Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--output` | `-o` | Output file path | `docs/technical_spec.md` |
| `--format` | `-f` | Output format (`markdown`, `html`, `pdf`) | `markdown` |
| `--template` | `-t` | Template to use | `default` |
| `--verbose` | `-v` | Enable verbose output | `false` |

#### Examples

```bash
# Generate with default settings
docgen spec

# Generate HTML output
docgen spec --format html

# Generate with custom output path
docgen spec --output docs/api_spec.md

# Generate PDF
docgen spec --format pdf --output docs/spec.pdf

# Use custom template
docgen spec --template custom
```

#### Output Formats

##### Markdown
- Clean, readable format
- Compatible with GitHub, GitLab
- Easy to edit and version control

##### HTML
- Professional web-ready format
- Includes CSS styling
- Perfect for web documentation

##### PDF
- Print-ready format
- Professional presentation
- Requires additional dependencies

### `plan`

Generates a project plan document.

```bash
docgen plan [options]
```

#### Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--output` | `-o` | Output file path | `docs/project_plan.md` |
| `--format` | `-f` | Output format (`markdown`, `html`, `pdf`) | `markdown` |
| `--template` | `-t` | Template to use | `default` |
| `--verbose` | `-v` | Enable verbose output | `false` |

#### Examples

```bash
# Generate with default settings
docgen plan

# Generate HTML output
docgen plan --format html

# Generate with custom output path
docgen plan --output docs/roadmap.md

# Generate PDF
docgen plan --format pdf --output docs/plan.pdf
```

### `marketing`

Generates marketing materials.

```bash
docgen marketing [options]
```

#### Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--output` | `-o` | Output file path | `docs/marketing.md` |
| `--format` | `-f` | Output format (`markdown`, `html`, `pdf`) | `markdown` |
| `--template` | `-t` | Template to use | `default` |
| `--verbose` | `-v` | Enable verbose output | `false` |

#### Examples

```bash
# Generate with default settings
docgen marketing

# Generate HTML output
docgen marketing --format html

# Generate with custom output path
docgen marketing --output marketing/index.html

# Use custom template
docgen marketing --template campaign
```

### `validate`

Validates project data and structure.

```bash
docgen validate [options]
```

#### Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--fix` | - | Fix issues automatically | `false` |
| `--verbose` | `-v` | Enable verbose output | `false` |

#### Examples

```bash
# Validate project
docgen validate

# Validate and fix issues
docgen validate --fix

# Validate with verbose output
docgen validate --verbose
```

#### Validation Checks

1. **Project Data File**
   - File exists and is readable
   - Valid YAML syntax
   - Required fields present

2. **Project Structure**
   - Required directories exist
   - Generated documents are present
   - File permissions are correct

3. **Data Integrity**
   - Project name is valid
   - Version follows semantic versioning
   - Email addresses are valid
   - URLs are properly formatted

### `help`

Shows detailed help information.

```bash
docgen help [command]
```

#### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `command` | No | Show help for specific command |

#### Examples

```bash
# Show general help
docgen help

# Show help for specific command
docgen help create
docgen help spec
```

## Configuration

### Project Data File (`project_data.yaml`)

The project data file contains all configuration for your project. It uses YAML format and supports the following structure:

#### Basic Structure

```yaml
project:
  name: "Project Name"           # Required: Project name
  description: "Description"     # Required: Project description
  version: "1.0.0"              # Required: Semantic version
  author: "Author Name"         # Optional: Author name
  email: "author@example.com"   # Optional: Author email
  repository: "https://..."     # Optional: Repository URL
  website: "https://..."        # Optional: Project website
  license: "MIT"                # Optional: License type

requirements:
  functional:                   # Required: Functional requirements
    - "Requirement 1"
    - "Requirement 2"
  non_functional:               # Optional: Non-functional requirements
    - "Performance requirement"
    - "Security requirement"

timeline:
  phases:                       # Optional: Project phases
    - name: "Phase 1"
      duration: "2 weeks"
      tasks:
        - "Task 1"
        - "Task 2"

team:
  members:                      # Optional: Team members
    - name: "John Doe"
      role: "Developer"
      email: "john@example.com"

technology:
  stack:                        # Optional: Technology stack
    - "Python"
    - "React"
    - "PostgreSQL"
  tools:
    - "Docker"
    - "Kubernetes"

deployment:
  environment: "production"     # Optional: Deployment environment
  platform: "cloud"            # Optional: Deployment platform
  monitoring: true              # Optional: Monitoring enabled
```

#### Field Validation

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `project.name` | String | Yes | Non-empty, alphanumeric with spaces |
| `project.description` | String | Yes | Non-empty |
| `project.version` | String | Yes | Semantic version format |
| `project.email` | String | No | Valid email format |
| `project.repository` | String | No | Valid URL format |
| `project.website` | String | No | Valid URL format |
| `requirements.functional` | Array | Yes | Non-empty array |
| `requirements.non_functional` | Array | No | Array of strings |

## Templates

### Template System

DocGen CLI uses Jinja2 templates for document generation. Templates are located in the `src/templates/` directory.

#### Default Templates

- `technical_spec.j2` - Technical specification template
- `project_plan.j2` - Project plan template
- `marketing.j2` - Marketing materials template

#### Template Variables

Templates have access to all project data through the following variables:

```jinja2
# Project information
{{ project.name }}
{{ project.description }}
{{ project.version }}
{{ project.author }}
{{ project.email }}

# Requirements
{% for req in requirements.functional %}
- {{ req }}
{% endfor %}

# Team members
{% for member in team.members %}
- {{ member.name }} ({{ member.role }})
{% endfor %}

# Technology stack
{% for tech in technology.stack %}
- {{ tech }}
{% endfor %}
```

#### Custom Templates

You can create custom templates by placing them in the `templates/` directory:

```bash
mkdir templates
# Create your custom template files
```

Use custom templates with the `--template` option:

```bash
docgen spec --template custom
```

## Environment Variables

DocGen CLI respects the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `DOCGEN_CONFIG_DIR` | Configuration directory | `~/.docgen` |
| `DOCGEN_TEMPLATE_DIR` | Template directory | `./templates` |
| `DOCGEN_OUTPUT_DIR` | Default output directory | `./docs` |
| `DOCGEN_VERBOSE` | Enable verbose output | `false` |

## Exit Codes

DocGen CLI uses the following exit codes:

| Code | Description |
|------|-------------|
| `0` | Success |
| `1` | General error |
| `2` | Invalid command or option |
| `3` | File not found |
| `4` | Permission denied |
| `5` | Validation error |
| `6` | Template error |

## Error Handling

### Error Types

1. **Validation Errors**
   - Invalid project data
   - Missing required fields
   - Invalid file formats

2. **File System Errors**
   - Permission denied
   - File not found
   - Disk space issues

3. **Template Errors**
   - Template not found
   - Template syntax errors
   - Missing template variables

4. **Configuration Errors**
   - Invalid configuration
   - Missing dependencies
   - Environment issues

### Error Messages

Error messages follow a consistent format:

```
❌ Error: <error-type>
<detailed-description>

Suggestions:
- <suggestion-1>
- <suggestion-2>
```

### Verbose Mode

Enable verbose mode for detailed error information:

```bash
docgen <command> --verbose
```

This provides:
- Detailed error messages
- Stack traces
- Debug information
- Execution flow

## Performance

### Benchmarks

Typical performance on modern hardware:

| Operation | Time | Memory |
|-----------|------|--------|
| Project creation | < 1s | < 50MB |
| Document generation | < 5s | < 100MB |
| Validation | < 2s | < 50MB |

### Optimization Tips

1. **Use virtual environments** to avoid dependency conflicts
2. **Keep project data files small** for faster processing
3. **Use SSD storage** for better I/O performance
4. **Enable verbose mode** only when debugging

## Security

### Input Validation

DocGen CLI validates all inputs to prevent security issues:

- **File paths**: Prevents directory traversal attacks
- **YAML content**: Validates structure and content
- **Template variables**: Sanitizes user input
- **URLs**: Validates format and protocol

### Best Practices

1. **Validate project data** before processing
2. **Use trusted templates** only
3. **Review generated content** before publishing
4. **Keep dependencies updated**

## Integration

### CI/CD Integration

Example GitHub Actions workflow:

```yaml
name: Generate Documentation
on: [push, pull_request]

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install DocGen CLI
        run: pip install docgen-cli
      - name: Generate documentation
        run: |
          docgen spec --format html
          docgen plan --format pdf
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: documentation
          path: docs/
```

### Makefile Integration

```makefile
.PHONY: docs clean

docs: project_data.yaml
	docgen spec --format html
	docgen plan --format pdf
	docgen marketing --format html

clean:
	rm -rf docs/*.html docs/*.pdf

validate:
	docgen validate --fix
```

## Troubleshooting

### Common Issues

#### "command not found: docgen"
- Check installation: `pip show docgen-cli`
- Verify PATH: `which docgen`
- Reinstall: `pip install --user docgen-cli`

#### "project_data.yaml not found"
- Ensure you're in a project directory
- Create a project: `docgen create my-project`
- Check file permissions

#### "Template not found"
- Verify template exists in `templates/` directory
- Use default templates: remove `--template` option
- Check template syntax

#### "Permission denied"
- Check file permissions
- Use virtual environment
- Run with appropriate user permissions

### Debug Mode

Enable debug mode for detailed troubleshooting:

```bash
export DOCGEN_VERBOSE=true
docgen <command>
```

### Log Files

DocGen CLI creates log files in the following locations:

- **Linux/macOS**: `~/.docgen/logs/`
- **Windows**: `%APPDATA%\docgen\logs\`

Log files include:
- Command execution logs
- Error details
- Performance metrics
- Debug information

## Support

### Getting Help

1. **Documentation**: [User Guide](USER_GUIDE.md)
2. **GitHub Issues**: [Report bugs](https://github.com/docgen-cli/docgen-cli/issues)
3. **Discussions**: [Community support](https://github.com/docgen-cli/docgen-cli/discussions)
4. **Email**: support@docgen.dev

### Contributing

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Add tests**
5. **Submit a pull request**

### License

DocGen CLI is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

For more information, visit the [official documentation](https://docgen-cli.readthedocs.io) or [GitHub repository](https://github.com/docgen-cli/docgen-cli).
