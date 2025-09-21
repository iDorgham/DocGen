# Continue Commands

Commands for resuming development work, continuing from previous sessions, and maintaining development momentum in the spec-driven development workflow.

## Session Continuation Commands

### @continue
Resumes development from the last active session or checkpoint.

**Usage**: `@continue [context]`

**Examples**:
- `@continue` - Resumes from last checkpoint
- `@continue task-1.2` - Continues specific task
- `@continue phase-1` - Continues current phase
- `@continue after-break` - Resumes after interruption

**What it does**:
- Retrieves last active development context
- Shows current task status and progress
- Identifies next steps based on previous work
- Restores development environment state
- Provides context for continuing work

### @continue-task
Continues work on a specific task from where it was left off.

**Usage**: `@continue-task [task-id] [context]`

**Examples**:
- `@continue-task 1.1` - Continues Task 1.1
- `@continue-task 1.2 implementation` - Continues Task 1.2 implementation
- `@continue-task 2.1 testing` - Continues Task 2.1 testing phase

**What it does**:
- Shows task progress and current status
- Identifies what was completed and what remains
- Provides next implementation steps
- Restores task-specific context
- Validates task prerequisites

### @continue-phase
Continues work on the current development phase.

**Usage**: `@continue-phase [phase-number] [context]`

**Examples**:
- `@continue-phase 1` - Continues Phase 1 work
- `@continue-phase 2 validation` - Continues Phase 2 validation tasks
- `@continue-phase 3 testing` - Continues Phase 3 testing work

**What it does**:
- Shows phase progress and milestones
- Identifies completed and remaining tasks
- Provides phase-specific next steps
- Validates phase prerequisites
- Shows phase quality gates status

## Context Restoration Commands

### @restore-context
Restores the complete development context from a previous session.

**Usage**: `@restore-context [session-id] [scope]`

**Examples**:
- `@restore-context` - Restores last session context
- `@restore-context session-123` - Restores specific session
- `@restore-context last task` - Restores last task context
- `@restore-context yesterday phase` - Restores yesterday's phase context

**What it does**:
- Retrieves session history and context
- Restores active files and configurations
- Shows previous decisions and progress
- Identifies interrupted workflows
- Provides seamless continuation

### @restore-progress
Restores progress tracking and status from previous work.

**Usage**: `@restore-progress [scope] [timeframe]`

**Examples**:
- `@restore-progress` - Restores all progress
- `@restore-progress tasks` - Restores task progress
- `@restore-progress milestones` - Restores milestone progress
- `@restore-progress last-week` - Restores last week's progress

**What it does**:
- Shows progress since last session
- Identifies completed work
- Updates progress tracking
- Shows velocity and trends
- Provides progress insights

### @restore-state
Restores the development environment state.

**Usage**: `@restore-state [environment] [scope]`

**Examples**:
- `@restore-state` - Restores default environment
- `@restore-state testing` - Restores testing environment
- `@restore-state development` - Restores development environment
- `@restore-state validation` - Restores validation environment

**What it does**:
- Restores development environment
- Shows active configurations
- Identifies environment-specific settings
- Validates environment readiness
- Provides environment status

## Workflow Continuation Commands

### @continue-workflow
Continues a specific development workflow from interruption.

**Usage**: `@continue-workflow [workflow-type] [step]`

**Examples**:
- `@continue-workflow spec-driven` - Continues spec-driven workflow
- `@continue-workflow testing` - Continues testing workflow
- `@continue-workflow validation` - Continues validation workflow
- `@continue-workflow documentation` - Continues documentation workflow

**What it does**:
- Identifies interrupted workflow
- Shows workflow progress
- Provides next workflow steps
- Validates workflow prerequisites
- Restores workflow context

### @continue-implementation
Continues code implementation from where it was left off.

**Usage**: `@continue-implementation [component] [approach]`

**Examples**:
- `@continue-implementation ProjectManager` - Continues ProjectManager implementation
- `@continue-implementation validation systematic` - Continues validation systematically
- `@continue-implementation testing iterative` - Continues testing iteratively

