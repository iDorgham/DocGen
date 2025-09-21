# DocGen CLI Template Contracts

## Overview
This document defines the template contracts for the DocGen CLI tool, specifying the template structure, rendering contracts, and template management interfaces that ensure consistent and reliable document generation.

## 1. Template Structure Contracts

### 1.1 Template File Contract

#### Template File Structure
```yaml
TemplateFile:
  file_extension: ".j2"
  encoding: "UTF-8"
  line_ending: "LF"
  max_file_size: 1048576  # 1MB
  
  required_sections:
    - header: "Template metadata and configuration"
    - content: "Main template content"
    - footer: "Template closing and metadata"
  
  optional_sections:
    - imports: "External template imports"
    - macros: "Reusable template functions"
    - filters: "Custom filter definitions"
    - variables: "Default variable definitions"
```

#### Template Header Contract
```yaml
TemplateHeader:
  format: "YAML front matter"
  required_fields:
    - name: "Template identifier"
    - type: "Document type (spec|plan|marketing)"
    - version: "Semantic version"
    - description: "Template description"
  
  optional_fields:
    - author: "Template author"
    - created_at: "Creation date"
    - updated_at: "Last update date"
    - tags: "Template tags"
    - dependencies: "Required templates"
    - variables: "Required variables"
    - filters: "Custom filters"
  
  example: |
    ---
    name: "technical_specification"
    type: "spec"
    version: "1.2.0"
    description: "Comprehensive technical specification template"
    author: "DocGen Team"
    variables:
      - project_name
      - project_description
      - technical_requirements
    ---
```

### 1.2 Template Content Contract

#### Content Structure Requirements
```yaml
ContentStructure:
  document_structure:
    - title: "Document title (required)"
    - metadata: "Document metadata (required)"
    - table_of_contents: "Optional TOC"
    - sections: "Main content sections"
    - appendices: "Optional appendices"
    - references: "Optional references"
  
  section_requirements:
    - heading: "Section heading (required)"
    - content: "Section content (required)"
    - subsections: "Optional subsections"
    - metadata: "Optional section metadata"
  
  content_validation:
    - min_sections: 1
    - max_sections: 50
    - min_content_length: 100
    - max_content_length: 1000000
    - required_sections: ["title", "metadata"]
```

#### Jinja2 Syntax Contract
```yaml
Jinja2Syntax:
  allowed_constructs:
    - variables: "{{ variable_name }}"
    - expressions: "{{ expression }}"
    - filters: "{{ variable | filter }}"
    - conditionals: "{% if condition %}...{% endif %}"
    - loops: "{% for item in list %}...{% endfor %}"
    - includes: "{% include 'template.j2' %}"
    - macros: "{% macro name() %}...{% endmacro %}"
    - blocks: "{% block name %}...{% endblock %}"
    - extends: "{% extends 'base.j2' %}"
  
  forbidden_constructs:
    - exec: "{% exec code %}"
    - eval: "{% eval expression %}"
    - import: "{% import module %}"
    - from: "{% from module import item %}"
    - raw: "{% raw %}...{% endraw %}"
  
  security_restrictions:
    - no_file_access: "Cannot access filesystem"
    - no_network_access: "Cannot make network calls"
    - no_system_commands: "Cannot execute system commands"
    - limited_imports: "Only safe imports allowed"
```

### 1.3 Template Variable Contract

#### Variable Definition Structure
```yaml
VariableDefinition:
  name: string
    pattern: "^[a-zA-Z_][a-zA-Z0-9_]*$"
    max_length: 50
    required: true
  
  type: enum
    values: ["string", "number", "boolean", "array", "object", "date", "datetime"]
    required: true
  
  required: boolean
    default: false
    required: true
  
  default_value: any
    type: matches variable type
    required: false
  
  description: string
    max_length: 200
    required: false
  
  validation_rules: object
    type: ValidationRules
    required: false
  
  example: any
    type: matches variable type
    required: false
```

