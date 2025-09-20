# Project Management Commands

Commands for managing the DocGen CLI project lifecycle, tracking progress, and coordinating development activities.

## Project Status Commands

### @project-overview
Shows comprehensive project status and progress.

**Usage**: `@project-overview [detail-level]`

**Examples**:
- `@project-overview` - Shows high-level project status
- `@project-overview detailed` - Shows detailed progress breakdown
- `@project-overview risks` - Shows status with risk assessment

**What it does**:
- Displays current phase and milestone progress
- Shows completed vs. remaining tasks
- Reports spec compliance status
- Identifies blockers and dependencies
- Provides next steps recommendations

### @milestone-status
Shows status of specific milestones or phases.

**Usage**: `@milestone-status [milestone-id]`

**Examples**:
- `@milestone-status phase-1` - Shows Phase 1 status
- `@milestone-status mvp` - Shows MVP milestone status
- `@milestone-status task-1.1` - Shows specific task status

**What it does**:
- Reports milestone completion percentage
- Lists completed and remaining criteria
- Identifies blockers and dependencies
- Shows timeline and progress
- Provides completion estimates

### @task-board
Shows task board view of current development work.

**Usage**: `@task-board [filter]`

**Examples**:
- `@task-board` - Shows all tasks
- `@task-board current` - Shows current phase tasks
- `@task-board blocked` - Shows blocked tasks
- `@task-board completed` - Shows completed tasks

**What it does**:
- Displays tasks in board format (To Do, In Progress, Done)
- Shows task priorities and dependencies
- Identifies blocked or at-risk tasks
- Reports task progress and estimates
- Provides task management insights

## Progress Tracking Commands

### @progress-update
Updates progress for specific tasks or milestones.

**Usage**: `@progress-update [task-id] [status] [notes]`

**Examples**:
- `@progress-update 1.1 completed "All imports fixed and tested"`
- `@progress-update 1.2 in-progress "Working on ProjectManager class"`
- `@progress-update phase-1 75% "Most tasks complete, testing remaining"`

**What it does**:
- Updates task or milestone status
- Records progress notes and updates
- Tracks completion percentages
- Updates timeline estimates
- Maintains progress history

### @progress-report
Generates progress reports for stakeholders.

**Usage**: `@progress-report [scope] [format]`

**Examples**:
- `@progress-report weekly` - Generates weekly progress report
- `@progress-report phase-1 detailed` - Detailed Phase 1 report
- `@progress-report mvp summary` - MVP milestone summary

**What it does**:
- Generates formatted progress reports
- Includes completion metrics and timelines
- Reports on risks and blockers
- Shows quality metrics
- Provides stakeholder updates

### @velocity-track
Tracks development velocity and estimates.

**Usage**: `@velocity-track [period]`

**Examples**:
- `@velocity-track weekly` - Tracks weekly velocity
- `@velocity-track sprint` - Tracks sprint velocity
- `@velocity-track phase` - Tracks phase velocity

**What it does**:
- Calculates development velocity
- Estimates completion times
- Identifies velocity trends
- Reports on productivity metrics
- Provides timeline predictions

## Risk Management Commands

### @risk-identify
Identifies and assesses project risks.

**Usage**: `@risk-identify [risk-category]`

**Examples**:
- `@risk-identify technical` - Identifies technical risks
- `@risk-identify timeline` - Identifies timeline risks
- `@risk-identify quality` - Identifies quality risks

**What it does**:
- Scans for potential risks
- Assesses risk probability and impact
- Categorizes risks by type
- Suggests mitigation strategies
- Updates risk register

### @risk-mitigate
Implements risk mitigation strategies.

**Usage**: `@risk-mitigate [risk-id] [strategy]`

**Examples**:
- `@risk-mitigate import-issues "Add systematic import testing"`
- `@risk-mitigate timeline-delay "Increase testing automation"`
- `@risk-mitigate quality-debt "Schedule refactoring sprint"`

**What it does**:
- Implements specific mitigation strategies
- Tracks mitigation progress
- Monitors risk indicators
- Updates risk status
- Reports mitigation effectiveness

### @risk-monitor
Monitors ongoing risks and indicators.

**Usage**: `@risk-monitor [risk-id]`

**Examples**:
- `@risk-monitor` - Monitors all active risks
- `@risk-monitor high-priority` - Monitors high-priority risks
- `@risk-monitor technical` - Monitors technical risks

**What it does**:
- Tracks risk indicators
- Reports risk status changes
- Alerts on risk escalation
- Updates risk assessments
- Provides risk insights

## Resource Management Commands

### @resource-plan
Plans and allocates development resources.

**Usage**: `@resource-plan [resource-type]`

**Examples**:
- `@resource-plan time` - Plans time allocation
- `@resource-plan tasks` - Plans task allocation
- `@resource-plan dependencies` - Plans dependency management

**What it does**:
- Allocates resources to tasks
- Plans resource dependencies
- Optimizes resource utilization
- Identifies resource conflicts
- Provides resource recommendations

### @dependency-track
Tracks and manages task dependencies.

**Usage**: `@dependency-track [scope]`

**Examples**:
- `@dependency-track` - Tracks all dependencies
- `@dependency-track critical` - Tracks critical dependencies
- `@dependency-track blocked` - Tracks blocking dependencies

**What it does**:
- Maps task dependencies
- Identifies dependency chains
- Tracks dependency status
- Alerts on dependency issues
- Suggests dependency optimization

