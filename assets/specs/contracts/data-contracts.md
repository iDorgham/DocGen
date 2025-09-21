# DocGen CLI Data Contracts

## Overview
This document defines the data contracts for the DocGen CLI tool, specifying the data structures, validation rules, and data flow contracts that ensure data integrity and consistency across the system.

## 1. Core Data Models

### 1.1 Project Data Contract

#### Project Structure
```yaml
ProjectData:
  id: string
    format: UUID v4
    required: true
    example: "550e8400-e29b-41d4-a716-446655440000"
  
  name: string
    min_length: 1
    max_length: 100
    pattern: "^[a-zA-Z0-9][a-zA-Z0-9\\s\\-_]*[a-zA-Z0-9]$"
    required: true
    example: "My Awesome Project"
  
  description: string
    max_length: 500
    required: false
    example: "A comprehensive project management tool"
  
  created_at: datetime
    format: ISO 8601
    required: true
    example: "2025-01-19T14:30:00Z"
  
  updated_at: datetime
    format: ISO 8601
    required: true
    example: "2025-01-19T14:30:00Z"
  
  status: enum
    values: ["active", "archived", "deleted"]
    default: "active"
    required: true
  
  features: array
    type: FeatureData
    required: false
    max_items: 50
  
  phases: array
    type: PhaseData
    required: false
    max_items: 20
  
  metadata: object
    type: ProjectMetadata
    required: false
  
  tags: array
    type: string
    required: false
    max_items: 10
    unique: true
```

#### Feature Data Structure
```yaml
FeatureData:
  id: string
    format: UUID v4
    required: true
  
  name: string
    min_length: 1
    max_length: 100
    required: true
  
  description: string
    max_length: 1000
    required: false
  
  priority: enum
    values: ["low", "medium", "high", "critical"]
    default: "medium"
    required: true
  
  status: enum
    values: ["planned", "in_progress", "completed", "cancelled"]
    default: "planned"
    required: true
  
  estimated_effort: number
    type: integer
    min: 1
    max: 1000
    unit: "hours"
    required: false
  
  dependencies: array
    type: string (feature IDs)
    required: false
    max_items: 10
```

#### Phase Data Structure
```yaml
PhaseData:
  id: string
    format: UUID v4
    required: true
  
  name: string
    min_length: 1
    max_length: 100
    required: true
  
  description: string
    max_length: 1000
    required: false
  
  start_date: date
    format: ISO 8601 date
    required: false
  
  end_date: date
    format: ISO 8601 date
    required: false
  
  status: enum
    values: ["not_started", "in_progress", "completed", "on_hold"]
    default: "not_started"
    required: true
  
  deliverables: array
    type: DeliverableData
    required: false
    max_items: 20
  
  team_members: array
    type: TeamMemberData
    required: false
    max_items: 50
```

### 1.2 Document Data Contract

#### Document Structure
```yaml
DocumentData:
  id: string
    format: UUID v4
    required: true
  
  project_id: string
    format: UUID v4
    required: true
    foreign_key: ProjectData.id
  
  type: enum
    values: ["spec", "plan", "marketing"]
    required: true
  
  format: enum
    values: ["markdown", "html", "pdf"]
    required: true
  
  content: string
    min_length: 1
    max_length: 10485760  # 10MB
    required: true
  
  generated_at: datetime
    format: ISO 8601
    required: true
  
  template_used: string
    max_length: 500
    required: false
  
  custom_variables: object
    type: DocumentVariables
    required: false
  
  file_size: number
    type: integer
    min: 1
    max: 10485760  # 10MB
    unit: "bytes"
    required: false
  
  generation_time: number
    type: float
    min: 0
    max: 30
    unit: "seconds"
    required: false
  
  checksum: string
    format: SHA-256 hash
    required: false
    purpose: "integrity verification"
```

#### Document Variables Structure
```yaml
DocumentVariables:
  project_name: string
    required: false
  
  project_description: string
    required: false
  
  author: string
    required: false
  
  version: string
    format: semantic version
    required: false
  
  custom_fields: object
    type: key-value pairs
    required: false
    max_keys: 50
```

