# Technical Architecture for DocGen CLI

## Architecture Overview

### Core Architecture
- **CLI Framework**: Built with Click for command-line parsing and Rich for enhanced prompts and output formatting
- **Data Model**: Pydantic-based models (ProjectModel, DocumentConfig, TemplateModel) for structured data validation and serialization
- **Storage**: Project data stored in YAML files in user config directory (~/.docgen/projects/)
- **Templating System**: Jinja2 engine with custom environment filters and template inheritance
- **Error Handling**: Custom exception classes integrated with Click's error system; comprehensive logging via Python's logging module

### MCP Integration Architecture
- **Byterover MCP**: Knowledge management, project planning, and development workflow automation
- **TestSprite MCP**: Automated testing and quality assurance
- **Context7 MCP**: Library documentation and API reference lookup
- **Dart MCP**: Task and project management integration
- **Browser Tools MCP**: Real-time quality audits and debugging
- **Playwright MCP**: Advanced browser automation and end-to-end testing

## Project Structure

```
DocGen/
├── src/                        # Source code
│   ├── cli/                    # CLI interface
│   │   └── main.py            # Main CLI entry point
│   ├── commands/               # CLI commands
│   │   ├── project.py         # Project management commands
│   │   ├── generate.py        # Document generation commands
│   │   └── validate.py        # Validation commands
│   ├── core/                   # Core functionality
│   │   ├── generator.py       # Document generation engine
│   │   ├── project_manager.py # Project management logic
│   │   ├── template_manager.py # Template management
│   │   ├── validation.py      # Validation logic
│   │   ├── error_handler.py   # Error handling
│   │   └── git_manager.py     # Git integration
│   ├── models/                 # Data models
│   │   ├── project.py         # Project data models
│   │   ├── document.py        # Document models
│   │   ├── template.py        # Template models
│   │   └── error_handler.py   # Error models
│   ├── templates/              # Jinja2 templates
│   │   ├── spec.j2            # Technical specification template
│   │   ├── plan.j2            # Project plan template
│   │   ├── marketing.j2       # Marketing document template
│   │   ├── technical_spec.j2  # Detailed technical spec
│   │   ├── project_plan.j2    # Detailed project plan
│   │   └── marketing_loose.j2 # Flexible marketing template
│   └── utils/                  # Utility functions
│       ├── file_io.py         # File operations
│       ├── formatting.py      # Text formatting utilities
│       └── validation.py      # Input validation utilities
├── assets/             # Project assets and resources
│   ├── specifications/         # Specification documents
│   ├── templates/             # Template specifications
│   ├── data/                  # Sample data files
│   ├── documentation/         # Documentation
│   ├── development/           # Development tools and scripts
│   └── configuration/         # Configuration files
├── tests/                     # Test files
├── venv/                      # Virtual environment
├── pyproject.toml             # Project configuration
├── requirements.txt           # Python dependencies
└── README.md                  # Project overview
```

## Dependencies

### Core Dependencies
- **Click**: CLI framework
- **Jinja2**: Template engine
- **Pydantic**: Data validation
- **Rich**: Enhanced terminal output
- **PyYAML**: YAML file handling

### Output Dependencies
- **WeasyPrint**: PDF generation
- **Markdown**: Markdown processing

### Development Dependencies
- **pytest**: Testing framework
- **black**: Code formatting
- **flake8**: Code linting
- **mypy**: Type checking

### MCP Dependencies
- MCP client libraries for each server
- Authentication and configuration management

## Data Models

### Project Model
```python
class ProjectModel(BaseModel):
    id: str = Field(..., description="Unique project identifier")
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    path: str = Field(..., description="Project directory path")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    status: ProjectStatus = Field(default=ProjectStatus.ACTIVE)
    features: List[FeatureModel] = Field(default_factory=list)
    phases: List[PhaseModel] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
```

### Document Model
```python
class DocumentModel(BaseModel):
    id: str = Field(..., description="Unique document identifier")
    project_id: str = Field(..., description="Associated project ID")
    type: DocumentType = Field(..., description="Document type")
    format: OutputFormat = Field(..., description="Output format")
    content: str = Field(..., description="Generated content")
    generated_at: datetime = Field(default_factory=datetime.now)
    template_used: Optional[str] = Field(None)
    custom_variables: Dict[str, Any] = Field(default_factory=dict)
    file_size: Optional[int] = Field(None)
    generation_time: Optional[float] = Field(None)
```

### Template Model
```python
class TemplateModel(BaseModel):
    name: str = Field(..., description="Template identifier")
    type: DocumentType = Field(..., description="Document type")
    content: str = Field(..., description="Jinja2 template content")
    version: str = Field(..., description="Semantic version")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    description: Optional[str] = Field(None)
    author: Optional[str] = Field(None)
    custom_filters: List[FilterDefinition] = Field(default_factory=list)
    required_variables: List[str] = Field(default_factory=list)
    default_variables: Dict[str, Any] = Field(default_factory=dict)
```

## Template System

### Template Structure
- **Base Templates**: Common structure and styling
- **Document Templates**: Specific templates for each document type
- **Component Templates**: Reusable template components
- **Custom Templates**: User-defined template overrides

