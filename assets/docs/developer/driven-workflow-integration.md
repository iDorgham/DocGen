# Driven Workflow Integration Guide for DocGen CLI

## Overview
This guide provides comprehensive documentation for integrating and utilizing the Driven workflow principles within the DocGen CLI project. Driven workflow enhances development efficiency, quality, and traceability through automated spec-driven development, agent hooks, project steering, optimized MCP integration, and traceable AI output.

## Core Driven Principles

### 1. Spec-Driven Development (Driven-Spec)
- **Principle**: All development starts from structured specifications (requirements, technical designs, tasks). Code changes are directly traceable to these specs.
- **DocGen CLI Integration**: 
  - Automated validation of code against `assets/specs/requirements.md` and `assets/specs/technical/technical.md`
  - Tracking of spec evolution and impact on implementation
  - Commands like `@spec-driven-validate` and `@spec-driven-trace` provide enhanced spec compliance and traceability

### 2. Agent Hooks (Driven-Hooks)
- **Principle**: Automated, event-driven workflows for routine development tasks, triggered by specific events (e.g., pre-commit, post-task completion).
- **DocGen CLI Integration**:
  - Custom agent hooks can be registered using `@hooks-register` to automate tasks like linting, testing, and documentation updates
  - Hooks are integrated into the `assets/specs/development_workflow.md` phases

### 3. Project Steering (Driven-Steer)
- **Principle**: Maintaining consistency and alignment with project context, coding standards, and architectural decisions.
- **DocGen CLI Integration**:
  - Commands like `@steering-context` and `@steering-enforce` help maintain project context and enforce coding standards (e.g., PEP 8)
  - Key decisions are tracked using `@steering-decisions`

### 4. MCP Integration Optimization (Driven-MCP)
- **Principle**: Intelligent integration and optimization of Model Context Protocol (MCP) servers for knowledge management, testing, and documentation.
- **DocGen CLI Integration**:
  - `assets/dev/config/mcp/mcp_config.yaml` is configured for intelligent MCP server selection
  - Commands like `@mcp-optimize` and `@mcp-intelligent` facilitate efficient use of Byterover, TestSprite, Context7, and Dart

### 5. AI Traceability (Driven-AI)
- **Principle**: Ensuring every line of AI-generated code or content can be traced back to its originating specification and prompt.
- **DocGen CLI Integration**:
  - Commands like `@ai-trace` and `@ai-audit` provide audit trails for AI-generated code, documentation, and decisions
  - AI outputs are mapped to specifications using `@ai-map`

## Getting Started with Driven Workflow

### 1. Initialize Driven Integration
To set up the Driven workflow for your project, run the initialization command:
```bash
@driven-init
```
This command configures the necessary settings in `assets/dev/config/mcp/mcp_config.yaml` and prepares the environment for Driven-enhanced development.

### 2. Check Driven Status
Verify the status of your Driven integration and its components:
```bash
@driven-status
```
This will provide an overview of enabled components, quality gate compliance, and any recommendations.

### 3. Validate Driven Integration
Perform a comprehensive validation of the entire Driven workflow:
```bash
@driven-validate
```
This command runs checks across all Driven components, ensuring proper functionality and integration.

## Using Driven-Enhanced Commands

### Spec-Driven Development
- **Enhanced Validation**: Use `@spec-driven-validate [component]` to validate code against specs with stricter Driven compliance gates
- **AI-Powered Traceability**: Use `@spec-driven-trace [requirement-id]` to trace requirements, including AI-generated code and decisions
- **Spec Evolution**: Use `@spec-driven-evolve [type] [description]` to update specs and track their evolution

### Agent Hooks
- **Register Hooks**: `@hooks-register [hook-name] [event-trigger] [script-path]` to automate tasks
- **Execute Hooks**: `@hooks-execute [hook-name]` to manually trigger a hook
- **Monitor Hooks**: `@hooks-monitor` to view hook execution status and performance

### Project Steering
- **Manage Context**: `@steering-context get` or `@steering-context update "New guideline"` to maintain project context
- **Enforce Standards**: `@steering-enforce pep8` or `@steering-enforce architecture` to ensure compliance
- **Log Decisions**: `@steering-decisions log "Decision: Adopt new testing framework"` to track key choices

### MCP Integration
- **Optimize MCP Usage**: `@mcp-optimize` to intelligently select and configure MCP servers
- **Intelligent Queries**: `@mcp-intelligent "How to refactor this module?"` for context-aware information retrieval
- **Knowledge Management**: `@mcp-knowledge store "New design pattern"` or `@mcp-knowledge retrieve "CLI best practices"` for automated knowledge handling