### 1.3 Template Data Contract

#### Template Structure
```yaml
TemplateData:
  name: string
    min_length: 1
    max_length: 100
    pattern: "^[a-zA-Z0-9][a-zA-Z0-9\\-_]*[a-zA-Z0-9]$"
    required: true
    unique: true
  
  type: enum
    values: ["spec", "plan", "marketing"]
    required: true
  
  content: string
    min_length: 1
    max_length: 1048576  # 1MB
    required: true
    validation: "valid Jinja2 syntax"
  
  version: string
    format: semantic version
    required: true
    example: "1.0.0"
  
  created_at: datetime
    format: ISO 8601
    required: true
  
  updated_at: datetime
    format: ISO 8601
    required: true
  
  description: string
    max_length: 500
    required: false
  
  author: string
    max_length: 100
    required: false
  
  custom_filters: array
    type: FilterDefinition
    required: false
    max_items: 20
  
  required_variables: array
    type: string
    required: false
    max_items: 100
  
  default_variables: object
    type: key-value pairs
    required: false
    max_keys: 50
  
  dependencies: array
    type: string (template names)
    required: false
    max_items: 10
```

#### Filter Definition Structure
```yaml
FilterDefinition:
  name: string
    min_length: 1
    max_length: 50
    pattern: "^[a-zA-Z_][a-zA-Z0-9_]*$"
    required: true
  
  description: string
    max_length: 200
    required: false
  
  parameters: array
    type: FilterParameter
    required: false
    max_items: 10
  
  return_type: string
    values: ["string", "number", "boolean", "array", "object"]
    required: true
```

### 1.4 Configuration Data Contract

#### Configuration Structure
```yaml
ConfigurationData:
  version: string
    format: semantic version
    required: true
    example: "1.0.0"
  
  user_preferences: object
    type: UserPreferences
    required: true
  
  project_settings: object
    type: ProjectSettings
    required: true
  
  template_settings: object
    type: TemplateSettings
    required: true
  
  output_settings: object
    type: OutputSettings
    required: true
  
  created_at: datetime
    format: ISO 8601
    required: true
  
  updated_at: datetime
    format: ISO 8601
    required: true
```

#### User Preferences Structure
```yaml
UserPreferences:
  default_output_format: enum
    values: ["markdown", "html", "pdf"]
    default: "markdown"
    required: true
  
  default_output_directory: string
    max_length: 500
    required: false
  
  auto_save: boolean
    default: true
    required: true
  
  theme: enum
    values: ["light", "dark", "auto"]
    default: "auto"
    required: true
  
  language: string
    format: ISO 639-1
    default: "en"
    required: true
  
  notifications: object
    type: NotificationSettings
    required: true
```

## 2. Data Validation Contracts

### 2.1 Input Validation Rules

#### Project Name Validation
```yaml
ProjectNameValidation:
  rules:
    - required: true
    - min_length: 1
    - max_length: 100
    - pattern: "^[a-zA-Z0-9][a-zA-Z0-9\\s\\-_]*[a-zA-Z0-9]$"
    - unique: true (within user scope)
    - no_reserved_words: ["admin", "system", "root", "config"]
  
  error_messages:
    required: "Project name is required"
    min_length: "Project name must be at least 1 character"
    max_length: "Project name must not exceed 100 characters"
    pattern: "Project name must start and end with alphanumeric characters"
    unique: "Project name already exists"
    reserved: "Project name contains reserved words"
```

#### Email Validation
```yaml
EmailValidation:
  rules:
    - required: false
    - format: RFC 5322 compliant
    - max_length: 254
    - unique: true (within project scope)
  
  error_messages:
    format: "Invalid email format"
    max_length: "Email must not exceed 254 characters"
    unique: "Email already exists in project"
```

#### Date Validation
```yaml
DateValidation:
  rules:
    - format: ISO 8601
    - not_future: true (for creation dates)
    - not_past: true (for future dates, when specified)
    - logical_order: true (start_date <= end_date)
  
  error_messages:
    format: "Date must be in ISO 8601 format"
    future: "Date cannot be in the future"
    past: "Date cannot be in the past"
    order: "Start date must be before end date"
```

