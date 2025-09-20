# Spec-Driven Development Commands

This file contains .cursor commands to support the Spec-Driven Development Plan for DocGen CLI.

## Spec Management Commands

### @spec-validate
Validates that current implementation matches specifications and requirements.

**Usage**: `@spec-validate [component]`

**Examples**:
- `@spec-validate` - Validates entire project against specs
- `@spec-validate project` - Validates project management features
- `@spec-validate generation` - Validates document generation features
- `@spec-validate validation` - Validates error handling and validation

**What it does**:
- Checks if current code implements requirements from `specs/requirements.md`
- Validates technical implementation against `specs/tech.md`
- Ensures tasks from `specs/tasks.md` are being followed
- Reports any gaps between specs and implementation

### @spec-update
Updates specifications based on implementation discoveries or changes.

**Usage**: `@spec-update [type] [description]`

**Examples**:
- `@spec-update requirements "Add new validation requirement for template security"`
- `@spec-update tech "Update architecture to include new error handling module"`
- `@spec-update tasks "Add new milestone for performance optimization"`

**What it does**:
- Updates the appropriate spec file with new information
- Maintains traceability between specs and implementation
- Ensures specs stay current with development progress

### @spec-trace
Traces a specific requirement through the entire development process.

**Usage**: `@spec-trace [requirement-id]`

**Examples**:
- `@spec-trace FR-01` - Traces Project Creation requirement
- `@spec-trace NFR-01` - Traces Usability requirement
- `@spec-trace Task-1.1` - Traces specific task implementation

**What it does**:
- Shows where a requirement is defined in specs
- Identifies which code implements the requirement
- Lists test cases that validate the requirement
- Reports current implementation status

## Development Workflow Commands

### @phase-start
Initiates a new development phase with proper setup and validation.

**Usage**: `@phase-start [phase-number]`

**Examples**:
- `@phase-start 1` - Starts Phase 1: Foundation & Core Implementation
- `@phase-start 2` - Starts Phase 2: Validation & Error Handling
- `@phase-start 3` - Starts Phase 3: Testing & Quality Assurance

**What it does**:
- Reviews phase requirements and acceptance criteria
- Sets up development environment for the phase
- Creates task tracking for phase milestones
- Validates prerequisites are met

### @task-implement
Implements a specific task from the development plan with spec traceability.

**Usage**: `@task-implement [task-id]`

**Examples**:
- `@task-implement 1.1` - Implements Task 1.1: Fix Import Dependencies
- `@task-implement 1.2` - Implements Task 1.2: Core Project Management Commands
- `@task-implement 2.1` - Implements Task 2.1: Comprehensive Validation System

**What it does**:
- Reviews task requirements and acceptance criteria
- Implements code following spec requirements
- Creates/updates tests for the implementation
- Validates implementation against acceptance criteria
- Updates progress tracking

### @milestone-check
Validates that a milestone has been completed according to specifications.

**Usage**: `@milestone-check [milestone-id]`

**Examples**:
- `@milestone-check 1.1` - Checks Task 1.1 completion
- `@milestone-check phase-1` - Checks Phase 1 completion
- `@milestone-check mvp` - Checks MVP milestone

**What it does**:
- Reviews all acceptance criteria for the milestone
- Runs validation tests
- Checks spec compliance
- Reports completion status and any remaining work

## Testing & Validation Commands

### @test-spec-compliance
Runs comprehensive tests to ensure spec compliance.

**Usage**: `@test-spec-compliance [scope]`

**Examples**:
- `@test-spec-compliance all` - Tests all specifications
- `@test-spec-compliance functional` - Tests functional requirements
- `@test-spec-compliance non-functional` - Tests non-functional requirements

**What it does**:
- Runs unit tests for all implemented features
- Validates error handling scenarios
- Tests performance requirements
- Checks cross-platform compatibility
- Reports test coverage and compliance status

### @validate-quality-gates
Validates that all quality gates are met before proceeding.

**Usage**: `@validate-quality-gates [gate-type]`

**Examples**:
- `@validate-quality-gates code-review` - Validates code review checklist
- `@validate-quality-gates test-coverage` - Validates 80% test coverage
- `@validate-quality-gates spec-traceability` - Validates spec-to-code traceability

**What it does**:
- Checks that every function maps to a spec requirement
- Validates error handling and user-friendly messages
- Ensures comprehensive input validation
- Verifies test coverage requirements
- Confirms documentation is updated

### @error-scenario-test
Tests error handling and recovery scenarios.

**Usage**: `@error-scenario-test [scenario-type]`

**Examples**:
- `@error-scenario-test validation` - Tests input validation errors
- `@error-scenario-test recovery` - Tests automatic recovery mechanisms
- `@error-scenario-test security` - Tests security validation scenarios

**What it does**:
- Tests invalid input handling
- Validates error message clarity
- Tests automatic recovery mechanisms
- Checks security validation
- Reports error handling effectiveness

## Project Management Commands

### @project-status
Shows current project status against the development plan.