### AI Traceability
- **Trace AI Output**: `@ai-trace [ai-output-id]` to link AI-generated content to its source
- **Audit AI Quality**: `@ai-audit all` or `@ai-audit code` to check AI outputs against quality standards
- **Map AI to Specs**: `@ai-map [ai-output-id] [spec-id]` to explicitly link AI content to requirements

## Best Practices

### Regular Validation
- Run `@driven-validate` and `@spec-driven-validate` frequently to ensure continuous compliance
- Use `@quality-driven-gates` for comprehensive quality assurance

### Documentation
- Use `@mcp-knowledge store` and `@steering-decisions log` to maintain a rich knowledge base
- Keep AI outputs traceable with `@ai-map` and `@ai-trace`

### Automation
- Identify repetitive tasks and automate them using `@hooks-register`
- Use `@workflow-automate` to set up comprehensive automated workflows

### Monitoring
- Utilize `@workflow-monitor` and `@hooks-monitor` to ensure efficient workflow execution
- Generate regular `@compliance-report` for continuous improvement

## Troubleshooting

### Driven Initialization Errors
- Ensure `mcp_config.yaml` is correctly configured and all MCP servers are accessible
- Check that all required dependencies are installed and properly configured

### Agent Hook Failures
- Verify script paths, permissions, and review `@hooks-monitor` for error logs
- Ensure hooks are properly registered and event triggers are correctly configured

### Traceability Gaps
- Use `@ai-trace` to identify untracked AI outputs
- Verify that AI outputs are properly tagged and linked to specifications using `@ai-map`

### MCP Integration Issues
- Run `@mcp-optimize` to reconfigure MCP server usage
- Check MCP server connectivity and performance using `@mcp-intelligent`

## Advanced Usage

### Custom Agent Hooks
Create custom hooks for project-specific automation:
```bash
@hooks-register custom-lint pre-commit assets/dev/scripts/custom_lint.py
@hooks-register auto-doc post-commit assets/dev/scripts/update_docs.py
```

### Intelligent MCP Queries
Leverage context-aware MCP server selection:
```bash
@mcp-intelligent "How to implement error handling for CLI commands?"
@mcp-intelligent "What are the best practices for Python CLI development?"
```

### Comprehensive Quality Assurance
Run full quality checks with Driven enhancement:
```bash
@quality-driven-gates all
@compliance-report all
@ai-audit all
```

## Integration with Existing Workflows

### Development Phases
Driven workflow integrates seamlessly with the existing development phases in `assets/specs/development_workflow.md`:

1. **Project Initialization**: Enhanced with `@driven-init` and `@driven-status`
2. **Active Development**: Enhanced with `@mcp-optimize` and `@ai-trace`
3. **Testing & Validation**: Enhanced with `@hooks-execute` and `@ai-audit`
4. **Documentation & Knowledge**: Enhanced with `@mcp-knowledge` and `@steering-context`

### MCP Server Integration
Driven workflow optimizes the use of existing MCP servers:
- **Byterover**: Enhanced knowledge management and project memory
- **TestSprite**: Automated testing with intelligent test selection
- **Context7**: Context-aware library documentation retrieval
- **Dart**: Intelligent task management and progress tracking
- **Browser Tools**: Automated quality audits and performance monitoring

## Performance Optimization

### MCP Server Optimization
- Use `@mcp-optimize` to configure optimal MCP server usage
- Monitor performance with `@workflow-monitor`
- Cache frequently accessed knowledge with `@mcp-knowledge`

### Workflow Efficiency
- Automate routine tasks with `@hooks-register`
- Use `@workflow-automate` for comprehensive workflow automation
- Monitor and optimize with `@workflow-monitor`

## Security and Compliance

### AI Output Security
- Use `@ai-audit` to ensure AI outputs meet security standards
- Track all AI decisions with `@ai-trace`
- Map AI outputs to security requirements with `@ai-map`

### Spec Compliance
- Maintain 100% spec compliance with `@spec-driven-validate`
- Track spec evolution with `@spec-driven-evolve`
- Ensure traceability with `@spec-driven-trace`

## Conclusion

The Driven workflow integration provides a comprehensive framework for enhancing the DocGen CLI development process. By leveraging automated spec-driven development, intelligent agent hooks, project steering, optimized MCP integration, and traceable AI output, developers can achieve higher efficiency, better quality, and complete traceability in their development work.

This guide will help you leverage the full potential of Driven workflow integration in your DocGen CLI development.