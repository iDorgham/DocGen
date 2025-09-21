"""
Comprehensive documentation system for DocGen CLI.

This module provides extensive documentation, examples, and tutorials
to enhance the developer experience.
"""

from typing import Any, Dict, List, Optional
from pathlib import Path
from datetime import datetime

from src.core.cli_enhancements import EnhancedConsole, HelpSystem
from src.core.error_handler import DocGenError, ErrorSeverity, ErrorCategory


class DocumentationSystem:
    """Comprehensive documentation system with examples and tutorials."""
    
    def __init__(self, console: EnhancedConsole):
        self.console = console
        self.help_system = HelpSystem(console)
        self._setup_help_system()
    
    def _setup_help_system(self):
        """Setup the help system with all commands and examples."""
        # Main commands
        self.help_system.add_command(
            "create",
            "Create a new DocGen project with guided setup",
            examples=[
                "docgen create --name 'My Project' --path './my-project'",
                "docgen create --interactive",
                "docgen create --name 'API Project' --description 'REST API documentation'"
            ],
            related_commands=["recent", "switch", "status"]
        )
        
        self.help_system.add_command(
            "spec",
            "Generate technical specification document",
            examples=[
                "docgen spec --format markdown",
                "docgen spec --format html --output ./docs/spec.html",
                "docgen spec --validate-data --auto-commit"
            ],
            related_commands=["plan", "marketing", "generate-all"]
        )
        
        self.help_system.add_command(
            "plan",
            "Generate project plan document",
            examples=[
                "docgen plan --format markdown",
                "docgen plan --format pdf --output ./docs/project-plan.pdf"
            ],
            related_commands=["spec", "marketing", "generate-all"]
        )
        
        self.help_system.add_command(
            "marketing",
            "Generate marketing materials document",
            examples=[
                "docgen marketing --format html",
                "docgen marketing --format pdf --output ./docs/marketing.pdf"
            ],
            related_commands=["spec", "plan", "generate-all"]
        )
        
        # Template commands
        self.help_system.add_command(
            "template list",
            "List all available templates",
            examples=[
                "docgen template list",
                "docgen template list --type spec",
                "docgen template list --sort date"
            ],
            related_commands=["template install", "template create", "template validate"]
        )
        
        self.help_system.add_command(
            "template install",
            "Install a template from various sources",
            examples=[
                "docgen template install ./my-template.j2",
                "docgen template install https://github.com/user/template.git",
                "docgen template install ./template-dir --name 'custom-spec'"
            ],
            related_commands=["template list", "template create", "template validate"]
        )
        
        # Git commands
        self.help_system.add_command(
            "git init",
            "Initialize Git repository for the project",
            examples=[
                "docgen git init",
                "docgen git init --branch main --user-name 'John Doe'",
                "docgen git init --no-initial-commit"
            ],
            related_commands=["git status", "git commit", "git push"]
        )
        
        self.help_system.add_command(
            "git commit",
            "Commit changes to Git repository",
            examples=[
                "docgen git commit --message 'Add generated docs'",
                "docgen git commit --auto",
                "docgen git commit --files 'docs/spec.md,docs/plan.md'"
            ],
            related_commands=["git status", "git push", "git log"]
        )
    
    def show_quick_start(self):
        """Show comprehensive quick start guide."""
        self.help_system.show_quick_start()
    
    def show_troubleshooting(self):
        """Show comprehensive troubleshooting guide."""
        self.help_system.show_troubleshooting()
    
    def show_examples(self, command: str = None):
        """Show examples for commands."""
        if command:
            self.help_system.show_command_help(command)
        else:
            self._show_all_examples()
    
    def _show_all_examples(self):
        """Show examples for all commands."""
        examples_guide = """
# DocGen CLI Examples

## Project Management

### Create a New Project
```bash
# Basic project creation
docgen create --name "My API Project" --path "./api-project"

# Interactive project creation
docgen create --interactive

# Project with description
docgen create --name "E-commerce Platform" --description "Online shopping platform with payment integration"
```

### Project Navigation
```bash
# Show recent projects
docgen recent

# Switch to a different project
docgen switch --project-id project_name_1234567890

# Show current project status
docgen status
```

## Document Generation

### Generate Individual Documents
```bash
# Technical specification
docgen spec --format markdown
docgen spec --format html --output ./docs/technical-spec.html
docgen spec --format pdf --validate-data

# Project plan
docgen plan --format markdown
docgen plan --format pdf --output ./docs/project-plan.pdf

# Marketing materials
docgen marketing --format html
docgen marketing --format pdf --output ./docs/marketing.pdf
```

### Generate All Documents
```bash
# Generate all documents in markdown
docgen generate-all --format markdown

# Generate all documents in HTML
docgen generate-all --format html --output-dir ./docs/html

# Generate all documents in PDF
docgen generate-all --format pdf --output-dir ./docs/pdf
```

## Template Management

### List and Explore Templates
```bash
# List all templates
docgen template list

# List templates by type
docgen template list --type spec
docgen template list --type plan

# Sort templates
docgen template list --sort date
docgen template list --sort version
```

### Install Templates
```bash
# Install from local file
docgen template install ./my-custom-template.j2

# Install from local directory
docgen template install ./template-package/

# Install from URL
docgen template install https://github.com/user/template.git

# Install with custom name
docgen template install ./template.j2 --name "my-spec-template"
```

### Create Custom Templates
```bash
# Create template interactively
docgen template create

# Create specific type
docgen template create --type spec --name "API Specification"

# Create marketing template
docgen template create --type marketing --name "Product Brochure"
```

### Validate Templates
```bash
# Validate template file
docgen template validate ./my-template.j2

# Validate template directory
docgen template validate ./template-package/
```

## Git Integration

### Initialize Git Repository
```bash
# Basic Git initialization
docgen git init

# Initialize with custom settings
docgen git init --branch main --user-name "John Doe" --user-email "john@example.com"

# Initialize without initial commit
docgen git init --no-initial-commit
```

### Commit Changes
```bash
# Commit with custom message
docgen git commit --message "Add generated documentation"

# Auto-generate commit message
docgen git commit --auto

# Commit specific files
docgen git commit --files "docs/spec.md,docs/plan.md" --message "Update project docs"
```

### Git Status and History
```bash
# Show Git status
docgen git status

# Show commit history
docgen git log --limit 10

# Show all branches
docgen git branches
```

### Push to Remote
```bash
# Push to current branch
docgen git push

# Push specific branch
docgen git push --branch feature/docs

# Set upstream and push
docgen git push --set-upstream
```

## Validation and Quality

### Project Validation
```bash
# Validate current project
docgen validate

# Validate specific project
docgen validate --project-id project_name_1234567890

# Validate and fix issues
docgen validate --fix-issues
```

### Error Reporting
```bash
# Generate error report
docgen error-report

# Save error report to file
docgen error-report --output ./error-report.json
```

## Advanced Usage

### Workflow Automation
```bash
# Create project and generate all docs
docgen create --name "My Project" && docgen generate-all

# Generate docs and commit to Git
docgen generate-all --format markdown && docgen git commit --auto

# Validate and generate with error handling
docgen validate --fix-issues && docgen spec --format html
```

### Batch Operations
```bash
# Generate multiple formats
for format in markdown html pdf; do
    docgen generate-all --format $format --output-dir ./docs/$format
done

# Process multiple projects
for project in project1 project2 project3; do
    docgen switch --project-id $project
    docgen generate-all --format markdown
done
```

## Configuration Examples

### Project Data Structure
```yaml
# project_data.yaml
project:
  name: "My Awesome Project"
  description: "A comprehensive project description"
  version: "1.0.0"
  goals:
    - "Deliver high-quality software"
    - "Ensure excellent user experience"
  
team:
  lead: "Project Manager"
  members:
    - name: "Lead Developer"
      role: "Technical Lead"
      responsibilities: ["Architecture", "Code Review"]
  
requirements:
  functional:
    - id: "FR-001"
      title: "User Authentication"
      description: "Users must be able to login"
      priority: "High"
  
timeline:
  phases:
    - number: 1
      name: "Planning"
      duration: "2 weeks"
      deliverables: ["Requirements", "Architecture"]
```

### Template Customization
```jinja2
# Custom template example
# {{ template_name }}.j2

# {{ project.name }}

## Overview
{{ project.description }}

## Team Structure
{% for member in team.members %}
### {{ member.name }}
- **Role:** {{ member.role }}
- **Responsibilities:** {{ member.responsibilities | join(', ') }}
{% endfor %}

## Requirements
{% for req in requirements.functional %}
### {{ req.id }}: {{ req.title }}
**Priority:** {{ req.priority }}
**Description:** {{ req.description }}

{% if req.acceptance_criteria %}
**Acceptance Criteria:**
{% for criteria in req.acceptance_criteria %}
- {{ criteria }}
{% endfor %}
{% endif %}
{% endfor %}
```
"""
        self.console.print_markdown(examples_guide, "Command Examples")
    
    def show_tutorial(self, topic: str = None):
        """Show interactive tutorial."""
        if topic:
            self._show_topic_tutorial(topic)
        else:
            self._show_tutorial_menu()
    
    def _show_tutorial_menu(self):
        """Show tutorial menu."""
        tutorial_menu = """
# DocGen CLI Tutorials

Choose a tutorial to get started:

## 1. Getting Started
- **Duration:** 5 minutes
- **Prerequisites:** None
- **What you'll learn:** Basic project creation and document generation

## 2. Template Customization
- **Duration:** 10 minutes
- **Prerequisites:** Basic DocGen knowledge
- **What you'll learn:** Creating and customizing templates

## 3. Git Integration
- **Duration:** 8 minutes
- **Prerequisites:** Basic Git knowledge
- **What you'll learn:** Version control with DocGen projects

## 4. Advanced Workflows
- **Duration:** 15 minutes
- **Prerequisites:** Intermediate DocGen knowledge
- **What you'll learn:** Automation and batch operations

## 5. Troubleshooting
- **Duration:** 10 minutes
- **Prerequisites:** Basic DocGen knowledge
- **What you'll learn:** Common issues and solutions

Run: `docgen tutorial <topic>` to start a specific tutorial
"""
        self.console.print_markdown(tutorial_menu, "Tutorial Menu")
    
    def _show_topic_tutorial(self, topic: str):
        """Show tutorial for specific topic."""
        tutorials = {
            "getting-started": self._tutorial_getting_started,
            "templates": self._tutorial_templates,
            "git": self._tutorial_git,
            "advanced": self._tutorial_advanced,
            "troubleshooting": self._tutorial_troubleshooting
        }
        
        if topic in tutorials:
            tutorials[topic]()
        else:
            self.console.print_error(f"Unknown tutorial topic: {topic}")
            self._show_tutorial_menu()
    
    def _tutorial_getting_started(self):
        """Getting started tutorial."""
        tutorial = """
# Getting Started Tutorial

## Step 1: Create Your First Project

Let's create a new DocGen project:

```bash
docgen create --name "My First Project" --path "./my-first-project"
```

This command will:
- Create a new project directory
- Set up the basic project structure
- Create an initial project data file
- Set this as your current project

## Step 2: Explore Project Structure

Your project now has this structure:
```
my-first-project/
├── docs/           # Generated documents go here
├── templates/      # Custom templates
├── data/          # Project data files
└── project_data.yaml  # Main project configuration
```

## Step 3: Generate Your First Document

Generate a technical specification:

```bash
docgen spec --format markdown
```

This creates a technical specification document in the `docs/` directory.

## Step 4: Generate All Documents

Create all document types at once:

```bash
docgen generate-all --format markdown
```

This generates:
- Technical specification
- Project plan
- Marketing materials

## Step 5: View Results

Check your generated documents:

```bash
ls docs/
```

You should see:
- technical_spec.md
- project_plan.md
- marketing.md

## Next Steps

- Edit `project_data.yaml` to customize your project
- Try different output formats: `--format html` or `--format pdf`
- Learn about templates: `docgen tutorial templates`
"""
        self.console.print_markdown(tutorial, "Getting Started Tutorial")
    
    def _tutorial_templates(self):
        """Template tutorial."""
        tutorial = """
# Template Customization Tutorial

## Understanding Templates

Templates are Jinja2 files that define how your documents are generated. They use your project data to create formatted output.

## Step 1: List Available Templates

```bash
docgen template list
```

This shows all available templates with their types and versions.

## Step 2: Create a Custom Template

```bash
docgen template create --type spec --name "My Custom Spec"
```

This creates a new template in your project's templates directory.

## Step 3: Edit Your Template

Open the template file and customize it:

```jinja2
# My Custom Spec Template

# {{ project.name }}

## Project Overview
{{ project.description }}

## Key Features
{% for goal in project.goals %}
- {{ goal }}
{% endfor %}

## Team
{% for member in team.members %}
### {{ member.name }}
**Role:** {{ member.role }}
**Responsibilities:**
{% for resp in member.responsibilities %}
- {{ resp }}
{% endfor %}
{% endfor %}
```

## Step 4: Validate Your Template

```bash
docgen template validate ./templates/my-custom-spec.j2
```

## Step 5: Use Your Template

Generate documents with your custom template:

```bash
docgen spec --template my-custom-spec
```

## Advanced Template Features

### Conditional Content
```jinja2
{% if project.version %}
**Version:** {{ project.version }}
{% endif %}
```

### Loops and Iteration
```jinja2
{% for req in requirements.functional %}
### {{ req.id }}: {{ req.title }}
{{ req.description }}
{% endfor %}
```

### Filters and Formatting
```jinja2
{{ project.name | upper }}
{{ project.description | truncate(100) }}
```
"""
        self.console.print_markdown(tutorial, "Template Tutorial")
    
    def _tutorial_git(self):
        """Git integration tutorial."""
        tutorial = """
# Git Integration Tutorial

## Why Use Git with DocGen?

Git integration helps you:
- Track changes to generated documents
- Collaborate with team members
- Maintain version history
- Deploy documentation automatically

## Step 1: Initialize Git Repository

```bash
docgen git init
```

This creates a Git repository and makes an initial commit.

## Step 2: Check Git Status

```bash
docgen git status
```

This shows the current state of your repository.

## Step 3: Generate and Commit Documents

```bash
# Generate documents
docgen generate-all --format markdown

# Commit the changes
docgen git commit --auto
```

The `--auto` flag generates a commit message based on the changes.

## Step 4: Set Up Remote Repository

```bash
docgen git remote origin https://github.com/username/my-project.git
```

## Step 5: Push to Remote

```bash
docgen git push --set-upstream
```

## Workflow Best Practices

### Regular Workflow
1. Generate documents: `docgen generate-all`
2. Review changes: `docgen git status`
3. Commit changes: `docgen git commit --auto`
4. Push to remote: `docgen git push`

### Branching Strategy
```bash
# Create feature branch
docgen git branch feature/new-template

# Switch to branch
docgen git checkout feature/new-template

# Make changes and commit
docgen generate-all
docgen git commit --message "Add new template"

# Push feature branch
docgen git push --branch feature/new-template
```

### Automated Workflows
```bash
# Generate and commit in one command
docgen generate-all && docgen git commit --auto && docgen git push
```
"""
        self.console.print_markdown(tutorial, "Git Integration Tutorial")
    
    def _tutorial_advanced(self):
        """Advanced workflows tutorial."""
        tutorial = """
# Advanced Workflows Tutorial

## Batch Operations

### Generate Multiple Formats
```bash
for format in markdown html pdf; do
    docgen generate-all --format $format --output-dir ./docs/$format
done
```

### Process Multiple Projects
```bash
for project in api-project web-app mobile-app; do
    docgen switch --project-id $project
    docgen generate-all --format markdown
    docgen git commit --auto
done
```

## Automation Scripts

### Daily Documentation Update
```bash
#!/bin/bash
# daily-docs.sh

# Update all projects
for project in $(docgen recent --format json | jq -r '.[].id'); do
    docgen switch --project-id $project
    docgen generate-all --format markdown
    docgen git commit --auto --message "Daily documentation update"
    docgen git push
done
```

### CI/CD Integration
```yaml
# .github/workflows/docs.yml
name: Generate Documentation

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install DocGen
      run: pip install docgen-cli
    
    - name: Generate Documentation
      run: |
        docgen generate-all --format markdown
        docgen generate-all --format html
    
    - name: Commit Changes
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        docgen git commit --auto
        git push
```

## Custom Templates

### API Documentation Template
```jinja2
# API Documentation Template

# {{ project.name }} API Documentation

## Overview
{{ project.description }}

## Endpoints
{% for endpoint in api.endpoints %}
### {{ endpoint.method }} {{ endpoint.path }}
**Description:** {{ endpoint.description }}

**Parameters:**
{% for param in endpoint.parameters %}
- `{{ param.name }}` ({{ param.type }}): {{ param.description }}
{% endfor %}

**Response:**
```json
{{ endpoint.response | tojson(indent=2) }}
```
{% endfor %}
```

### Project Status Template
```jinja2
# Project Status Template

# {{ project.name }} - Project Status

## Current Phase
**Phase:** {{ timeline.current_phase.name }}
**Progress:** {{ timeline.current_phase.progress }}%

## Recent Milestones
{% for milestone in timeline.recent_milestones %}
- **{{ milestone.name }}** ({{ milestone.date }}): {{ milestone.status }}
{% endfor %}

## Upcoming Tasks
{% for task in timeline.upcoming_tasks %}
- [ ] {{ task.title }} (Due: {{ task.due_date }})
{% endfor %}
```

## Performance Optimization

### Parallel Processing
```python
# parallel_generation.py
import concurrent.futures
import subprocess

def generate_docs(project_id, format_type):
    subprocess.run([
        'docgen', 'switch', '--project-id', project_id
    ])
    subprocess.run([
        'docgen', 'generate-all', '--format', format_type
    ])

projects = ['project1', 'project2', 'project3']
formats = ['markdown', 'html', 'pdf']

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    for project in projects:
        for format_type in formats:
            future = executor.submit(generate_docs, project, format_type)
            futures.append(future)
    
    for future in concurrent.futures.as_completed(futures):
        future.result()
```

## Monitoring and Analytics

### Document Generation Metrics
```bash
# Track generation time
time docgen generate-all --format markdown

# Monitor file sizes
find docs/ -name "*.md" -exec wc -c {} \\;

# Check template usage
docgen template list --sort date
```
"""
        self.console.print_markdown(tutorial, "Advanced Workflows Tutorial")
    
    def _tutorial_troubleshooting(self):
        """Troubleshooting tutorial."""
        tutorial = """
# Troubleshooting Tutorial

## Common Issues and Solutions

### 1. Project Not Found

**Problem:** `Error: No current project set`

**Solutions:**
```bash
# Check available projects
docgen recent

# Switch to existing project
docgen switch --project-id project_name_1234567890

# Create new project
docgen create --name "My Project"
```

### 2. Template Errors

**Problem:** `Template error: Template not found`

**Solutions:**
```bash
# List available templates
docgen template list

# Validate template
docgen template validate ./my-template.j2

# Install missing template
docgen template install ./template.j2
```

### 3. Validation Failures

**Problem:** `Validation error: Missing required field`

**Solutions:**
```bash
# Validate with fixes
docgen validate --fix-issues

# Check project data file
cat project_data.yaml

# Edit project data
nano project_data.yaml
```

### 4. Git Issues

**Problem:** `Not a Git repository`

**Solutions:**
```bash
# Initialize Git
docgen git init

# Check Git status
docgen git status

# Add remote repository
docgen git remote origin https://github.com/user/repo.git
```

### 5. Permission Errors

**Problem:** `Permission denied`

**Solutions:**
```bash
# Check file permissions
ls -la project_data.yaml

# Fix permissions
chmod 644 project_data.yaml

# Check directory permissions
ls -la docs/
```

## Debugging Techniques

### Enable Verbose Output
```bash
# Run with debug information
docgen --verbose spec --format markdown

# Check error logs
docgen error-report --output ./error-report.json
```

### Validate Project Structure
```bash
# Check project structure
docgen validate

# List project files
find . -name "*.yaml" -o -name "*.j2" -o -name "*.md"
```

### Test Template Syntax
```bash
# Validate template
docgen template validate ./template.j2

# Test with sample data
docgen spec --template template.j2 --dry-run
```

## Getting Help

### Command Help
```bash
# Get help for specific command
docgen create --help
docgen spec --help
docgen template --help
```

### Error Reports
```bash
# Generate detailed error report
docgen error-report --output ./debug-report.json

# View recent errors
docgen error-report
```

### Community Support
- Check the documentation: `docgen tutorial`
- View examples: `docgen examples`
- Report issues on GitHub
- Join the community forum

## Prevention Tips

### Regular Maintenance
```bash
# Weekly validation
docgen validate --fix-issues

# Update templates
docgen template list --outdated

# Clean up old files
find docs/ -name "*.tmp" -delete
```

### Backup Strategy
```bash
# Backup project data
cp project_data.yaml project_data.yaml.backup

# Commit changes regularly
docgen git commit --auto

# Push to remote
docgen git push
```

### Best Practices
- Always validate before generating
- Use version control for all projects
- Keep templates simple and readable
- Test templates with sample data
- Document custom templates
"""
        self.console.print_markdown(tutorial, "Troubleshooting Tutorial")


# Global documentation system instance
documentation_system = DocumentationSystem(EnhancedConsole())