**What it does**:
- Shows implementation progress
- Identifies completed and remaining code
- Provides next implementation steps
- Validates implementation approach
- Shows code quality status

### @continue-testing
Continues testing work from previous session.

**Usage**: `@continue-testing [test-type] [scope]`

**Examples**:
- `@continue-testing unit` - Continues unit testing
- `@continue-testing integration` - Continues integration testing
- `@continue-testing validation` - Continues validation testing
- `@continue-testing performance` - Continues performance testing

**What it does**:
- Shows testing progress and results
- Identifies completed and remaining tests
- Provides next testing steps
- Shows test coverage status
- Validates testing approach

## Session Management Commands

### @session-status
Shows the status of current and previous development sessions.

**Usage**: `@session-status [session-id] [detail-level]`

**Examples**:
- `@session-status` - Shows current session status
- `@session-status last` - Shows last session status
- `@session-status detailed` - Shows detailed session status
- `@session-status session-123` - Shows specific session status

**What it does**:
- Shows session history and status
- Identifies active and completed sessions
- Shows session progress and outcomes
- Provides session insights
- Tracks session metrics

### @session-resume
Resumes a specific development session.

**Usage**: `@session-resume [session-id] [context]`

**Examples**:
- `@session-resume` - Resumes last session
- `@session-resume session-123` - Resumes specific session
- `@session-resume last task` - Resumes last task session
- `@session-resume yesterday` - Resumes yesterday's session

**What it does**:
- Restores session context
- Shows session progress
- Identifies next steps
- Validates session prerequisites
- Provides seamless continuation

### @session-checkpoint
Creates a checkpoint for current development work.

**Usage**: `@session-checkpoint [checkpoint-name] [scope]`

**Examples**:
- `@session-checkpoint` - Creates default checkpoint
- `@session-checkpoint task-1.2-complete` - Creates task checkpoint
- `@session-checkpoint phase-1-milestone` - Creates phase checkpoint
- `@session-checkpoint before-testing` - Creates pre-testing checkpoint

**What it does**:
- Saves current development state
- Creates resumable checkpoint
- Records progress and context
- Enables easy continuation
- Provides checkpoint summary

## Progress Continuation Commands

### @continue-progress
Continues progress tracking from previous session.

**Usage**: `@continue-progress [scope] [timeframe]`

**Examples**:
- `@continue-progress` - Continues all progress tracking
- `@continue-progress tasks` - Continues task progress
- `@continue-progress milestones` - Continues milestone progress
- `@continue-progress last-week` - Continues last week's progress

**What it does**:
- Shows progress since last session
- Updates progress tracking
- Identifies completed work
- Shows progress trends
- Provides progress insights

### @continue-tracking
Continues tracking of specific development metrics.

**Usage**: `@continue-tracking [metric-type] [scope]`

**Examples**:
- `@continue-tracking velocity` - Continues velocity tracking
- `@continue-tracking quality` - Continues quality tracking
- `@continue-tracking coverage` - Continues coverage tracking
- `@continue-tracking performance` - Continues performance tracking

**What it does**:
- Shows tracking progress
- Identifies tracking gaps
- Provides tracking insights
- Updates tracking metrics
- Shows tracking trends

### @continue-metrics
Continues development metrics collection and analysis.

**Usage**: `@continue-metrics [metric-type] [timeframe]`

**Examples**:
- `@continue-metrics development` - Continues development metrics
- `@continue-metrics quality` - Continues quality metrics
- `@continue-metrics performance` - Continues performance metrics
- `@continue-metrics last-month` - Continues last month's metrics

**What it does**:
- Shows metrics progress
- Identifies metrics gaps
- Provides metrics insights
- Updates metrics collection
- Shows metrics trends

## Quality Continuation Commands

### @continue-quality
Continues quality assurance work from previous session.

**Usage**: `@continue-quality [quality-type] [scope]`