#### Variable Context Contract
```yaml
VariableContext:
  project_variables:
    - project_name: string (required)
    - project_description: string (optional)
    - project_version: string (optional)
    - project_status: string (optional)
    - created_at: datetime (required)
    - updated_at: datetime (required)
  
  team_variables:
    - team_members: array (optional)
    - project_manager: string (optional)
    - stakeholders: array (optional)
    - contact_info: object (optional)
  
  technical_variables:
    - requirements: array (optional)
    - architecture: object (optional)
    - technologies: array (optional)
    - dependencies: array (optional)
  
  timeline_variables:
    - phases: array (optional)
    - milestones: array (optional)
    - deadlines: array (optional)
    - duration: number (optional)
  
  custom_variables:
    - user_defined: object (optional)
    - template_specific: object (optional)
    - environment_specific: object (optional)
```

## 2. Template Rendering Contracts

### 2.1 Rendering Engine Contract

#### Rendering Process
```yaml
RenderingProcess:
  steps:
    1. template_validation:
       - syntax_check: "Valid Jinja2 syntax"
       - security_check: "No dangerous constructs"
       - dependency_check: "All includes available"
    
    2. context_preparation:
       - variable_validation: "All required variables present"
       - type_coercion: "Convert types as needed"
       - default_application: "Apply default values"
    
    3. template_rendering:
       - environment_setup: "Configure Jinja2 environment"
       - filter_registration: "Register custom filters"
       - template_compilation: "Compile template"
       - content_rendering: "Generate output"
    
    4. output_validation:
       - content_check: "Non-empty output"
       - format_validation: "Valid output format"
       - size_validation: "Within size limits"
    
    5. post_processing:
       - formatting: "Apply output formatting"
       - metadata_injection: "Add generation metadata"
       - checksum_calculation: "Calculate content hash"
```

#### Rendering Environment Contract
```yaml
RenderingEnvironment:
  jinja2_config:
    - autoescape: true
    - trim_blocks: true
    - lstrip_blocks: true
    - keep_trailing_newline: true
    - line_statement_prefix: null
    - line_comment_prefix: null
  
  custom_filters:
    - format_date: "Format date strings"
    - format_number: "Format numbers"
    - format_currency: "Format currency values"
    - format_percentage: "Format percentages"
    - truncate_text: "Truncate long text"
    - markdown_to_html: "Convert markdown to HTML"
    - json_pretty: "Pretty print JSON"
    - yaml_pretty: "Pretty print YAML"
  
  custom_functions:
    - current_date: "Get current date"
    - current_time: "Get current time"
    - random_id: "Generate random ID"
    - slugify: "Convert text to slug"
    - word_count: "Count words in text"
    - reading_time: "Estimate reading time"
  
  security_settings:
    - sandboxed: true
    - no_file_access: true
    - no_network_access: true
    - limited_imports: true
    - max_execution_time: 30  # seconds
    - max_memory_usage: 128   # MB
```

### 2.2 Template Inheritance Contract

#### Template Inheritance Structure
```yaml
TemplateInheritance:
  base_templates:
    - spec_base.j2: "Base for specification templates"
    - plan_base.j2: "Base for project plan templates"
    - marketing_base.j2: "Base for marketing templates"
    - common_base.j2: "Common base for all templates"
  
  inheritance_rules:
    - single_inheritance: "Templates can extend only one base"
    - block_override: "Child templates can override blocks"
    - block_super: "Child templates can call parent blocks"
    - block_append: "Child templates can append to blocks"
    - block_prepend: "Child templates can prepend to blocks"
  
  block_structure:
    - title: "Document title block"
    - metadata: "Document metadata block"
    - content: "Main content block"
    - styles: "CSS styles block"
    - scripts: "JavaScript block"
    - footer: "Document footer block"
```

#### Block Definition Contract
```yaml
BlockDefinition:
  name: string
    pattern: "^[a-zA-Z_][a-zA-Z0-9_]*$"
    max_length: 50
    required: true
  
  type: enum
    values: ["content", "metadata", "style", "script", "structure"]
    required: true
  
  required: boolean
    default: false
    required: true
  
  default_content: string
    required: false
  
  allowed_content: enum
    values: ["html", "markdown", "text", "css", "javascript", "any"]
    default: "any"
    required: true
  
  validation_rules: object
    type: ContentValidationRules
    required: false
```

### 2.3 Template Include Contract

