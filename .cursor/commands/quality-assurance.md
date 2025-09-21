# Quality Assurance Commands

Commands for maintaining code quality, testing, and validation throughout the spec-driven development process.

## Testing Commands

### @test-coverage
Checks and reports test coverage against the 80% requirement.

**Usage**: `@test-coverage [scope]`

**Examples**:
- `@test-coverage` - Shows overall test coverage
- `@test-coverage docgen/commands` - Shows coverage for commands module
- `@test-coverage new` - Shows coverage for recently added code

**What it does**:
- Runs pytest with coverage reporting
- Identifies uncovered code areas
- Suggests additional test cases
- Reports coverage percentage
- Highlights critical uncovered areas

### @test-generate
Generates test cases for new or modified code.

**Usage**: `@test-generate [component]`

**Examples**:
- `@test-generate docgen/commands/project.py` - Generates tests for project commands
- `@test-generate validation` - Generates tests for validation logic
- `@test-generate models` - Generates tests for data models

**What it does**:
- Analyzes code to identify test scenarios
- Generates unit tests for functions and methods
- Creates integration tests for workflows
- Generates error scenario tests
- Ensures test coverage for edge cases

### @test-run
Runs specific test suites with detailed reporting.

**Usage**: `@test-run [test-type] [scope]`

**Examples**:
- `@test-run unit` - Runs all unit tests
- `@test-run integration` - Runs integration tests
- `@test-run validation` - Runs validation tests
- `@test-run performance` - Runs performance tests

**What it does**:
- Executes specified test suite
- Reports test results and failures
- Identifies flaky tests
- Measures test execution time
- Suggests test improvements

## Code Quality Commands

### @lint-check
Runs linting and code style checks.

**Usage**: `@lint-check [scope]`

**Examples**:
- `@lint-check` - Checks all Python files
- `@lint-check docgen/` - Checks docgen package
- `@lint-check new` - Checks recently modified files

**What it does**:
- Runs flake8, black, and isort checks
- Reports style violations
- Suggests code improvements
- Checks for common Python issues
- Validates import organization

### @type-check
Runs type checking with mypy.

**Usage**: `@type-check [scope]`

**Examples**:
- `@type-check` - Checks all files
- `@type-check docgen/models` - Checks data models
- `@type-check new` - Checks recently modified files

**What it does**:
- Validates type hints
- Identifies type errors
- Suggests type improvements
- Checks for missing type annotations
- Reports type safety issues

### @security-scan
Scans for security vulnerabilities and issues.

**Usage**: `@security-scan [scope]`

**Examples**:
- `@security-scan` - Scans entire codebase
- `@security-scan validation` - Scans validation logic
- `@security-scan templates` - Scans template handling

**What it does**:
- Scans for common security issues
- Checks for template injection vulnerabilities
- Validates input sanitization
- Reports security best practices violations
- Suggests security improvements

## Validation Commands

### @validate-inputs
Validates input handling and sanitization.

**Usage**: `@validate-inputs [component]`

**Examples**:
- `@validate-inputs cli` - Validates CLI input handling
- `@validate-inputs templates` - Validates template input handling
- `@validate-inputs project` - Validates project data inputs

**What it does**:
- Tests input validation logic
- Checks for injection vulnerabilities
- Validates data sanitization
- Tests edge cases and malformed inputs
- Reports validation coverage

### @validate-errors
Validates error handling and user experience.

**Usage**: `@validate-errors [scenario]`

**Examples**:
- `@validate-errors validation` - Tests validation error handling
- `@validate-errors file-io` - Tests file operation errors
- `@validate-errors template` - Tests template rendering errors

**What it does**:
- Tests error message clarity
- Validates error recovery mechanisms
- Checks user-friendly error reporting
- Tests exception handling
- Reports error handling effectiveness

### @validate-performance
Validates performance requirements.

**Usage**: `@validate-performance [component]`

**Examples**:
- `@validate-performance generation` - Tests document generation speed
- `@validate-performance cli` - Tests CLI response times
- `@validate-performance validation` - Tests validation performance

**What it does**:
- Measures execution times
- Tests with various data sizes
- Identifies performance bottlenecks
- Validates < 5 second requirement
- Reports performance metrics

## Documentation Quality Commands

### @doc-validate
Validates documentation quality and completeness.

