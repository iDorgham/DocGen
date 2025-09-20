# Quick Reference - DocGen CLI Commands

## 🚀 Most Used Commands

### Project Status & Overview
```bash
@project-overview              # Show comprehensive project status
@task-board current           # Show current tasks
@milestone-status phase-1     # Show phase status
@progress-update 1.1 completed "Task done"  # Update progress
```

### Session Continuation
```bash
@continue                     # Resume from last checkpoint
@continue-task 1.1           # Continue specific task
@continue-phase 1            # Continue current phase
@restore-context             # Restore development context
```

### Spec-Driven Development
```bash
@spec-validate all            # Validate against all specs
@spec-trace FR-01             # Trace specific requirement
@spec-implement FR-01 project # Implement from spec
@phase-start 1                # Start Phase 1
```

### Task Implementation
```bash
@task-analyze 1.1             # Analyze task requirements
@task-implement 1.1           # Implement task
@task-validate 1.1            # Validate task completion
@task-integrate 1.1           # Integrate with codebase
```

### Quality Assurance
```bash
@test-coverage                # Check test coverage
@quality-check new            # Check new code quality
@security-scan                # Scan for security issues
@performance-validate         # Validate performance
```

### Development Workflow
```bash
@code-generate ProjectManager FR-01  # Generate spec-compliant code
@test-implement ProjectManager unit  # Implement tests
@doc-sync                      # Sync documentation
@gate-check all               # Check quality gates
```

## 📋 Daily Workflow Commands

### Morning Standup
```bash
@project-overview
@task-board current
@risk-monitor high-priority
```

### During Development
```bash
@spec-validate [component]
@task-implement [task-id]
@quality-check new
@test-coverage new
```

### Before Commit
```bash
@pre-commit-check
@security-scan new
@test-run all
@doc-sync
```

### End of Day
```bash
@progress-update [current-task]
@session-checkpoint [checkpoint-name]
@risk-monitor
@stakeholder-update team
```

### Resuming Work
```bash
@continue
@restore-context
@continue-task [task-id]
@continue-progress
```

## 🎯 Phase-Specific Commands

### Phase 1: Foundation & Core Implementation
```bash
@phase-init 1
@task-implement 1.1  # Fix imports
@task-implement 1.2  # Project management
@task-implement 1.3  # Document generation
@phase-validate 1
```

### Phase 2: Validation & Error Handling
```bash
@phase-init 2
@task-implement 2.1  # Validation system
@task-implement 2.2  # Error handling
@quality-check all
@phase-validate 2
```

### Phase 3: Testing & Quality Assurance
```bash
@phase-init 3
@test-implement all
@quality-validate all
@doc-sync all
@phase-validate 3
```

## 🔍 Troubleshooting Commands

### When Things Go Wrong
```bash
@project-overview risks       # Check project risks
@risk-identify technical      # Identify technical risks
@quality-report critical      # Check critical issues
@spec-validate all           # Validate spec compliance
```

### When Stuck
```bash
@next-steps                   # Get next steps guidance
@task-analyze [task-id]       # Analyze current task
@spec-trace [requirement-id]  # Trace requirements
@stakeholder-update team      # Get team input
```

### When Resuming Work
```bash
@continue                     # Resume from last checkpoint
@restore-context             # Restore development context
@session-status              # Check session status
@continue-progress           # Continue progress tracking
```

### When Validating
```bash
@milestone-check [milestone]  # Check milestone completion
@gate-check all              # Check all quality gates
@integration-test all        # Run integration tests
@deployment-prep mvp         # Prepare for deployment
```

## 📊 Reporting Commands

### Progress Reports
```bash
@progress-report weekly       # Weekly progress
@progress-report phase-1      # Phase 1 progress
@velocity-track weekly        # Development velocity
@quality-report              # Quality metrics
```

### Stakeholder Updates
```bash
@stakeholder-update team      # Team update
@stakeholder-update management # Management update
@stakeholder-update users     # User update
@meeting-prep daily-standup   # Meeting preparation
```

## 🛠️ Utility Commands

### Code Quality
```bash
@lint-check                  # Code linting
@type-check                  # Type checking
@code-refactor [component]   # Refactor code
@code-optimize [component]   # Optimize code
```

### Documentation
```bash
@doc-validate                # Validate docs
@doc-test                    # Test documentation
@generate-examples           # Generate examples
@doc-sync                    # Sync documentation
```

### Testing
```bash
@test-run unit              # Run unit tests
@test-run integration       # Run integration tests
@test-generate [component]  # Generate tests
@test-validate [scope]      # Validate tests
```

### Session Management
```bash
@continue                   # Resume development
@continue-task [task-id]    # Continue specific task
@session-checkpoint [name]  # Create checkpoint
@restore-context           # Restore context
```

## 🎨 Command Patterns

### Spec-Driven Development
```bash
@spec-trace [req] → @spec-implement [req] → @spec-validate [req] → @test-spec-compliance
```

### Task Implementation
```bash
@task-analyze [task] → @task-implement [task] → @task-validate [task] → @task-integrate [task]
```

### Quality Assurance
```bash
@quality-check [scope] → @test-coverage [scope] → @security-scan [scope] → @performance-validate [scope]
```

### Phase Management
```bash
@phase-init [phase] → @phase-plan [phase] → @phase-execute [phase] → @phase-validate [phase]
```

### Session Continuation
```bash
@continue → @restore-context → @continue-task [task] → @continue-progress
```

## 📝 Command Parameters

### Common Parameters
- `[scope]`: `all`, `new`, `current`, `critical`
- `[detail-level]`: `summary`, `detailed`, `verbose`
- `[format]`: `markdown`, `json`, `table`
- `[component]`: Component name (e.g., `ProjectManager`, `DocumentGenerator`)

### Task/Milestone IDs
- `1.1`, `1.2`, `1.3` - Phase 1 tasks
- `2.1`, `2.2` - Phase 2 tasks
- `3.1`, `3.2` - Phase 3 tasks
- `phase-1`, `phase-2`, `phase-3` - Phase milestones
- `mvp` - MVP milestone

### Requirement IDs
- `FR-01`, `FR-02`, `FR-03`, `FR-04` - Functional requirements
- `NFR-01`, `NFR-02`, `NFR-03`, `NFR-04`, `NFR-05` - Non-functional requirements

## 🚨 Emergency Commands

### When Project is Blocked
```bash
@project-overview risks
@risk-identify all
@next-steps emergency
@stakeholder-update management
```

### When Quality is Compromised
```bash
@quality-report critical
@gate-check all
@security-scan all
@performance-validate all
```

### When Specs are Out of Sync
```bash
@spec-validate all
@spec-update [type] [description]
@spec-trace [requirement-id]
@doc-sync all
```

## 💡 Pro Tips

1. **Always start with specs**: Use `@spec-validate` before implementing
2. **Update progress regularly**: Use `@progress-update` frequently
3. **Check quality continuously**: Use `@quality-check new` for new code
4. **Monitor risks proactively**: Use `@risk-monitor` regularly
5. **Validate before proceeding**: Use `@gate-check` before milestones

## 🔗 Related Files

- [Spec-Driven Development Plan](../SPEC_DRIVEN_DEVELOPMENT_PLAN.md)
- [Specifications](../specs/)
- [Quality Assurance](./quality-assurance.md)
- [Project Management](./project-management.md)
- [Development Workflow](./development-workflow.md)

---

**Remember**: These commands are designed to make spec-driven development efficient and reliable. Use them consistently to maintain high quality and ensure project success.
