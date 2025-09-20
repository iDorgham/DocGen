# Development Workflow Commands

Commands for implementing the spec-driven development workflow, following the development plan phases and ensuring proper implementation practices.

## Phase Management Commands

### @phase-init
Initializes a new development phase with proper setup.

**Usage**: `@phase-init [phase-number] [phase-name]`

**Examples**:
- `@phase-init 1 "Foundation & Core Implementation"`
- `@phase-init 2 "Validation & Error Handling"`
- `@phase-init 3 "Testing & Quality Assurance"`

**What it does**:
- Reviews phase requirements and acceptance criteria
- Sets up development environment for the phase
- Creates phase-specific task tracking
- Validates prerequisites are met
- Establishes phase milestones and checkpoints

### @phase-plan
Plans the implementation approach for a phase.

**Usage**: `@phase-plan [phase-number]`

**Examples**:
- `@phase-plan 1` - Plans Phase 1 implementation
- `@phase-plan 2` - Plans Phase 2 implementation
- `@phase-plan 3` - Plans Phase 3 implementation

**What it does**:
- Analyzes phase requirements and dependencies
- Creates implementation roadmap
- Identifies resource requirements
- Plans task sequencing and dependencies
- Establishes quality gates and checkpoints

### @phase-execute
Executes the planned phase implementation.

**Usage**: `@phase-execute [phase-number] [approach]`

**Examples**:
- `@phase-execute 1 sequential` - Executes Phase 1 sequentially
- `@phase-execute 2 parallel` - Executes Phase 2 with parallel tasks
- `@phase-execute 3 iterative` - Executes Phase 3 iteratively

**What it does**:
- Implements phase tasks according to plan
- Manages task dependencies and sequencing
- Monitors progress and quality
- Handles phase-specific challenges
- Maintains spec traceability

### @phase-validate
Validates phase completion against acceptance criteria.

**Usage**: `@phase-validate [phase-number]`

**Examples**:
- `@phase-validate 1` - Validates Phase 1 completion
- `@phase-validate 2` - Validates Phase 2 completion
- `@phase-validate 3` - Validates Phase 3 completion

**What it does**:
- Reviews all phase acceptance criteria
- Runs comprehensive validation tests
- Checks spec compliance
- Reports completion status
- Identifies any remaining work

## Task Implementation Commands

### @task-analyze
Analyzes a task to understand requirements and approach.

**Usage**: `@task-analyze [task-id]`

**Examples**:
- `@task-analyze 1.1` - Analyzes Task 1.1: Fix Import Dependencies
- `@task-analyze 1.2` - Analyzes Task 1.2: Core Project Management Commands
- `@task-analyze 2.1` - Analyzes Task 2.1: Comprehensive Validation System

**What it does**:
- Reviews task requirements and acceptance criteria
- Identifies dependencies and prerequisites
- Analyzes implementation approach
- Estimates effort and complexity
- Plans task execution strategy

### @task-implement
Implements a specific task following spec requirements.

**Usage**: `@task-implement [task-id] [approach]`

**Examples**:
- `@task-implement 1.1 systematic` - Implements Task 1.1 systematically
- `@task-implement 1.2 iterative` - Implements Task 1.2 iteratively
- `@task-implement 2.1 test-driven` - Implements Task 2.1 with TDD

**What it does**:
- Implements code following spec requirements
- Creates/updates tests for the implementation
- Validates implementation against acceptance criteria
- Maintains spec traceability
- Updates progress tracking

### @task-validate
Validates task completion against acceptance criteria.

**Usage**: `@task-validate [task-id]`

**Examples**:
- `@task-validate 1.1` - Validates Task 1.1 completion
- `@task-validate 1.2` - Validates Task 1.2 completion
- `@task-validate 2.1` - Validates Task 2.1 completion

**What it does**:
- Reviews task acceptance criteria
- Runs task-specific validation tests
- Checks spec compliance
- Reports completion status
- Identifies any remaining work

### @task-integrate
Integrates completed task with existing codebase.

**Usage**: `@task-integrate [task-id]`

**Examples**:
- `@task-integrate 1.1` - Integrates Task 1.1 changes
- `@task-integrate 1.2` - Integrates Task 1.2 changes
- `@task-integrate 2.1` - Integrates Task 2.1 changes

**What it does**:
- Integrates task implementation with existing code
- Resolves integration conflicts
- Updates dependent components
- Runs integration tests
- Validates system functionality