**Usage**: `@doc-validate [doc-type]`

**Examples**:
- `@doc-validate api` - Validates API documentation
- `@doc-validate examples` - Validates usage examples
- `@doc-validate readme` - Validates README quality

**What it does**:
- Checks documentation completeness
- Validates code examples
- Tests documentation accuracy
- Identifies missing documentation
- Reports documentation quality

### @doc-test
Tests documentation examples and code snippets.

**Usage**: `@doc-test [doc-type]`

**Examples**:
- `@doc-test readme` - Tests README examples
- `@doc-test api` - Tests API documentation examples
- `@doc-test tutorials` - Tests tutorial examples

**What it does**:
- Executes code examples from documentation
- Validates example accuracy
- Tests installation instructions
- Checks command examples
- Reports documentation test results

## Cross-Platform Validation Commands

### @platform-test
Tests cross-platform compatibility.

**Usage**: `@platform-test [platform]`

**Examples**:
- `@platform-test windows` - Tests Windows compatibility
- `@platform-test linux` - Tests Linux compatibility
- `@platform-test macos` - Tests macOS compatibility

**What it does**:
- Tests platform-specific functionality
- Validates path handling
- Checks file system operations
- Tests CLI behavior
- Reports platform-specific issues

### @python-version-test
Tests Python version compatibility.

**Usage**: `@python-version-test [version]`

**Examples**:
- `@python-version-test 3.8` - Tests Python 3.8 compatibility
- `@python-version-test 3.9` - Tests Python 3.9 compatibility
- `@python-version-test 3.13` - Tests Python 3.13 compatibility

**What it does**:
- Tests with specific Python versions
- Validates feature compatibility
- Checks dependency compatibility
- Tests import behavior
- Reports version-specific issues

## Continuous Integration Commands

### @ci-validate
Validates CI/CD pipeline readiness.

**Usage**: `@ci-validate [pipeline-stage]`

**Examples**:
- `@ci-validate build` - Validates build process
- `@ci-validate test` - Validates test pipeline
- `@ci-validate deploy` - Validates deployment process

**What it does**:
- Tests build configuration
- Validates test pipeline
- Checks deployment readiness
- Tests automation scripts
- Reports CI/CD issues

### @pre-commit-check
Runs pre-commit validation checks.

**Usage**: `@pre-commit-check [scope]`

**Examples**:
- `@pre-commit-check` - Runs all pre-commit checks
- `@pre-commit-check staged` - Checks only staged files
- `@pre-commit-check new` - Checks new files

**What it does**:
- Runs linting checks
- Validates code formatting
- Checks type hints
- Runs security scans
- Reports pre-commit issues

## Quality Metrics Commands

### @quality-report
Generates comprehensive quality report.

**Usage**: `@quality-report [scope]`

**Examples**:
- `@quality-report` - Generates full quality report
- `@quality-report recent` - Reports on recent changes
- `@quality-report critical` - Reports critical issues only

**What it does**:
- Combines all quality metrics
- Reports test coverage
- Shows code quality scores
- Identifies technical debt
- Provides improvement recommendations

### @quality-trends
Shows quality trends over time.

**Usage**: `@quality-trends [metric]`

**Examples**:
- `@quality-trends coverage` - Shows test coverage trends
- `@quality-trends complexity` - Shows code complexity trends
- `@quality-trends issues` - Shows issue resolution trends

**What it does**:
- Tracks quality metrics over time
- Identifies quality trends
- Reports improvement areas
- Shows regression patterns
- Provides quality insights

## Usage Guidelines

1. **Run quality checks frequently** during development
2. **Use test-coverage** to ensure 80% coverage requirement
3. **Validate inputs and errors** for security and usability
4. **Test cross-platform** compatibility regularly
5. **Generate quality reports** before major milestones

## Command Workflows

### Daily Development:
```
@lint-check new
@type-check new
@test-run unit
@test-coverage new
```

### Before Commit:
```
@pre-commit-check
@security-scan new
@validate-inputs new
@test-run all
```

### Before Release:
```
@quality-report
@platform-test all
@python-version-test all
@ci-validate all
```

### Weekly Quality Review:
```
@quality-trends
@test-coverage
@security-scan
@doc-validate
```

These commands ensure consistent quality throughout the development process and help maintain the high standards required for the DocGen CLI project.