**Examples**:
- `@continue-quality` - Continues all quality work
- `@continue-quality testing` - Continues testing quality
- `@continue-quality validation` - Continues validation quality
- `@continue-quality documentation` - Continues documentation quality

**What it does**:
- Shows quality progress
- Identifies quality gaps
- Provides quality insights
- Updates quality metrics
- Shows quality trends

### @continue-validation
Continues validation work from previous session.

**Usage**: `@continue-validation [validation-type] [scope]`

**Examples**:
- `@continue-validation` - Continues all validation
- `@continue-validation spec` - Continues spec validation
- `@continue-validation code` - Continues code validation
- `@continue-validation performance` - Continues performance validation

**What it does**:
- Shows validation progress
- Identifies validation gaps
- Provides validation insights
- Updates validation status
- Shows validation results

### @continue-compliance
Continues compliance checking from previous session.

**Usage**: `@continue-compliance [compliance-type] [scope]`

**Examples**:
- `@continue-compliance` - Continues all compliance
- `@continue-compliance spec` - Continues spec compliance
- `@continue-compliance quality` - Continues quality compliance
- `@continue-compliance security` - Continues security compliance

**What it does**:
- Shows compliance progress
- Identifies compliance gaps
- Provides compliance insights
- Updates compliance status
- Shows compliance results

## Documentation Continuation Commands

### @continue-docs
Continues documentation work from previous session.

**Usage**: `@continue-docs [doc-type] [scope]`

**Examples**:
- `@continue-docs` - Continues all documentation
- `@continue-docs api` - Continues API documentation
- `@continue-docs user` - Continues user documentation
- `@continue-docs developer` - Continues developer documentation

**What it does**:
- Shows documentation progress
- Identifies documentation gaps
- Provides documentation insights
- Updates documentation status
- Shows documentation trends

### @continue-sync
Continues documentation synchronization from previous session.

**Usage**: `@continue-sync [sync-type] [scope]`

**Examples**:
- `@continue-sync` - Continues all synchronization
- `@continue-sync code` - Continues code-doc sync
- `@continue-sync specs` - Continues spec-doc sync
- `@continue-sync examples` - Continues example sync

**What it does**:
- Shows sync progress
- Identifies sync gaps
- Provides sync insights
- Updates sync status
- Shows sync results

## Usage Guidelines

1. **Use @continue regularly** to maintain development momentum
2. **Create checkpoints** with @session-checkpoint before breaks
3. **Restore context** with @restore-context for seamless continuation
4. **Track progress** with @continue-progress for accurate status
5. **Maintain quality** with @continue-quality for consistent standards

## Command Workflows

### Resuming After Break:
```
@continue
@restore-context
@continue-task [task-id]
@continue-progress
```

### Continuing Phase Work:
```
@continue-phase [phase-number]
@continue-workflow spec-driven
@continue-quality
@continue-validation
```

### Resuming Implementation:
```
@continue-implementation [component]
@continue-testing [test-type]
@continue-docs
@continue-sync
```

### Session Management:
```
@session-status
@session-checkpoint [name]
@session-resume [session-id]
@continue-metrics
```

### Quality Continuation:
```
@continue-quality
@continue-validation
@continue-compliance
@continue-tracking quality
```

## Integration with Development Plan

These commands integrate seamlessly with the spec-driven development workflow:

### Phase Continuation:
- Use `@continue-phase` to resume phase work
- Use `@continue-workflow` to resume phase workflows
- Use `@continue-validation` to resume phase validation

### Task Continuation:
- Use `@continue-task` to resume specific tasks
- Use `@continue-implementation` to resume task implementation
- Use `@continue-testing` to resume task testing

### Quality Continuation:
- Use `@continue-quality` to resume quality work
- Use `@continue-compliance` to resume compliance checking
- Use `@continue-validation` to resume validation work

These commands ensure that development work can be seamlessly continued from any interruption point, maintaining momentum and ensuring no work is lost or duplicated.