### 2.2 Data Integrity Rules

#### Referential Integrity
```yaml
ReferentialIntegrity:
  project_documents:
    - document.project_id must exist in projects table
    - cascade_delete: true (delete documents when project deleted)
  
  project_phases:
    - phase.project_id must exist in projects table
    - cascade_delete: true (delete phases when project deleted)
  
  phase_deliverables:
    - deliverable.phase_id must exist in phases table
    - cascade_delete: true (delete deliverables when phase deleted)
  
  template_dependencies:
    - dependency must exist in templates table
    - circular_dependency: false (prevent circular references)
```

#### Data Consistency Rules
```yaml
DataConsistency:
  project_timestamps:
    - updated_at >= created_at
    - updated_at changes when any related data changes
  
  document_metadata:
    - file_size matches actual content length
    - checksum matches content hash
    - generation_time is reasonable (< 30 seconds)
  
  template_syntax:
    - content must be valid Jinja2 syntax
    - required_variables must be used in template
    - custom_filters must be properly defined
```

## 3. Data Flow Contracts

### 3.1 Project Creation Flow
```yaml
ProjectCreationFlow:
  steps:
    1. validate_input:
       - project_name: ProjectNameValidation
       - description: StringValidation (optional)
       - features: ArrayValidation (optional)
    
    2. check_constraints:
       - name_uniqueness: true
       - user_permissions: true
       - system_limits: true
    
    3. create_project:
       - generate_id: UUID v4
       - set_timestamps: current_time
       - set_status: "active"
       - create_directory: true
    
    4. save_data:
       - write_project_file: YAML format
       - update_index: true
       - log_operation: true
    
    5. return_result:
       - project_id: string
       - project_path: string
       - status: "created"
```

### 3.2 Document Generation Flow
```yaml
DocumentGenerationFlow:
  steps:
    1. validate_request:
       - project_exists: true
       - document_type: valid enum
       - output_format: valid enum
       - permissions: true
    
    2. load_data:
       - project_data: ProjectData
       - template_data: TemplateData
       - custom_variables: DocumentVariables
    
    3. prepare_context:
       - merge_data: project + custom
       - validate_required_variables: true
       - apply_defaults: true
    
    4. render_template:
       - load_template: Jinja2
       - apply_filters: custom filters
       - render_content: string
       - validate_output: true
    
    5. format_output:
       - markdown: direct output
       - html: convert + style
       - pdf: convert via WeasyPrint
    
    6. save_document:
       - write_file: specified format
       - update_metadata: DocumentData
       - log_generation: true
    
    7. return_result:
       - file_path: string
       - file_size: number
       - generation_time: number
```

### 3.3 Data Migration Flow
```yaml
DataMigrationFlow:
  steps:
    1. backup_current:
       - create_backup: timestamped
       - verify_backup: checksum
       - store_backup: safe location
    
    2. validate_migration:
       - check_version: current vs target
       - identify_changes: schema differences
       - estimate_impact: data affected
    
    3. perform_migration:
       - transform_data: apply schema changes
       - validate_transformed: integrity check
       - update_metadata: version info
    
    4. verify_migration:
       - data_integrity: checksum comparison
       - functionality_test: basic operations
       - rollback_plan: if issues found
    
    5. complete_migration:
       - update_version: target version
       - cleanup_backup: after verification
       - log_migration: success/failure
```

## 4. Data Storage Contracts

### 4.1 File System Storage
```yaml
FileSystemStorage:
  project_structure:
    ~/.docgen/
      projects/
        {project_id}/
          project.yaml
          documents/
            {document_id}.{format}
          templates/
            custom/
          backups/
            {timestamp}/
  
  file_permissions:
    - projects/: 755 (owner: rwx, group: rx, other: rx)
    - project.yaml: 644 (owner: rw, group: r, other: r)
    - documents/: 755
    - backups/: 700 (owner only)
  
  file_formats:
    - project_data: YAML
    - documents: Markdown/HTML/PDF
    - templates: Jinja2
    - configuration: YAML
    - logs: JSON
```