#### Include Structure
```yaml
IncludeStructure:
  include_types:
    - partial: "Include template partials"
    - component: "Include reusable components"
    - section: "Include document sections"
    - macro: "Include macro definitions"
  
  include_syntax:
    - simple: "{% include 'template.j2' %}"
    - with_context: "{% include 'template.j2' with context %}"
    - with_variables: "{% include 'template.j2' var1=value1 %}"
    - ignore_missing: "{% include 'template.j2' ignore missing %}"
  
  include_validation:
    - path_validation: "Include path must be valid"
    - circular_dependency: "Prevent circular includes"
    - max_depth: "Maximum include depth: 10"
    - max_includes: "Maximum includes per template: 50"
```

#### Include Security Contract
```yaml
IncludeSecurity:
  allowed_paths:
    - templates/: "Template directory only"
    - components/: "Component directory only"
    - partials/: "Partial directory only"
  
  forbidden_paths:
    - ../: "Parent directory access"
    - /: "Root directory access"
    - ~/: "Home directory access"
    - system/: "System directory access"
  
  path_validation:
    - relative_only: true
    - no_dot_dot: true
    - whitelist_only: true
    - extension_check: ".j2 files only"
```

## 3. Template Management Contracts

### 3.1 Template Storage Contract

#### Template File Organization
```yaml
TemplateFileOrganization:
  directory_structure:
    templates/
      base/
        - common_base.j2
        - spec_base.j2
        - plan_base.j2
        - marketing_base.j2
      spec/
        - technical_spec.j2
        - api_spec.j2
        - user_spec.j2
      plan/
        - project_plan.j2
        - sprint_plan.j2
        - release_plan.j2
      marketing/
        - product_overview.j2
        - feature_highlight.j2
        - case_study.j2
      components/
        - header.j2
        - footer.j2
        - navigation.j2
        - metadata.j2
      partials/
        - requirements.j2
        - timeline.j2
        - team.j2
        - risks.j2
  
  file_naming:
    - format: "snake_case.j2"
    - max_length: 100
    - allowed_chars: "a-z, 0-9, _, -"
    - descriptive: "Name should describe purpose"
```

#### Template Metadata Contract
```yaml
TemplateMetadata:
  metadata_file: "template_metadata.yaml"
  location: "templates/ directory"
  
  required_fields:
    - name: "Template identifier"
    - type: "Document type"
    - version: "Semantic version"
    - description: "Template description"
  
  optional_fields:
    - author: "Template author"
    - created_at: "Creation date"
    - updated_at: "Last update date"
    - tags: "Template tags"
    - dependencies: "Required templates"
    - variables: "Required variables"
    - filters: "Custom filters"
    - examples: "Usage examples"
    - changelog: "Version history"
  
  validation_rules:
    - yaml_syntax: "Valid YAML syntax"
    - required_fields: "All required fields present"
    - version_format: "Semantic versioning"
    - unique_name: "Unique template name"
```

### 3.2 Template Versioning Contract

#### Version Management
```yaml
VersionManagement:
  versioning_scheme: "Semantic Versioning (SemVer)"
  format: "MAJOR.MINOR.PATCH"
  
  version_rules:
    - major: "Breaking changes to template structure"
    - minor: "New features, backward compatible"
    - patch: "Bug fixes, backward compatible"
  
  version_validation:
    - format_check: "Valid SemVer format"
    - increment_check: "Version must increment"
    - changelog_required: "Changelog entry required"
    - migration_guide: "Breaking changes need migration guide"
  
  version_history:
    - storage: "template_metadata.yaml"
    - format: "YAML array"
    - retention: "All versions kept"
    - access: "Version history queryable"
```

#### Template Migration Contract
```yaml
TemplateMigration:
  migration_triggers:
    - version_upgrade: "Template version changed"
    - breaking_changes: "Incompatible changes detected"
    - user_request: "Manual migration requested"
  
  migration_process:
    1. backup_current: "Backup existing template"
    2. validate_migration: "Check migration requirements"
    3. apply_migration: "Apply migration rules"
    4. validate_result: "Verify migration success"
    5. update_metadata: "Update template metadata"
  
  migration_rules:
    - backward_compatibility: "Maintain backward compatibility when possible"
    - data_preservation: "Preserve existing data"
    - user_notification: "Notify user of changes"
    - rollback_option: "Provide rollback option"
```

