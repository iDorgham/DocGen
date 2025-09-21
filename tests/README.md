# DocGen CLI Test Suite

This directory contains comprehensive tests for the DocGen CLI project, organized to meet the 80% coverage requirement and ensure high-quality software delivery.

## Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── conftest.py                 # Pytest configuration and shared fixtures
├── README.md                   # This file
├── unit/                       # Unit tests
│   ├── __init__.py
│   ├── test_models.py          # Data model tests
│   ├── test_utils.py           # Utility function tests
│   ├── test_core.py            # Core functionality tests
│   └── test_commands.py        # Command handler tests
├── integration/                # Integration tests
│   ├── __init__.py
│   ├── test_workflows.py       # End-to-end workflow tests
│   └── test_performance.py     # Performance requirement tests
└── cli/                        # CLI-specific tests
    ├── __init__.py
    └── test_cli_interface.py   # CLI interface tests
```

## Test Categories

### Unit Tests (`tests/unit/`)
- **Purpose**: Test individual components in isolation
- **Coverage**: All public methods and functions
- **Speed**: Fast execution (< 1 second each)
- **Dependencies**: Mocked external dependencies

**Test Files:**
- `test_models.py`: Project and Template model validation
- `test_utils.py`: File I/O, formatting, and validation utilities
- `test_core.py`: Document generation, template management, validation
- `test_commands.py`: CLI command handlers and argument parsing

### Integration Tests (`tests/integration/`)
- **Purpose**: Test complete workflows and system interactions
- **Coverage**: End-to-end user journeys
- **Speed**: Moderate execution (1-5 seconds each)
- **Dependencies**: Real file system operations

**Test Files:**
- `test_workflows.py`: Complete user workflows from project creation to document generation
- `test_performance.py`: Performance benchmarks and resource usage validation

### CLI Tests (`tests/cli/`)
- **Purpose**: Test command-line interface functionality
- **Coverage**: CLI argument parsing, help systems, error handling
- **Speed**: Fast execution
- **Dependencies**: Click test runner

**Test Files:**
- `test_cli_interface.py`: CLI interface, argument parsing, user interaction

## Running Tests

### Quick Start
```bash
# Run all tests with coverage
python run_tests.py

# Run specific test types
python run_tests.py --type unit
python run_tests.py --type integration
python run_tests.py --type cli

# Run with HTML coverage report
python run_tests.py --coverage --html
```

### Using pytest directly
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_models.py

# Run tests with specific markers
pytest -m unit
pytest -m integration
pytest -m "not slow"
```

### Test Script Options
```bash
python run_tests.py --help

Options:
  --type {unit,integration,cli,all}  Type of tests to run
  --coverage                         Generate coverage report
  --html                            Generate HTML coverage report
  --verbose                         Verbose output
  --fast                           Skip slow tests
  --lint                           Run linting checks
  --format                         Format code with black and isort
```

## Test Configuration

### Pytest Configuration (`pytest.ini`)
- **Test Discovery**: Automatic discovery of test files
- **Coverage**: 80% minimum coverage requirement
- **Markers**: Custom markers for test categorization
- **Timeouts**: 300-second timeout for long-running tests
- **Output**: Verbose output with short tracebacks

### Coverage Configuration
- **Source**: `src/` directory
- **Exclusions**: Test files, virtual environments, cache files
- **Reports**: Terminal, HTML, and XML formats
- **Threshold**: 80% minimum coverage

## Test Fixtures

### Shared Fixtures (`conftest.py`)
- `cli_runner`: Click CLI test runner
- `temp_dir`: Temporary directory for testing
- `sample_project_data`: Sample project data
- `sample_project_yaml`: Sample project YAML file
- `mock_project`: Mock Project instance
- `mock_template`: Mock Template instance
- `mock_file_operations`: Mocked file I/O operations
- `mock_git_operations`: Mocked git operations
- `mock_template_engine`: Mocked Jinja2 template engine
- `test_templates_dir`: Test templates directory
- `test_output_dir`: Test output directory

## Performance Requirements

The test suite validates the following performance requirements:

- **Project Creation**: < 2 seconds
- **Document Generation**: < 5 seconds
- **Project Validation**: < 3 seconds
- **Template Rendering**: < 2 seconds
- **Memory Usage**: < 512MB per operation
- **File Size**: < 10MB per document
- **Concurrent Operations**: < 5 per user

## Quality Gates

### Pre-Commit Gates
- All unit tests must pass
- Code coverage must be ≥ 80%
- Linting checks must pass
- Type checking must pass

### Pre-Deployment Gates
- All tests (unit, integration, CLI) must pass
- Performance benchmarks must be met
- Security validation must pass
- Documentation must be updated

## Test Data

### Sample Data
- **Project Data**: Realistic project information for testing
- **Templates**: Jinja2 templates with various complexity levels
- **Output Files**: Expected output formats and content

### Test Scenarios
- **Valid Inputs**: Normal operation scenarios
- **Invalid Inputs**: Error handling and validation
- **Edge Cases**: Boundary conditions and limits
- **Error Recovery**: Graceful error handling

## Continuous Integration

### Automated Testing
- **Trigger**: On every commit and pull request
- **Execution**: Full test suite with coverage reporting
- **Reporting**: Coverage reports and test results
- **Quality Gates**: Block deployment if tests fail

### Test Maintenance
- **Regular Updates**: Tests updated with code changes
- **Coverage Monitoring**: Continuous coverage tracking
- **Performance Monitoring**: Performance regression detection
- **Test Optimization**: Regular test performance optimization

## Troubleshooting

### Common Issues

**Import Errors**
```bash
# Ensure src is in Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

**Coverage Issues**
```bash
# Check coverage configuration
pytest --cov=src --cov-report=term-missing
```

**Performance Test Failures**
```bash
# Run performance tests separately
pytest tests/integration/test_performance.py -v
```

**Memory Issues**
```bash
# Monitor memory usage
python -m pytest tests/integration/test_performance.py::TestPerformanceRequirements::test_memory_usage_performance -v
```

### Debug Mode
```bash
# Run tests with debug output
pytest -vvv --tb=long

# Run specific test with debug
pytest tests/unit/test_models.py::TestProject::test_project_creation_with_valid_data -vvv
```

## Contributing

### Adding New Tests
1. **Unit Tests**: Add to appropriate `test_*.py` file in `tests/unit/`
2. **Integration Tests**: Add to `tests/integration/`
3. **CLI Tests**: Add to `tests/cli/`
4. **Fixtures**: Add shared fixtures to `conftest.py`

### Test Guidelines
- **Naming**: Use descriptive test names
- **Isolation**: Tests should be independent
- **Mocking**: Mock external dependencies
- **Coverage**: Aim for 100% coverage of new code
- **Documentation**: Document complex test scenarios

### Test Quality
- **Fast**: Unit tests should be fast (< 1 second)
- **Reliable**: Tests should be deterministic
- **Maintainable**: Tests should be easy to understand and modify
- **Comprehensive**: Cover success, failure, and edge cases

## Metrics and Reporting

### Coverage Reports
- **Terminal**: Real-time coverage during test execution
- **HTML**: Detailed coverage report in `htmlcov/`
- **XML**: Machine-readable coverage data

### Test Metrics
- **Execution Time**: Track test performance
- **Coverage Percentage**: Monitor code coverage
- **Test Count**: Track number of tests
- **Failure Rate**: Monitor test reliability

### Quality Metrics
- **Code Quality**: Linting and type checking results
- **Performance**: Benchmark results
- **Security**: Security validation results
- **Maintainability**: Test maintainability scores
