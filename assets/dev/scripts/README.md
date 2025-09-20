# DocGen CLI Scripts

This directory contains essential development and automation scripts for the DocGen CLI project.

## Essential Scripts

### Core Development
- `dev_helpers.py` - Development utilities and project analysis
- `quick_dev_setup.py` - Quick development environment setup
- `generate_docs.py` - Document generation using templates

### MCP Integration
- `mcp_master_integration.py` - Comprehensive MCP server integration
- `run_mcp_integration.py` - Simple runner for MCP integration

### Quality Assurance
- `advanced_quality_assurance.py` - Comprehensive quality assurance
- `run_quality_checks.py` - Quality checks runner

### Workflow Management
- `workflow_automation.py` - Main workflow automation
- `run_all_scripts.py` - Script orchestrator

## Usage

### Quick Setup
```bash
python assets/dev/scripts/quick_dev_setup.py
```

### Run MCP Integration
```bash
python assets/dev/scripts/run_mcp_integration.py
```

### Run Quality Checks
```bash
python assets/dev/scripts/run_quality_checks.py
```

### Run All Scripts
```bash
python assets/dev/scripts/run_all_scripts.py
```

## Script Organization

All redundant and overlapping scripts have been removed. Only the most comprehensive and essential scripts remain to avoid confusion and maintenance overhead.

## Cleanup Summary

**Removed Scripts:**
- Redundant MCP integration scripts (6 scripts)
- Redundant quality assurance scripts (3 scripts)
- Redundant workflow scripts (4 scripts)
- Demo and basic versions of scripts
- Shell scripts replaced by Python equivalents

**Kept Scripts:**
- 8 essential scripts covering all core functionality
- Most comprehensive versions of each script type
- Clear separation of concerns
