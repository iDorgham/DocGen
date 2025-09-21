# Driven Workflow Commands for DocGen CLI

This file contains .cursor commands to support the Driven Workflow integration for DocGen CLI.

## Driven Core Commands

### @driven-init
Initializes the Driven workflow integration for the current project.

**Usage**: `@driven-init`

**What it does**:
- Configures Driven workflow settings in `mcp_config.yaml`
- Sets up initial agent hooks and project steering parameters
- Validates prerequisites for Driven integration

### @driven-status
Displays the current status of the Driven workflow integration.

**Usage**: `@driven-status`

**What it does**:
- Reports on the status of Driven components (spec validation, agent hooks, etc.)
- Shows current quality gate compliance related to Driven
- Identifies any issues or recommendations for Driven optimization

### @driven-validate
Validates the overall Driven workflow integration and its components.

**Usage**: `@driven-validate`

**What it does**:
- Runs comprehensive checks on all Driven components
- Verifies configuration, agent hook functionality, and traceability
- Provides a detailed report on the integration's health

## Enhanced Spec-Driven Commands

### @spec-driven-validate
Validates current implementation against specifications with Driven's enhanced compliance gates.

**Usage**: `@spec-driven-validate [component]`

**Examples**:
- `@spec-driven-validate` - Validates entire project with Driven gates
- `@spec-driven-validate FR-01` - Validates specific functional requirement

**What it does**:
- Leverages Driven's automated gates for stricter spec compliance
- Provides detailed feedback on traceability and adherence to requirements

### @spec-driven-trace
Traces a specific requirement through the development process with Driven's AI traceability.

**Usage**: `@spec-driven-trace [requirement-id]`

**Examples**:
- `@spec-driven-trace FR-01` - Traces Project Creation requirement with AI insights

**What it does**:
- Shows where a requirement is defined, implemented, and tested
- Includes AI-generated code and decisions in the traceability report

### @spec-driven-evolve
Updates specifications based on implementation discoveries or changes, tracking evolution.

**Usage**: `@spec-driven-evolve [type] [description]`

**Examples**:
- `@spec-driven-evolve requirements "Add new Driven-specific validation rule"`

**What it does**:
- Updates the appropriate spec file
- Logs the change as part of the spec's evolution history

## Agent Hooks Commands

### @hooks-register
Registers a new agent hook for automated workflows.

**Usage**: `@hooks-register [hook-name] [event-trigger] [script-path]`

**Examples**:
- `@hooks-register pre-commit-lint pre-commit assets/dev/scripts/run_lint.py`

**What it does**:
- Adds a new entry to the agent hooks configuration
- Ensures the script is executable and linked to the trigger

### @hooks-execute
Manually executes a registered agent hook.

**Usage**: `@hooks-execute [hook-name]`

**Examples**:
- `@hooks-execute pre-commit-lint`

**What it does**:
- Triggers the specified agent hook script
- Reports on the execution status and any errors

### @hooks-monitor
Monitors the execution and performance of agent hooks.

**Usage**: `@hooks-monitor`

**What it does**:
- Displays a dashboard of recent hook executions
- Reports on success rates, execution times, and errors

## Project Steering Commands

### @steering-context
Retrieves and updates the current project context for steering decisions.

**Usage**: `@steering-context [action] [details]`

**Examples**:
- `@steering-context get` - Retrieves current project context
- `@steering-context update "New architectural decision: use microservices"`

**What it does**:
- Provides relevant project information (specs, rules, decisions)
- Allows updating the context to guide future development

### @steering-enforce
Enforces coding standards and architectural guidelines.

**Usage**: `@steering-enforce [standard-type]`

**Examples**:
- `@steering-enforce pep8` - Enforces PEP 8 compliance
- `@steering-enforce architecture` - Validates against architectural guidelines

**What it does**:
- Runs automated checks to ensure adherence to standards
- Reports on non-compliance and suggests fixes

### @steering-decisions
Tracks and logs key project steering decisions.

**Usage**: `@steering-decisions [action] [decision-details]`

**Examples**:
- `@steering-decisions log "Decision: Use Pydantic for all data models"`

**What it does**:
- Records important project decisions for future reference
- Maintains an audit trail of steering choices

## MCP Integration Commands

### @mcp-optimize
Optimizes MCP server usage for current development context.

**Usage**: `@mcp-optimize`

**What it does**:
- Analyzes the current task and intelligently selects optimal MCP servers
- Configures MCP servers for best performance and relevance

### @mcp-intelligent
Performs an intelligent query across MCP servers based on context.

**Usage**: `@mcp-intelligent [query]`

**Examples**:
- `@mcp-intelligent "How to implement a new CLI command?"`

**What it does**:
- Routes the query to the most relevant MCP servers (Byterover, Context7, etc.)
- Consolidates and presents comprehensive results

### @mcp-knowledge
Manages knowledge storage and retrieval via MCP servers.

**Usage**: `@mcp-knowledge [action] [details]`

**Examples**:
- `@mcp-knowledge store "New pattern for error handling"`
- `@mcp-knowledge retrieve "best practices for CLI design"`