## Spec-Driven Development Commands

### @spec-implement
Implements code directly from specification requirements.

**Usage**: `@spec-implement [requirement-id] [component]`

**Examples**:
- `@spec-implement FR-01 project-management` - Implements FR-01 for project management
- `@spec-implement NFR-01 usability` - Implements NFR-01 for usability
- `@spec-implement Task-1.1 imports` - Implements Task 1.1 for imports

**What it does**:
- Maps specification requirements to code
- Implements features according to specs
- Maintains spec-to-code traceability
- Validates implementation against specs
- Updates spec compliance tracking

### @spec-validate
Validates implementation against specifications.

**Usage**: `@spec-validate [scope] [requirement-id]`

**Examples**:
- `@spec-validate all` - Validates all specifications
- `@spec-validate functional FR-01` - Validates FR-01 implementation
- `@spec-validate non-functional NFR-01` - Validates NFR-01 implementation

**What it does**:
- Checks implementation against spec requirements
- Validates feature completeness
- Reports spec compliance status
- Identifies spec gaps
- Suggests spec improvements

### @spec-trace
Traces requirements through implementation and testing.

**Usage**: `@spec-trace [requirement-id] [scope]`

**Examples**:
- `@spec-trace FR-01 implementation` - Traces FR-01 through implementation
- `@spec-trace NFR-01 testing` - Traces NFR-01 through testing
- `@spec-trace Task-1.1 all` - Traces Task 1.1 through all phases

**What it does**:
- Maps requirements to implementation code
- Identifies test coverage for requirements
- Reports requirement status
- Validates requirement completeness
- Maintains requirement traceability

## Code Implementation Commands

### @code-generate
Generates code following spec requirements and best practices.

**Usage**: `@code-generate [component] [spec-reference]`

**Examples**:
- `@code-generate ProjectManager FR-01` - Generates ProjectManager for FR-01
- `@code-generate DocumentGenerator FR-02` - Generates DocumentGenerator for FR-02
- `@code-generate InputValidator FR-03` - Generates InputValidator for FR-03

**What it does**:
- Generates code according to specifications
- Follows project coding standards
- Includes proper error handling
- Adds comprehensive docstrings
- Implements type hints

### @code-refactor
Refactors code to improve quality and maintainability.

**Usage**: `@code-refactor [component] [reason]`

**Examples**:
- `@code-refactor ProjectManager "Improve error handling"`
- `@code-refactor DocumentGenerator "Optimize performance"`
- `@code-refactor InputValidator "Enhance security"`

**What it does**:
- Refactors code for better quality
- Improves code maintainability
- Optimizes performance
- Enhances security
- Maintains spec compliance

### @code-optimize
Optimizes code for performance and efficiency.

**Usage**: `@code-optimize [component] [optimization-type]`

**Examples**:
- `@code-optimize DocumentGenerator performance` - Optimizes generation performance
- `@code-optimize ProjectManager memory` - Optimizes memory usage
- `@code-optimize InputValidator speed` - Optimizes validation speed

**What it does**:
- Optimizes code performance
- Reduces memory usage
- Improves execution speed
- Maintains functionality
- Validates optimization results

## Testing Integration Commands

### @test-implement
Implements tests for new or modified code.

**Usage**: `@test-implement [component] [test-type]`

**Examples**:
- `@test-implement ProjectManager unit` - Implements unit tests for ProjectManager
- `@test-implement DocumentGenerator integration` - Implements integration tests
- `@test-implement InputValidator validation` - Implements validation tests

**What it does**:
- Creates comprehensive test suites
- Implements unit, integration, and end-to-end tests
- Tests error scenarios and edge cases
- Ensures test coverage requirements
- Validates test quality

### @test-validate
Validates test implementation and coverage.

**Usage**: `@test-validate [scope] [coverage-target]`

**Examples**:
- `@test-validate all 80%` - Validates all tests with 80% coverage
- `@test-validate new 90%` - Validates new code with 90% coverage
- `@test-validate critical 100%` - Validates critical code with 100% coverage

**What it does**:
- Validates test implementation quality
- Checks test coverage requirements
- Identifies missing test scenarios
- Reports test effectiveness
- Suggests test improvements

### @test-execute
Executes test suites with comprehensive reporting.

**Usage**: `@test-execute [test-suite] [reporting-level]`