### 4.2 Data Serialization
```yaml
DataSerialization:
  yaml_files:
    - encoding: UTF-8
    - line_ending: LF
    - indentation: 2 spaces
    - max_line_length: 120
    - sort_keys: true
  
  json_files:
    - encoding: UTF-8
    - pretty_print: true
    - sort_keys: true
    - ensure_ascii: false
  
  binary_files:
    - pdf_documents: PDF/A format
    - images: PNG/JPEG format
    - archives: ZIP format
```

## 5. Data Security Contracts

### 5.1 Data Encryption
```yaml
DataEncryption:
  at_rest:
    - sensitive_data: AES-256 encryption
    - key_management: OS keyring
    - key_rotation: every 90 days
  
  in_transit:
    - network_communication: TLS 1.3
    - file_transfer: encrypted protocols
    - api_communication: HTTPS only
  
  key_management:
    - key_generation: cryptographically secure
    - key_storage: OS keyring/secure storage
    - key_backup: encrypted backup
    - key_recovery: secure process
```

### 5.2 Data Privacy
```yaml
DataPrivacy:
  personal_data:
    - collection: minimal necessary
    - processing: purpose limitation
    - storage: time limitation
    - deletion: right to be forgotten
  
  sensitive_data:
    - identification: automatic detection
    - protection: encryption at rest
    - access: role-based permissions
    - audit: access logging
  
  data_anonymization:
    - user_data: remove identifiers
    - project_data: sanitize sensitive info
    - logs: remove personal information
    - exports: anonymize by default
```

## 6. Data Backup and Recovery Contracts

### 6.1 Backup Strategy
```yaml
BackupStrategy:
  frequency:
    - project_data: on every change
    - configuration: daily
    - templates: weekly
    - logs: monthly
  
  retention:
    - project_backups: 30 days
    - configuration_backups: 90 days
    - template_backups: 1 year
    - log_backups: 6 months
  
  verification:
    - backup_integrity: checksum validation
    - restore_testing: monthly
    - backup_monitoring: automated alerts
    - recovery_documentation: up to date
```

### 6.2 Recovery Procedures
```yaml
RecoveryProcedures:
  data_corruption:
    - detection: automated monitoring
    - isolation: prevent further damage
    - restoration: from latest backup
    - verification: data integrity check
  
  accidental_deletion:
    - detection: user report
    - recovery: from backup
    - verification: user confirmation
    - prevention: improved safeguards
  
  system_failure:
    - assessment: impact analysis
    - recovery: full system restore
    - validation: functionality testing
    - documentation: incident report
```

## 7. Data Quality Contracts

### 7.1 Data Quality Metrics
```yaml
DataQualityMetrics:
  completeness:
    - required_fields: 100% populated
    - optional_fields: > 80% populated
    - relationships: all foreign keys valid
  
  accuracy:
    - data_validation: all rules passed
    - format_compliance: 100% compliant
    - business_rules: all constraints met
  
  consistency:
    - cross_references: all valid
    - timestamps: logical ordering
    - status_transitions: valid sequences
  
  timeliness:
    - data_freshness: < 24 hours old
    - update_frequency: as needed
    - processing_time: < 5 seconds
```

### 7.2 Data Quality Monitoring
```yaml
DataQualityMonitoring:
  automated_checks:
    - validation_rules: continuous
    - integrity_constraints: on change
    - format_compliance: on save
    - relationship_validity: on update
  
  quality_reports:
    - daily_summary: quality metrics
    - weekly_trends: quality changes
    - monthly_analysis: quality patterns
    - quarterly_review: quality strategy
  
  quality_improvement:
    - issue_tracking: quality problems
    - root_cause_analysis: problem sources
    - process_improvement: quality processes
    - training: quality awareness
```

---

**Data Contract Compliance**: All data operations in the DocGen CLI must adhere to these contracts. Data validation must be performed at all entry points, and data integrity must be maintained throughout the system lifecycle. Contract violations must be logged and addressed immediately.