### 3.3 Template Validation Contract

#### Template Validation Rules
```yaml
TemplateValidation:
  syntax_validation:
    - jinja2_syntax: "Valid Jinja2 syntax"
    - yaml_frontmatter: "Valid YAML front matter"
    - encoding_check: "UTF-8 encoding"
    - line_ending_check: "LF line endings"
  
  structure_validation:
    - required_sections: "All required sections present"
    - section_order: "Sections in correct order"
    - block_structure: "Valid block structure"
    - include_structure: "Valid include structure"
  
  content_validation:
    - variable_usage: "All variables properly used"
    - filter_usage: "All filters properly used"
    - macro_usage: "All macros properly used"
    - content_length: "Content within size limits"
  
  security_validation:
    - dangerous_constructs: "No dangerous constructs"
    - file_access: "No file system access"
    - network_access: "No network access"
    - system_commands: "No system command execution"
```

#### Validation Error Contract
```yaml
ValidationError:
  error_types:
    - syntax_error: "Jinja2 syntax errors"
    - structure_error: "Template structure errors"
    - content_error: "Content validation errors"
    - security_error: "Security validation errors"
    - dependency_error: "Dependency errors"
  
  error_format:
    - type: "Error type"
    - message: "Human-readable error message"
    - line: "Line number (if applicable)"
    - column: "Column number (if applicable)"
    - context: "Error context"
    - suggestion: "Suggested fix"
  
  error_handling:
    - fail_fast: "Stop on first error"
    - collect_all: "Collect all errors"
    - user_friendly: "User-friendly error messages"
    - actionable: "Provide actionable suggestions"
```

## 4. Template Customization Contracts

### 4.1 Custom Template Contract

#### Custom Template Structure
```yaml
CustomTemplate:
  location: "user_templates/ directory"
  inheritance: "Extends base templates"
  override_rules: "Can override any block"
  
  customization_levels:
    - basic: "Override content blocks only"
    - intermediate: "Override structure blocks"
    - advanced: "Override all blocks and add custom"
  
  validation_rules:
    - inherit_required: "Must extend a base template"
    - block_validation: "Override blocks must be valid"
    - variable_consistency: "Variables must be consistent"
    - security_compliance: "Must pass security validation"
```

#### Template Override Contract
```yaml
TemplateOverride:
  override_types:
    - block_override: "Override template blocks"
    - variable_override: "Override default variables"
    - filter_override: "Override default filters"
    - style_override: "Override default styles"
  
  override_rules:
    - inheritance_required: "Must extend base template"
    - block_signature: "Override blocks must match signature"
    - variable_type: "Override variables must match type"
    - filter_signature: "Override filters must match signature"
  
  override_validation:
    - syntax_check: "Override syntax must be valid"
    - type_check: "Override types must match"
    - dependency_check: "Override dependencies must be met"
    - security_check: "Override must pass security validation"
```

### 4.2 Template Configuration Contract

#### Template Configuration Structure
```yaml
TemplateConfiguration:
  config_file: "template_config.yaml"
  location: "project root or user config"
  
  configuration_sections:
    - default_templates: "Default template mappings"
    - custom_templates: "Custom template definitions"
    - template_variables: "Default variable values"
    - template_filters: "Custom filter definitions"
    - output_settings: "Output format settings"
  
  configuration_validation:
    - yaml_syntax: "Valid YAML syntax"
    - template_references: "All template references valid"
    - variable_definitions: "All variables properly defined"
    - filter_definitions: "All filters properly defined"
```

#### Template Variable Configuration
```yaml
TemplateVariableConfiguration:
  variable_sources:
    - project_data: "Project-specific variables"
    - user_preferences: "User preference variables"
    - system_variables: "System-generated variables"
    - custom_variables: "User-defined variables"
  
  variable_priority:
    1. custom_variables: "Highest priority"
    2. project_data: "High priority"
    3. user_preferences: "Medium priority"
    4. system_variables: "Lowest priority"
  
  variable_validation:
    - type_check: "Variables must match expected types"
    - required_check: "Required variables must be present"
    - format_check: "Variables must match expected formats"
    - dependency_check: "Variable dependencies must be met"
```

