# DocGen CLI Developer Quick Reference

## Project Structure
```
docgen/
├── __init__.py          # Main package
├── __main__.py          # Module entry point
├── cli.py               # CLI interface
├── commands/            # Command implementations
│   ├── project.py       # Project management commands
│   ├── generate.py      # Document generation commands
│   └── validate.py      # Validation commands
├── models/              # Business logic and data models
│   ├── project.py       # Project management
│   ├── document.py      # Document generation
│   ├── template.py      # Template management
│   └── error_handler.py # Error handling
├── templates/           # Jinja2 templates
│   ├── spec.j2          # Technical specification template
│   ├── plan.j2          # Project plan template
│   └── marketing.j2     # Marketing materials template
└── utils/               # Utility functions
    ├── validation.py    # Input validation
    ├── formatting.py    # Document formatting
    └── file_io.py       # File operations
```

## Quick Commands

### Development Setup
```bash
# Install in development mode
pip install -e .

# Run CLI
python -m docgen --help

# Run tests
pytest tests/

# Lint code
black docgen/
isort docgen/
flake8 docgen/
mypy docgen/
```

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/models/test_project.py

# Run with coverage
pytest --cov=docgen

# Run specific test
pytest tests/models/test_project.py::test_create_project
```

### Code Quality
```bash
# Format code
black docgen/ tests/

# Sort imports
isort docgen/ tests/

# Lint code
flake8 docgen/ tests/

# Type checking
mypy docgen/
```

## Key Files

### Specifications
- `specs/requirements.md` - Functional and non-functional requirements
- `specs/tech.md` - Technical architecture and implementation details
- `specs/tasks.md` - Development tasks and milestones

### Configuration
- `pyproject.toml` - Project configuration and dependencies
- `.gitignore` - Git ignore rules
- `README.md` - Project documentation

### Development
- `SPEC_DRIVEN_DEVELOPMENT_PLAN.md` - Complete development plan
- `COMMANDS_REFERENCE.md` - CLI commands documentation
- `SPEC_VALIDATION_CHECKLIST.md` - Validation checklist

## Common Patterns

### Adding a New Command
1. **Create command function** in appropriate `commands/` module
2. **Add to command group** in `cli.py`
3. **Write tests** in `tests/commands/`
4. **Update documentation** in `COMMANDS_REFERENCE.md`

### Adding a New Model
1. **Create model class** in `models/` package
2. **Add to `__init__.py`** exports
3. **Write tests** in `tests/models/`
4. **Update imports** in commands that use it

### Adding a New Template
1. **Create Jinja2 template** in `templates/`
2. **Add to template list** in `templates/__init__.py`
3. **Update generation logic** in `models/document.py`
4. **Write tests** for template rendering

## Import Patterns

### From Commands
```python
from ..models.project import ProjectManager
from ..utils.validation import InputValidator
```

### From Models
```python
from .error_handler import DocGenError
from ..utils.file_io import FileManager
```

### From Utils
```python
from .validation import ValidationError
from ..models.error_handler import handle_error
```

## Error Handling

### Custom Exceptions
```python
from ..models.error_handler import DocGenError, ValidationError

# Raise custom error
raise ValidationError("Invalid input provided")

# Handle with user-friendly message
try:
    # risky operation
except Exception as e:
    handle_error(e, context={"command": "create"})
```

### Validation
```python
from ..utils.validation import InputValidator

validator = InputValidator()
is_valid, error_msg = validator.validate_project_name(name)
if not is_valid:
    console.print(f"[red]Error: {error_msg}[/red]")
    return
```

## CLI Patterns

### Command Structure
```python
@click.group(name="project")
def project_group():
    """Project management commands."""
    pass

@project_group.command()
@click.option('--name', '-n', help='Project name')
def create(name: str):
    """Create a new project."""
    # Implementation
```

### Rich Output
```python
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Success message
console.print(Panel.fit(
    "[green]✓ Operation completed successfully![/green]",
    title="Success",
    border_style="green"
))

# Error message
console.print(f"[red]Error: {error_message}[/red]")

# Table output
table = Table(title="Results")
table.add_column("Name", style="cyan")
table.add_column("Status", style="green")
table.add_row("Item 1", "Success")
console.print(table)
```

## Testing Patterns

### Unit Tests
```python
import pytest
from docgen.models.project import ProjectManager

def test_create_project():
    """Test project creation."""
    manager = ProjectManager()
    result = manager.create_project("Test Project", Path("/tmp"), "Description")
    assert result["name"] == "Test Project"
    assert result["id"] is not None
```

### CLI Tests
```python
from click.testing import CliRunner
from docgen.cli import main

def test_create_command():
    """Test create command."""
    runner = CliRunner()
    result = runner.invoke(main, ["project", "create", "--name", "Test"])
    assert result.exit_code == 0
    assert "Project created successfully" in result.output
```

### Mock Tests
```python
from unittest.mock import patch, mock_open

@patch("builtins.open", new_callable=mock_open)
def test_file_operations(mock_file):
    """Test file operations with mock."""
    # Test implementation
    mock_file.assert_called_with("test.yaml", "w")
```

## Performance Guidelines

### Response Times
- Project operations: < 2 seconds
- Document generation: < 5 seconds
- Validation: < 3 seconds

### Resource Usage
- Memory: < 100MB for standard operations
- CPU: Minimal impact during operations
- Disk: < 10MB per project

## Security Guidelines

### Input Validation
```python
# Always validate user inputs
validator = InputValidator()
is_valid, error_msg = validator.validate_input(user_input)
if not is_valid:
    raise ValidationError(error_msg)

# Sanitize inputs
sanitized = validator.sanitize_input(user_input)
```

### File Operations
```python
# Validate file paths
if not output_path.is_absolute():
    output_path = Path.cwd() / output_path

# Check permissions
if not output_path.parent.exists():
    output_path.parent.mkdir(parents=True, exist_ok=True)
```

## Debugging

### Enable Verbose Output
```bash
python -m docgen --verbose <command>
```

### Check Project State
```bash
docgen project status
docgen validate project
```

### Test Individual Components
```python
# Test model directly
from docgen.models.project import ProjectManager
manager = ProjectManager()
projects = manager.get_all_projects()

# Test template rendering
from docgen.models.document import DocumentGenerator
generator = DocumentGenerator()
content = generator.generate_document("spec", project_data, "markdown")
```

## Common Issues

### Import Errors
- Check `__init__.py` files exist in all packages
- Verify relative import paths
- Ensure all dependencies are installed

### Template Errors
- Validate Jinja2 syntax
- Check template variable names
- Verify template file paths

### Permission Errors
- Check file/directory permissions
- Ensure output directories are writable
- Verify project directory access

### Performance Issues
- Profile document generation
- Check for large project data
- Optimize template rendering

## Best Practices

### Code Organization
- Keep commands focused on CLI logic
- Put business logic in models
- Use utils for reusable functions
- Maintain clear separation of concerns

### Error Handling
- Always provide user-friendly error messages
- Include actionable suggestions
- Log errors for debugging
- Handle edge cases gracefully

### Testing
- Write tests for all new functionality
- Test error scenarios
- Maintain high test coverage
- Test across platforms

### Documentation
- Update CLI help text
- Keep README current
- Document new features
- Provide usage examples

This quick reference provides essential information for developers working on the DocGen CLI project while maintaining the spec-driven development approach.
