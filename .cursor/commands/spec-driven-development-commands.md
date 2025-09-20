# DocGen CLI - Spec-Driven Development Commands

This directory contains comprehensive .cursor commands to support the Spec-Driven Development Plan for the DocGen CLI project. These commands ensure that all development follows the established specifications and maintains high quality standards.

## Command Categories

### 📋 [Spec-Driven Development](./spec-driven-dev.md)
Core commands for managing specifications, development phases, and ensuring spec compliance.

**Key Commands:**
- `@spec-validate` - Validates implementation against specifications
- `@phase-start` - Initiates new development phases
- `@task-implement` - Implements tasks with spec traceability
- `@milestone-check` - Validates milestone completion

### 🔄 [Development Workflow](./development-workflow.md)
Commands for implementing the development workflow, managing phases, and following best practices.

**Key Commands:**
- `@phase-init` - Initializes development phases
- `@task-analyze` - Analyzes task requirements
- `@spec-implement` - Implements from specifications
- `@code-generate` - Generates spec-compliant code

### 🎯 [Project Management](./project-management.md)
Commands for managing project lifecycle, tracking progress, and coordinating development activities.

**Key Commands:**
- `@project-overview` - Shows comprehensive project status
- `@progress-update` - Updates task and milestone progress
- `@risk-identify` - Identifies and assesses project risks
- `@stakeholder-update` - Generates stakeholder updates

### ✅ [Quality Assurance](./quality-assurance.md)
Commands for maintaining code quality, testing, and validation throughout development.

**Key Commands:**
- `@test-coverage` - Checks test coverage requirements
- `@quality-check` - Performs comprehensive quality checks
- `@security-scan` - Scans for security vulnerabilities
- `@performance-validate` - Validates performance requirements

## Quick Start Guide

### For New Developers
1. **Start with project overview**: `@project-overview`
2. **Understand current phase**: `@phase-status current`
3. **Review specifications**: `@spec-validate all`
4. **Check quality gates**: `@gate-check all`

### For Daily Development
1. **Check project status**: `@project-overview`
2. **Review current tasks**: `@task-board current`
3. **Implement tasks**: `@task-implement [task-id]`
4. **Validate quality**: `@quality-check new`

### For Phase Completion
1. **Validate phase**: `@phase-validate [phase-number]`
2. **Check milestones**: `@milestone-check [milestone-id]`
3. **Run quality gates**: `@gate-check all`
4. **Generate reports**: `@progress-report [phase]`

## Command Usage Patterns

### Spec-Driven Development Pattern
```
@spec-trace [requirement-id]
@spec-implement [requirement-id]
@spec-validate [scope]
@test-spec-compliance
```

### Task Implementation Pattern
```
@task-analyze [task-id]
@task-implement [task-id]
@task-validate [task-id]
@task-integrate [task-id]
```

### Quality Assurance Pattern
```
@quality-check [scope]
@test-coverage [scope]
@security-scan [scope]
@performance-validate [scope]
```

### Project Management Pattern
```
@project-overview
@progress-update [task-id]
@risk-monitor [risk-type]
@stakeholder-update [audience]
```

## Integration with Development Plan

These commands are designed to work seamlessly with the [Spec-Driven Development Plan](../SPEC_DRIVEN_DEVELOPMENT_PLAN.md):

### Phase 1: Foundation & Core Implementation
- Use `@phase-init 1` to start Phase 1
- Use `@task-implement 1.1` for import dependency fixes
- Use `@task-implement 1.2` for project management commands
- Use `@task-implement 1.3` for document generation core

### Phase 2: Validation & Error Handling
- Use `@phase-init 2` to start Phase 2
- Use `@task-implement 2.1` for validation system
- Use `@task-implement 2.2` for error handling
- Use `@quality-check all` for quality validation

### Phase 3: Testing & Quality Assurance
- Use `@phase-init 3` to start Phase 3
- Use `@test-implement` for comprehensive testing
- Use `@quality-validate` for quality assurance
- Use `@doc-sync` for documentation

## Best Practices

### 1. Always Start with Specs
- Use `@spec-validate` before implementing
- Use `@spec-trace` to understand requirements
- Use `@spec-implement` for spec-driven development

### 2. Follow the Development Plan
- Use `@phase-start` for new phases
- Use `@task-implement` for structured development
- Use `@milestone-check` for validation

### 3. Maintain Quality Standards
- Use `@quality-check` regularly
- Use `@test-coverage` to ensure 80% coverage
- Use `@security-scan` for security validation

### 4. Track Progress Continuously
- Use `@progress-update` for task updates
- Use `@risk-monitor` for risk management
- Use `@stakeholder-update` for communication

### 5. Validate Before Proceeding
- Use `@gate-check` before major milestones
- Use `@phase-validate` before phase completion
- Use `@spec-validate` for spec compliance

## Command Reference

### Quick Reference by Category

#### Spec Management
- `@spec-validate` - Validate against specs
- `@spec-update` - Update specifications
- `@spec-trace` - Trace requirements

#### Development Workflow
- `@phase-start` - Start development phase
- `@task-implement` - Implement task
- `@milestone-check` - Check milestone

#### Project Management
- `@project-overview` - Project status
- `@progress-update` - Update progress
- `@risk-identify` - Identify risks

#### Quality Assurance
- `@test-coverage` - Check test coverage
- `@quality-check` - Quality validation
- `@security-scan` - Security scanning

### Command Parameters

Most commands support optional parameters:
- `[scope]` - Limit to specific components (e.g., `new`, `all`, `critical`)
- `[detail-level]` - Control output detail (e.g., `summary`, `detailed`, `verbose`)
- `[format]` - Specify output format (e.g., `markdown`, `json`, `table`)

## Troubleshooting

### Common Issues

1. **Command not found**: Ensure you're using the correct command name and parameters
2. **Spec validation fails**: Check that specifications are up to date and complete
3. **Quality checks fail**: Review the specific quality issues and address them
4. **Progress tracking issues**: Ensure task IDs and milestone IDs are correct

### Getting Help

1. **Command help**: Most commands provide help with `@command-name help`
2. **Spec reference**: Check the [Spec-Driven Development Plan](../SPEC_DRIVEN_DEVELOPMENT_PLAN.md)
3. **Quality standards**: Review the [Quality Assurance](./quality-assurance.md) commands
4. **Project status**: Use `@project-overview` for current status

## Contributing

When adding new commands:

1. **Follow naming conventions**: Use descriptive, action-oriented names
2. **Include comprehensive help**: Provide clear usage examples
3. **Maintain spec traceability**: Link commands to specifications
4. **Update documentation**: Keep this README and command files current

## Support

For questions or issues with these commands:

1. **Check the development plan**: Review the [Spec-Driven Development Plan](../SPEC_DRIVEN_DEVELOPMENT_PLAN.md)
2. **Review specifications**: Check the `specs/` directory
3. **Use project status**: Run `@project-overview` for current information
4. **Validate setup**: Use `@spec-validate all` to check project status

---

These commands are designed to make spec-driven development efficient, reliable, and maintainable. Use them consistently throughout the development process to ensure the highest quality results.