**What it does**:
- Automates interaction with Byterover for knowledge management
- Ensures persistent storage and easy retrieval of development insights

## AI Traceability Commands

### @ai-trace
Traces AI-generated code or content back to its originating specification.

**Usage**: `@ai-trace [ai-output-id]`

**Examples**:
- `@ai-trace code-snippet-123` - Traces a specific AI-generated code block

**What it does**:
- Identifies the spec, task, and prompt that led to the AI output
- Provides an audit trail for AI-driven development

### @ai-audit
Audits AI-generated content for compliance with project rules and quality.

**Usage**: `@ai-audit [scope]`

**Examples**:
- `@ai-audit all` - Audits all recent AI outputs
- `@ai-audit documentation` - Audits AI-generated documentation

**What it does**:
- Checks AI outputs against coding standards, spec compliance, and quality gates
- Reports on any deviations or areas for improvement

### @ai-map
Maps AI-generated content to specific project specifications and tasks.

**Usage**: `@ai-map [ai-output-id] [spec-id]`

**Examples**:
- `@ai-map doc-gen-feature FR-02` - Maps AI-generated feature doc to FR-02

**What it does**:
- Establishes explicit links between AI outputs and project requirements
- Enhances traceability and project steering

## Workflow Automation Commands

### @workflow-automate
Sets up automated workflows for routine development tasks.

**Usage**: `@workflow-automate [workflow-type]`

**Examples**:
- `@workflow-automate testing` - Sets up automated testing workflows
- `@workflow-automate documentation` - Sets up automated documentation workflows

**What it does**:
- Configures automated triggers for common development tasks
- Sets up event-driven workflows for efficiency

### @workflow-monitor
Monitors the performance and effectiveness of automated workflows.

**Usage**: `@workflow-monitor`

**What it does**:
- Displays metrics on workflow execution
- Identifies optimization opportunities
- Reports on workflow effectiveness

## Quality Assurance Commands

### @quality-kiro-gates
Runs Kiro-enhanced quality gates with automated compliance checking.

**Usage**: `@quality-kiro-gates [gate-type]`

**Examples**:
- `@quality-kiro-gates spec-compliance` - Checks spec compliance with Kiro validation
- `@quality-kiro-gates traceability` - Validates traceability completeness

**What it does**:
- Runs enhanced quality checks with Kiro automation
- Provides detailed compliance reports
- Suggests improvements for quality gaps

### @compliance-report
Generates comprehensive compliance reports for all Kiro components.

**Usage**: `@compliance-report [scope]`

**Examples**:
- `@compliance-report all` - Generates full compliance report
- `@compliance-report spec-driven` - Reports on spec-driven development compliance

**What it does**:
- Analyzes compliance across all Kiro workflow components
- Provides actionable recommendations for improvement
- Tracks compliance trends over time

## Integration Commands

### @kiro-integrate
Integrates Kiro workflow with existing development processes.

**Usage**: `@kiro-integrate [component]`

**Examples**:
- `@kiro-integrate mcp` - Integrates Kiro with MCP servers
- `@kiro-integrate testing` - Integrates Kiro with testing workflows

**What it does**:
- Seamlessly integrates Kiro components with existing tools
- Ensures compatibility and optimal performance

### @kiro-sync
Synchronizes Kiro workflow components with project changes.

**Usage**: `@kiro-sync [component]`

**Examples**:
- `@kiro-sync specs` - Syncs Kiro with updated specifications
- `@kiro-sync context` - Updates project context for steering

**What it does**:
- Keeps Kiro components synchronized with project evolution
- Maintains consistency across all workflow components

## Usage Guidelines

### For Kiro Workflow Integration:
1. **Start with @kiro-init** to set up the integration
2. **Use @kiro-status** to monitor integration health
3. **Leverage @spec-kiro-validate** for enhanced spec compliance
4. **Set up @hooks-register** for automated workflows
5. **Use @steering-context** to maintain project direction

### For Enhanced Development:
1. **Use @mcp-optimize** before starting development tasks
2. **Apply @ai-trace** to track AI-generated content
3. **Run @quality-kiro-gates** for comprehensive quality assurance
4. **Use @workflow-automate** to streamline routine tasks

### For Continuous Improvement:
1. **Monitor with @workflow-monitor** for optimization opportunities
2. **Generate @compliance-report** for regular assessments
3. **Use @kiro-sync** to keep components current
4. **Apply @steering-decisions** to track important choices

## Command Combinations

### For Starting Kiro Integration:
```
@kiro-init
@kiro-status
@kiro-validate
@mcp-optimize
```

### For Enhanced Development Workflow:
```
@spec-kiro-validate
@mcp-intelligent "current task context"
@ai-trace [output-id]
@quality-kiro-gates
```

### For Automated Workflow Setup:
```
@hooks-register [hook-name] [trigger] [script]
@workflow-automate [workflow-type]
@steering-context update "project guidelines"
@workflow-monitor
```

These commands provide comprehensive support for Kiro workflow integration, enhancing the existing spec-driven development approach with advanced automation, traceability, and intelligence.