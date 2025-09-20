# DocGen CLI User Guide

## Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Commands Reference](#commands-reference)
4. [Project Structure](#project-structure)
5. [Templates and Customization](#templates-and-customization)
6. [Output Formats](#output-formats)
7. [Troubleshooting](#troubleshooting)
8. [Examples](#examples)
9. [Best Practices](#best-practices)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Install from PyPI (Recommended)
```bash
pip install docgen-cli
```

### Install from Source
```bash
git clone https://github.com/docgen-cli/docgen-cli.git
cd docgen-cli
pip install -e .
```

### Verify Installation
```bash
docgen --version
```

## Quick Start

### 1. Create Your First Project
```bash
docgen create my-awesome-project
cd my-awesome-project
```

### 2. Edit Project Data
Edit the `project_data.yaml` file with your project information:
```yaml
project:
  name: "My Awesome Project"
  description: "A revolutionary application that changes everything"
  version: "1.0.0"
  author: "Your Name"
  email: "your.email@example.com"
  repository: "https://github.com/username/my-awesome-project"
  
requirements:
  functional:
    - "User authentication system"
    - "Data management interface"
    - "Reporting dashboard"
  non_functional:
    - "Response time < 200ms"
    - "Support for 1000+ concurrent users"
    - "99.9% uptime"
```

### 3. Generate Documentation
```bash
# Generate all documents
docgen spec
docgen plan
docgen marketing

# Or generate with specific formats
docgen spec --format html --output docs/technical_spec.html
docgen plan --format pdf
```

### 4. Validate Your Project
```bash
docgen validate
```

## Commands Reference

### `docgen create <project-name> [path]`
Creates a new project with the specified name and optional path.

**Options:**
- `--verbose, -v`: Enable verbose output

**Examples:**
```bash
docgen create my-project
docgen create my-project ./projects/my-project
```

### `docgen spec [options]`
Generates a technical specification document.

**Options:**
- `--output, -o`: Output file path
- `--format, -f`: Output format (markdown, html, pdf)
- `--template, -t`: Template to use
- `--verbose, -v`: Enable verbose output

**Examples:**
```bash
docgen spec
docgen spec --output docs/spec.md
docgen spec --format html --output docs/spec.html
```

### `docgen plan [options]`
Generates a project plan document.

**Options:**
- `--output, -o`: Output file path
- `--format, -f`: Output format (markdown, html, pdf)
- `--template, -t`: Template to use
- `--verbose, -v`: Enable verbose output

**Examples:**
```bash
docgen plan
docgen plan --format html
docgen plan --output docs/project_plan.pdf
```

### `docgen marketing [options]`
Generates marketing materials.

**Options:**
- `--output, -o`: Output file path
- `--format, -f`: Output format (markdown, html, pdf)
- `--template, -t`: Template to use
- `--verbose, -v`: Enable verbose output

**Examples:**
```bash
docgen marketing
docgen marketing --format html
docgen marketing --template custom
```

### `docgen validate [options]`
Validates project data and structure.

**Options:**
- `--fix`: Fix issues automatically
- `--verbose, -v`: Enable verbose output

**Examples:**
```bash
docgen validate
docgen validate --fix
```

### `docgen help`
Shows detailed help information.

### `docgen --version`
Shows version information.

## Project Structure

When you create a project, DocGen CLI sets up the following structure:

```
my-project/
├── docs/                    # Generated documentation
│   ├── technical_spec.md   # Technical specification
│   ├── project_plan.md     # Project plan
│   └── marketing.md        # Marketing materials
├── data/                   # Project data files
└── project_data.yaml       # Project configuration
```

### Project Data File (`project_data.yaml`)

The project data file is the heart of your project configuration. It contains all the information needed to generate your documentation.

#### Basic Structure
```yaml
project:
  name: "Project Name"
  description: "Project description"
  version: "1.0.0"
  author: "Author Name"
  email: "author@example.com"
  repository: "https://github.com/username/project"

requirements:
  functional:
    - "Requirement 1"
    - "Requirement 2"
  non_functional:
    - "Performance requirement"
    - "Security requirement"

timeline:
  phases:
    - name: "Phase 1"
      duration: "2 weeks"
      tasks:
        - "Task 1"
        - "Task 2"

team:
  members:
    - name: "John Doe"
      role: "Developer"
      email: "john@example.com"
```

## Templates and Customization

### Default Templates

DocGen CLI comes with professional templates for:
- **Technical Specification**: Comprehensive technical documentation
- **Project Plan**: Detailed project planning and timeline
- **Marketing Materials**: Professional marketing content

### Custom Templates

You can create custom templates by placing them in the `templates/` directory:

```bash
mkdir templates
# Create your custom template files
```

### Template Variables

Templates use Jinja2 syntax and have access to all project data:

```jinja2
# Access project information
{{ project.name }}
{{ project.description }}
{{ project.version }}

# Access requirements
{% for req in requirements.functional %}
- {{ req }}
{% endfor %}

# Access team members
{% for member in team.members %}
- {{ member.name }} ({{ member.role }})
{% endfor %}
```

## Output Formats

### Markdown (Default)
- Clean, readable format
- Compatible with GitHub, GitLab, and most documentation platforms
- Easy to edit and version control

### HTML
- Professional web-ready format
- Includes CSS styling
- Perfect for web documentation

### PDF
- Print-ready format
- Professional presentation
- Requires additional dependencies

## Troubleshooting

### Common Issues

#### "project_data.yaml not found"
**Solution:** Make sure you're in a project directory or create a project first:
```bash
docgen create my-project
cd my-project
```

#### "Permission denied" errors
**Solution:** Check file permissions and ensure you have write access to the directory.

#### "Template not found" errors
**Solution:** Verify the template exists in the correct location or use the default templates.

#### Import errors
**Solution:** Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Getting Help

1. **Check the help:** `docgen help`
2. **Enable verbose mode:** Add `--verbose` to any command
3. **Check the logs:** Look for error messages in the output
4. **Report issues:** Create an issue on GitHub with:
   - Your command
   - Error message
   - Project data (sanitized)
   - System information

## Examples

### Example 1: Simple Web Application
```bash
# Create project
docgen create web-app

# Edit project_data.yaml
cat > project_data.yaml << EOF
project:
  name: "My Web App"
  description: "A modern web application"
  version: "1.0.0"
  author: "John Doe"
  email: "john@example.com"

requirements:
  functional:
    - "User registration and login"
    - "Dashboard interface"
    - "Data visualization"
  non_functional:
    - "Response time < 100ms"
    - "Mobile responsive design"
    - "HTTPS encryption"
EOF

# Generate documentation
docgen spec --format html
docgen plan
docgen marketing
```

### Example 2: API Documentation
```bash
# Create project
docgen create api-project

# Generate API documentation
docgen spec --output docs/api_spec.md
docgen plan --format html --output docs/api_plan.html
```

### Example 3: Marketing Campaign
```bash
# Create project
docgen create marketing-campaign

# Generate marketing materials
docgen marketing --format html --output marketing/index.html
```

## Best Practices

### 1. Project Organization
- Use descriptive project names
- Keep project data files up to date
- Organize generated documents in subdirectories

### 2. Documentation Quality
- Write clear, concise descriptions
- Include specific, measurable requirements
- Keep documentation current with project changes

### 3. Version Control
- Commit project data files to version control
- Use meaningful commit messages
- Tag releases with version numbers

### 4. Collaboration
- Share project data files with team members
- Use consistent naming conventions
- Document custom templates and processes

### 5. Automation
- Integrate DocGen CLI into your build process
- Use CI/CD pipelines to generate documentation
- Automate document updates on code changes

## Advanced Usage

### Batch Processing
```bash
# Generate all documents for multiple projects
for project in project1 project2 project3; do
    cd $project
    docgen spec
    docgen plan
    docgen marketing
    cd ..
done
```

### Custom Scripts
```bash
#!/bin/bash
# generate_docs.sh
PROJECT_NAME=$1
cd $PROJECT_NAME
docgen spec --format html --output docs/spec.html
docgen plan --format pdf --output docs/plan.pdf
docgen marketing --format html --output docs/marketing.html
echo "Documentation generated for $PROJECT_NAME"
```

### Integration with Build Systems
```makefile
# Makefile
docs: project_data.yaml
	docgen spec --format html
	docgen plan --format pdf
	docgen marketing --format html

clean:
	rm -rf docs/*.html docs/*.pdf
```

---

For more information, visit the [official documentation](https://docgen-cli.readthedocs.io) or [GitHub repository](https://github.com/docgen-cli/docgen-cli).