**Usage**: `@project-status [detail-level]`

**Examples**:
- `@project-status` - Shows high-level status
- `@project-status detailed` - Shows detailed progress
- `@project-status risks` - Shows risk assessment

**What it does**:
- Displays current phase and task progress
- Shows completed vs. remaining milestones
- Identifies any blockers or risks
- Reports spec compliance status
- Suggests next steps

### @risk-assessment
Assesses and mitigates development risks.

**Usage**: `@risk-assessment [risk-type]`

**Examples**:
- `@risk-assessment technical` - Assesses technical risks
- `@risk-assessment process` - Assesses process risks
- `@risk-assessment timeline` - Assesses timeline risks

**What it does**:
- Identifies potential risks from the development plan
- Suggests mitigation strategies
- Monitors risk indicators
- Updates risk status
- Recommends preventive actions

### @next-steps
Provides guidance on next development steps based on current status.

**Usage**: `@next-steps [context]`

**Examples**:
- `@next-steps` - Shows immediate next steps
- `@next-steps after-task-1.1` - Shows steps after completing Task 1.1
- `@next-steps phase-completion` - Shows steps for phase completion

**What it does**:
- Analyzes current development status
- Identifies next logical steps
- Suggests task prioritization
- Provides implementation guidance
- Links to relevant specifications

## Code Quality Commands

### @code-review-checklist
Runs the spec-driven code review checklist.

**Usage**: `@code-review-checklist [file-or-component]`

**Examples**:
- `@code-review-checklist` - Reviews all recent changes
- `@code-review-checklist docgen/commands/project.py` - Reviews specific file
- `@code-review-checklist validation` - Reviews validation components

**What it does**:
- Checks spec requirement mapping
- Validates error handling implementation
- Reviews input validation coverage
- Ensures test coverage
- Verifies documentation updates

### @performance-validate
Validates performance requirements are met.

**Usage**: `@performance-validate [component]`

**Examples**:
- `@performance-validate generation` - Tests document generation performance
- `@performance-validate validation` - Tests validation performance
- `@performance-validate cli` - Tests CLI response times

**What it does**:
- Tests document generation speed (< 5 seconds)
- Validates concurrent project handling
- Checks memory usage
- Reports performance metrics
- Identifies optimization opportunities

## Documentation Commands

### @doc-sync
Synchronizes documentation with current implementation.

**Usage**: `@doc-sync [doc-type]`

**Examples**:
- `@doc-sync` - Syncs all documentation
- `@doc-sync readme` - Updates README.md
- `@doc-sync api` - Updates API documentation
- `@doc-sync examples` - Updates usage examples

**What it does**:
- Updates documentation to match current implementation
- Ensures examples are current and working
- Validates documentation completeness
- Generates missing documentation
- Reports documentation gaps

### @generate-examples
Generates example usage and documentation.

**Usage**: `@generate-examples [example-type]`

**Examples**:
- `@generate-examples cli` - Generates CLI usage examples
- `@generate-examples templates` - Generates template examples
- `@generate-examples workflows` - Generates workflow examples

**What it does**:
- Creates working examples for all features
- Generates sample project data
- Creates template examples
- Documents common workflows
- Ensures examples are tested and working

## Integration Commands

### @integration-test
Runs integration tests for complete workflows.

**Usage**: `@integration-test [workflow]`

**Examples**:
- `@integration-test project-lifecycle` - Tests complete project lifecycle
- `@integration-test document-generation` - Tests document generation workflow
- `@integration-test error-handling` - Tests error handling workflows

**What it does**:
- Tests complete user workflows
- Validates end-to-end functionality
- Tests error scenarios
- Verifies cross-platform compatibility
- Reports integration test results

### @deployment-prep
Prepares the project for deployment and release.

**Usage**: `@deployment-prep [target]`

**Examples**:
- `@deployment-prep mvp` - Prepares MVP release
- `@deployment-prep v1.0` - Prepares version 1.0 release
- `@deployment-prep testing` - Prepares for testing deployment

**What it does**:
- Validates all requirements are met
- Runs comprehensive test suite
- Prepares release documentation
- Validates deployment readiness
- Creates release checklist

## Usage Guidelines

1. **Always start with spec validation** before implementing new features
2. **Use task-implement** for structured development following the plan
3. **Run milestone-check** before considering any phase complete
4. **Use quality gates** to ensure standards are maintained
5. **Keep specs updated** as implementation reveals new requirements

## Command Combinations

### For Starting a New Task:
```
@spec-trace [requirement-id]
@task-implement [task-id]
@test-spec-compliance
@milestone-check [task-id]
```

### For Phase Completion:
```
@milestone-check phase-[number]
@validate-quality-gates all
@integration-test all
@deployment-prep [phase]
```

### For Code Review:
```
@code-review-checklist
@spec-validate
@performance-validate
@doc-sync
```

These commands ensure that every aspect of development follows the spec-driven approach, maintaining traceability, quality, and alignment with the development plan.