**Examples**:
- `@test-execute all detailed` - Executes all tests with detailed reporting
- `@test-execute unit summary` - Executes unit tests with summary reporting
- `@test-execute integration verbose` - Executes integration tests with verbose output

**What it does**:
- Executes specified test suites
- Provides comprehensive test reporting
- Identifies test failures and issues
- Reports test performance
- Suggests test improvements

## Quality Assurance Integration Commands

### @quality-check
Performs comprehensive quality checks on code.

**Usage**: `@quality-check [scope] [quality-level]`

**Examples**:
- `@quality-check all high` - Performs high-level quality checks
- `@quality-check new strict` - Performs strict quality checks on new code
- `@quality-check critical comprehensive` - Performs comprehensive checks on critical code

**What it does**:
- Runs linting and style checks
- Performs static analysis
- Checks code complexity
- Validates security practices
- Reports quality metrics

### @quality-improve
Improves code quality based on analysis results.

**Usage**: `@quality-improve [component] [improvement-type]`

**Examples**:
- `@quality-improve ProjectManager complexity` - Reduces complexity in ProjectManager
- `@quality-improve DocumentGenerator security` - Improves security in DocumentGenerator
- `@quality-improve InputValidator maintainability` - Improves maintainability

**What it does**:
- Improves code quality metrics
- Reduces complexity and technical debt
- Enhances security and reliability
- Improves maintainability
- Validates quality improvements

### @quality-validate
Validates quality improvements and standards compliance.

**Usage**: `@quality-validate [scope] [standard]`

**Examples**:
- `@quality-validate all pep8` - Validates PEP 8 compliance
- `@quality-validate new security` - Validates security standards
- `@quality-validate critical performance` - Validates performance standards

**What it does**:
- Validates quality standards compliance
- Checks improvement effectiveness
- Reports quality metrics
- Identifies remaining issues
- Suggests further improvements

## Documentation Integration Commands

### @doc-implement
Implements documentation for new or modified code.

**Usage**: `@doc-implement [component] [doc-type]`

**Examples**:
- `@doc-implement ProjectManager api` - Implements API documentation
- `@doc-implement DocumentGenerator usage` - Implements usage documentation
- `@doc-implement InputValidator examples` - Implements example documentation

**What it does**:
- Creates comprehensive documentation
- Implements API documentation
- Creates usage examples
- Documents best practices
- Validates documentation quality

### @doc-sync
Synchronizes documentation with code changes.

**Usage**: `@doc-sync [scope] [sync-level]`

**Examples**:
- `@doc-sync all automatic` - Automatically syncs all documentation
- `@doc-sync new manual` - Manually syncs new code documentation
- `@doc-sync critical comprehensive` - Comprehensively syncs critical documentation

**What it does**:
- Synchronizes documentation with code
- Updates API documentation
- Refreshes usage examples
- Validates documentation accuracy
- Reports documentation status

### @doc-validate
Validates documentation quality and completeness.

**Usage**: `@doc-validate [scope] [validation-level]`

**Examples**:
- `@doc-validate all comprehensive` - Comprehensively validates all documentation
- `@doc-validate new basic` - Basic validation of new documentation
- `@doc-validate critical strict` - Strict validation of critical documentation

**What it does**:
- Validates documentation completeness
- Checks documentation accuracy
- Tests documentation examples
- Reports documentation quality
- Suggests documentation improvements

## Usage Guidelines

1. **Follow phase sequence** - Complete phases in order
2. **Implement spec-driven** - Always reference specifications
3. **Validate continuously** - Check quality at each step
4. **Test thoroughly** - Ensure comprehensive test coverage
5. **Document completely** - Maintain up-to-date documentation

## Command Workflows

### Starting a New Phase:
```
@phase-init [phase-number]
@phase-plan [phase-number]
@phase-execute [phase-number]
@phase-validate [phase-number]
```

### Implementing a Task:
```
@task-analyze [task-id]
@spec-implement [requirement-id]
@code-generate [component]
@test-implement [component]
@task-validate [task-id]
```

### Quality Assurance:
```
@quality-check [scope]
@test-validate [scope]
@doc-validate [scope]
@spec-validate [scope]
```

### Continuous Integration:
```
@code-generate [component]
@test-implement [component]
@quality-check [scope]
@doc-sync [scope]
```

These commands provide a comprehensive workflow for implementing the spec-driven development plan, ensuring that every aspect of development follows the established specifications and maintains high quality standards.