### @capacity-plan
Plans development capacity and workload.

**Usage**: `@capacity-plan [period]`

**Examples**:
- `@capacity-plan weekly` - Plans weekly capacity
- `@capacity-plan sprint` - Plans sprint capacity
- `@capacity-plan phase` - Plans phase capacity

**What it does**:
- Calculates available capacity
- Plans workload distribution
- Identifies capacity constraints
- Optimizes capacity utilization
- Provides capacity insights

## Communication Commands

### @stakeholder-update
Generates updates for project stakeholders.

**Usage**: `@stakeholder-update [audience] [format]`

**Examples**:
- `@stakeholder-update team` - Updates for development team
- `@stakeholder-update management` - Updates for management
- `@stakeholder-update users` - Updates for end users

**What it does**:
- Generates audience-appropriate updates
- Includes relevant progress metrics
- Highlights key achievements
- Reports on risks and issues
- Provides next steps

### @meeting-prep
Prepares for project meetings and reviews.

**Usage**: `@meeting-prep [meeting-type]`

**Examples**:
- `@meeting-prep daily-standup` - Prepares for daily standup
- `@meeting-prep sprint-review` - Prepares for sprint review
- `@meeting-prep milestone-review` - Prepares for milestone review

**What it does**:
- Gathers relevant project data
- Prepares status updates
- Identifies discussion topics
- Generates meeting agenda
- Provides talking points

### @decision-log
Records and tracks project decisions.

**Usage**: `@decision-log [action] [decision]`

**Examples**:
- `@decision-log record "Use Jinja2 for templating"`
- `@decision-log review` - Reviews recent decisions
- `@decision-log impact` - Analyzes decision impact

**What it does**:
- Records project decisions
- Tracks decision rationale
- Monitors decision outcomes
- Reports decision impact
- Maintains decision history

## Quality Gates Commands

### @gate-check
Checks quality gates before proceeding.

**Usage**: `@gate-check [gate-type]`

**Examples**:
- `@gate-check code-review` - Checks code review gate
- `@gate-check testing` - Checks testing gate
- `@gate-check documentation` - Checks documentation gate

**What it does**:
- Validates quality gate criteria
- Reports gate status
- Identifies gate failures
- Suggests gate improvements
- Tracks gate metrics

### @gate-enforce
Enforces quality gates and standards.

**Usage**: `@gate-enforce [standard]`

**Examples**:
- `@gate-enforce test-coverage` - Enforces 80% test coverage
- `@gate-enforce code-quality` - Enforces code quality standards
- `@gate-enforce documentation` - Enforces documentation standards

**What it does**:
- Enforces quality standards
- Blocks progress if gates fail
- Reports compliance status
- Suggests improvements
- Tracks enforcement metrics

### @gate-report
Reports on quality gate performance.

**Usage**: `@gate-report [period]`

**Examples**:
- `@gate-report weekly` - Weekly gate performance
- `@gate-report phase` - Phase gate performance
- `@gate-report trend` - Gate performance trends

**What it does**:
- Reports gate success rates
- Identifies gate trends
- Analyzes gate effectiveness
- Suggests gate improvements
- Tracks gate metrics

## Release Management Commands

### @release-plan
Plans project releases and versions.

**Usage**: `@release-plan [release-type]`

**Examples**:
- `@release-plan mvp` - Plans MVP release
- `@release-plan v1.0` - Plans version 1.0 release
- `@release-plan patch` - Plans patch release

**What it does**:
- Plans release scope and timeline
- Identifies release requirements
- Maps features to releases
- Plans release activities
- Provides release roadmap

### @release-prep
Prepares for project releases.

**Usage**: `@release-prep [release-id]`

**Examples**:
- `@release-prep mvp` - Prepares MVP release
- `@release-prep v1.0` - Prepares version 1.0 release
- `@release-prep hotfix` - Prepares hotfix release

**What it does**:
- Validates release readiness
- Prepares release artifacts
- Plans release activities
- Coordinates release team
- Provides release checklist

### @release-track
Tracks release progress and status.

**Usage**: `@release-track [release-id]`

**Examples**:
- `@release-track mvp` - Tracks MVP release
- `@release-track v1.0` - Tracks version 1.0 release
- `@release-track all` - Tracks all releases

**What it does**:
- Tracks release progress
- Reports release status
- Identifies release blockers
- Monitors release metrics
- Provides release insights

## Usage Guidelines

1. **Update progress regularly** to maintain accurate tracking
2. **Monitor risks proactively** to prevent issues
3. **Use quality gates** to maintain standards
4. **Plan resources carefully** to optimize efficiency
5. **Communicate frequently** with stakeholders

## Command Workflows

### Daily Project Management:
```
@project-overview
@task-board current
@risk-monitor high-priority
@progress-update [current-task]
```

### Weekly Planning:
```
@velocity-track weekly
@resource-plan weekly
@capacity-plan weekly
@stakeholder-update team
```

### Milestone Management:
```
@milestone-status [milestone]
@gate-check all
@release-prep [milestone]
@progress-report [milestone]
```

### Risk Management:
```
@risk-identify all
@risk-mitigate [high-risk]
@risk-monitor active
@decision-log review
```

These commands provide comprehensive project management capabilities to ensure the DocGen CLI project stays on track, maintains quality, and delivers on time according to the spec-driven development plan.