### Template Inheritance
```jinja2
{% extends "base.j2" %}

{% block title %}{{ project_name }} - Technical Specification{% endblock %}

{% block content %}
# Technical Specification

## Project Overview
{{ project_description }}

## Requirements
{% for requirement in requirements %}
- {{ requirement }}
{% endfor %}
{% endblock %}
```

### Custom Filters
- `format_date`: Format date strings
- `format_number`: Format numbers with locale
- `format_currency`: Format currency values
- `truncate_text`: Truncate long text with ellipsis
- `markdown_to_html`: Convert markdown to HTML
- `json_pretty`: Pretty print JSON
- `yaml_pretty`: Pretty print YAML

## Output Generation

### Markdown Output
- Direct Jinja2 rendering to markdown files
- Support for GitHub-flavored markdown
- Automatic table of contents generation
- Code syntax highlighting

### HTML Output
- Jinja2 rendering with HTML templates
- Embedded CSS for styling
- Responsive design for different screen sizes
- Print-friendly stylesheets

### PDF Output
- HTML to PDF conversion using WeasyPrint
- Professional styling and formatting
- Page breaks and headers/footers
- Table of contents and page numbering

## MCP Integration Details

### Byterover MCP Integration
```python
class ByteroverIntegration:
    def __init__(self):
        self.client = ByteroverClient()
    
    def retrieve_knowledge(self, query: str) -> Dict[str, Any]:
        """Retrieve relevant knowledge for development context"""
        return self.client.retrieve(query)
    
    def store_knowledge(self, content: str) -> bool:
        """Store implementation knowledge and patterns"""
        return self.client.store(content)
    
    def save_implementation_plan(self, plan: ImplementationPlan) -> bool:
        """Save structured implementation plans"""
        return self.client.save_plan(plan)
```

### TestSprite MCP Integration
```python
class TestSpriteIntegration:
    def __init__(self):
        self.client = TestSpriteClient()
    
    def bootstrap_tests(self, project_path: str) -> bool:
        """Initialize testing environment"""
        return self.client.bootstrap(project_path)
    
    def generate_test_plan(self, project_path: str) -> TestPlan:
        """Generate comprehensive test plan"""
        return self.client.generate_plan(project_path)
    
    def execute_tests(self, test_ids: List[str]) -> TestResults:
        """Execute automated tests"""
        return self.client.execute_tests(test_ids)
```

### Context7 MCP Integration
```python
class Context7Integration:
    def __init__(self):
        self.client = Context7Client()
    
    def resolve_library_id(self, library_name: str) -> str:
        """Resolve library name to Context7 ID"""
        return self.client.resolve_id(library_name)
    
    def get_library_docs(self, library_id: str, topic: str) -> str:
        """Get comprehensive library documentation"""
        return self.client.get_docs(library_id, topic)
```

## Error Handling

### Exception Hierarchy
```python
class DocGenError(Exception):
    """Base exception for all DocGen errors"""
    pass

class ValidationError(DocGenError):
    """Input validation errors"""
    pass

class TemplateError(DocGenError):
    """Template rendering errors"""
    pass

class ProjectError(DocGenError):
    """Project management errors"""
    pass

class GenerationError(DocGenError):
    """Document generation errors"""
    pass
```

### Error Recovery
- Automatic rollback for failed operations
- Graceful degradation for non-critical failures
- User-friendly error messages with recovery suggestions
- Comprehensive logging for debugging

## Performance Optimization

### Caching Strategy
- Template compilation caching
- Project data caching
- Generated document caching
- MCP response caching

### Memory Management
- Lazy loading of large templates
- Streaming for large document generation
- Garbage collection optimization
- Memory usage monitoring

### Concurrent Processing
- Parallel template rendering
- Concurrent MCP server calls
- Async file operations
- Thread-safe data access

## Security Implementation

### Input Sanitization
- XSS prevention in HTML output
- Path traversal prevention
- Template injection prevention
- SQL injection prevention (future)

### Data Protection
- Encryption at rest for sensitive data
- Secure file permissions
- No sensitive data in logs
- Secure MCP communication

## Testing Strategy

### Unit Testing
- Model validation tests
- Template rendering tests
- Command execution tests
- Utility function tests

### Integration Testing
- End-to-end workflow tests
- MCP integration tests
- File system operation tests
- Cross-platform compatibility tests

### Performance Testing
- Document generation benchmarks
- Memory usage profiling
- Concurrent operation testing
- Load testing for large projects

## Deployment and Distribution

### Packaging
- setuptools-based packaging
- Wheel distribution
- PyPI publishing
- Docker containerization (future)

### Installation
```bash
pip install docgen-cli
```

### Configuration
- User configuration in ~/.docgen/
- Project-specific configuration
- Environment variable support
- MCP server configuration

## Monitoring and Logging

### Logging Strategy
- Structured logging with JSON format
- Different log levels for different components
- Log rotation and archival
- Performance metrics logging

### Monitoring
- Application performance monitoring
- Error rate tracking
- User behavior analytics
- System resource monitoring

## Future Architecture Considerations

### Scalability
- Database integration for large-scale projects
- Distributed processing for large documents
- Cloud-based template storage
- API-based architecture

### Extensibility
- Plugin architecture for custom commands
- Template marketplace integration
- Third-party service integrations
- Custom output format support

### Advanced Features
- Real-time collaboration
- Version control integration
- Automated document updates
- AI-powered content generation