## 5. Template Performance Contracts

### 5.1 Rendering Performance Contract

#### Performance Requirements
```yaml
RenderingPerformance:
  response_time_limits:
    - simple_template: "< 1 second"
    - complex_template: "< 3 seconds"
    - large_template: "< 5 seconds"
    - template_with_includes: "< 10 seconds"
  
  resource_limits:
    - memory_usage: "< 128 MB"
    - cpu_usage: "< 50% for 5 seconds"
    - disk_io: "< 10 MB read/write"
    - network_io: "0 MB (no network access)"
  
  scalability_requirements:
    - concurrent_renders: "Support 5 concurrent renders"
    - template_cache: "Cache compiled templates"
    - variable_cache: "Cache processed variables"
    - output_cache: "Cache rendered output when possible"
```

#### Performance Monitoring
```yaml
PerformanceMonitoring:
  metrics_collection:
    - render_time: "Time to render template"
    - memory_usage: "Memory used during render"
    - cpu_usage: "CPU used during render"
    - template_size: "Size of template file"
    - output_size: "Size of rendered output"
  
  performance_alerts:
    - slow_renders: "Alert on renders > 5 seconds"
    - high_memory: "Alert on memory > 128 MB"
    - high_cpu: "Alert on CPU > 50%"
    - large_output: "Alert on output > 10 MB"
  
  performance_optimization:
    - template_compilation: "Compile templates once"
    - variable_preprocessing: "Preprocess variables"
    - output_streaming: "Stream large outputs"
    - cache_management: "Manage template cache"
```

### 5.2 Template Optimization Contract

#### Optimization Strategies
```yaml
TemplateOptimization:
  compilation_optimization:
    - precompile_templates: "Compile templates at startup"
    - cache_compiled: "Cache compiled templates"
    - optimize_bytecode: "Optimize Jinja2 bytecode"
    - lazy_loading: "Load templates on demand"
  
  rendering_optimization:
    - variable_caching: "Cache processed variables"
    - filter_optimization: "Optimize filter execution"
    - block_optimization: "Optimize block rendering"
    - include_optimization: "Optimize include processing"
  
  memory_optimization:
    - template_pooling: "Reuse template instances"
    - variable_pooling: "Reuse variable objects"
    - output_streaming: "Stream large outputs"
    - garbage_collection: "Explicit garbage collection"
```

## 6. Template Testing Contracts

### 6.1 Template Test Contract

#### Test Structure
```yaml
TemplateTest:
  test_file: "test_{template_name}.py"
  location: "tests/templates/ directory"
  
  test_types:
    - syntax_test: "Test template syntax"
    - rendering_test: "Test template rendering"
    - variable_test: "Test variable handling"
    - output_test: "Test output format"
    - performance_test: "Test rendering performance"
  
  test_data:
    - sample_data: "Sample project data"
    - edge_cases: "Edge case data"
    - error_cases: "Error condition data"
    - performance_data: "Large dataset for performance"
  
  test_validation:
    - output_validation: "Validate rendered output"
    - format_validation: "Validate output format"
    - content_validation: "Validate output content"
    - performance_validation: "Validate performance metrics"
```

#### Test Execution Contract
```yaml
TestExecution:
  test_environment:
    - isolated: "Each test runs in isolation"
    - deterministic: "Tests produce consistent results"
    - fast: "Tests complete quickly"
    - reliable: "Tests don't have flaky behavior"
  
  test_coverage:
    - template_coverage: "All templates tested"
    - variable_coverage: "All variables tested"
    - filter_coverage: "All filters tested"
    - error_coverage: "All error cases tested"
  
  test_reporting:
    - detailed_results: "Detailed test results"
    - performance_metrics: "Performance test results"
    - coverage_report: "Test coverage report"
    - failure_analysis: "Analysis of test failures"
```

---

**Template Contract Compliance**: All template operations in the DocGen CLI must adhere to these contracts. Template validation must be performed before rendering, and template performance must be monitored and optimized. Contract violations must be logged and addressed to ensure reliable document generation.
