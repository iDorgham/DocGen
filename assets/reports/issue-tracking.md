# DocGen CLI Issue Tracking

## Issue Summary

- **Total Issues**: 4
- **Critical Issues**: 2
- **Medium Priority Issues**: 2
- **Low Priority Issues**: 0
- **Resolved Issues**: 0

## Critical Issues (Priority: High)

### Issue #1: Template Location Inconsistency
- **ID**: TEMPLATE-001
- **Priority**: Critical
- **Status**: Open
- **Assigned**: Unassigned
- **Created**: [Current Date]
- **Updated**: [Current Date]

#### Description
Templates exist in both `src/templates/` and `assets/templates/` directories, causing confusion about which location is the active template directory.

#### Impact
- Confusion about active template location
- Potential template loading failures
- Maintenance overhead
- Developer confusion

#### Root Cause
Project reorganization moved templates to `assets/templates/` but some templates remain in `src/templates/`. The `generate_docs.py` script uses `FileSystemLoader('src/templates')`, suggesting `src/templates/` is the active location.

#### Evidence
- `src/templates/` contains: `marketing.j2`, `plan.j2`, `spec.j2`
- `assets/templates/` contains: `tasks-template.md`, `plan-template.md`, `spec-template.md`, `agent-file-template.md`
- `assets/scripts/generate_docs.py` uses `FileSystemLoader('src/templates')`

#### Proposed Solution for Template Location

1. **Decision**: Choose `src/templates/` as the active template directory
2. **Action**: Move all templates from `assets/templates/` to `src/templates/`
3. **Action**: Update all references to use `src/templates/`
4. **Action**: Update documentation to reflect template location
5. **Action**: Remove `assets/templates/` directory

#### Acceptance Criteria for Template Location

- [ ] All templates are in `src/templates/` directory
- [ ] All references point to `src/templates/`
- [ ] Documentation reflects correct template location
- [ ] Template loading works correctly
- [ ] No duplicate template directories

#### Estimated Effort for Template Location

- **Time**: 4 hours
- **Complexity**: Low
- **Risk**: Low

#### Dependencies for Template Location

- None

#### Related Issues for Template Location

- Issue #2: Missing Template File

---

### Issue #2: Missing Template File
- **ID**: TEMPLATE-002
- **Priority**: Critical
- **Status**: Open
- **Assigned**: Unassigned
- **Created**: [Current Date]
- **Updated**: [Current Date]

#### Description
The file `src/templates/tasks-template.md` is referenced but not found in the expected location.

#### Impact
- Template generation may fail
- Missing functionality for task template generation
- Incomplete template system

#### Root Cause
Template file was not created or was moved during project reorganization.

#### Evidence
- File `src/templates/tasks-template.md` not found
- Template is referenced in documentation
- Template is expected by the system

#### Proposed Solution for Missing Template

1. **Action**: Create `src/templates/tasks-template.md` file
2. **Action**: Implement task template content
3. **Action**: Test template loading and generation
4. **Action**: Update documentation if needed

#### Acceptance Criteria for Missing Template

- [ ] `src/templates/tasks-template.md` file exists
- [ ] Template content is complete and functional
- [ ] Template loads correctly
- [ ] Template generates valid output
- [ ] Documentation is updated

#### Estimated Effort for Missing Template

- **Time**: 2 hours
- **Complexity**: Low
- **Risk**: Low

#### Dependencies for Missing Template

- Issue #1: Template Location Inconsistency (should be resolved first)

#### Related Issues for Missing Template

- Issue #1: Template Location Inconsistency

---

## Medium Priority Issues

### Issue #3: Documentation Redundancy
- **ID**: DOCS-001
- **Priority**: Medium
- **Status**: Open
- **Assigned**: Unassigned
- **Created**: [Current Date]
- **Updated**: [Current Date]

#### Description
The `docs/generated_docs/` and `docs/generated/` folders contain identical content, creating redundancy and maintenance overhead.

#### Impact
- Maintenance overhead
- Developer confusion
- Potential inconsistency
- Wasted storage space

#### Root Cause
Project reorganization created duplicate directories with identical content.

#### Evidence
- `docs/generated_docs/` and `docs/generated/` exist
- Both contain identical content
- Both are referenced in documentation

#### Proposed Solution for Documentation Redundancy

1. **Action**: Choose one directory as the primary location
2. **Action**: Move all content to primary directory
3. **Action**: Update all references to use primary directory
4. **Action**: Remove duplicate directory
5. **Action**: Update documentation

#### Acceptance Criteria for Documentation Redundancy

- [ ] Only one generated docs directory exists
- [ ] All references point to correct directory
- [ ] No duplicate content
- [ ] Documentation is updated
- [ ] No broken references

#### Estimated Effort for Documentation Redundancy

- **Time**: 2 hours
- **Complexity**: Low
- **Risk**: Low

#### Dependencies for Documentation Redundancy

- None

#### Related Issues for Documentation Redundancy

- None

---

### Issue #4: Test Import Path Issues
- **ID**: TEST-001
- **Priority**: Medium
- **Status**: Partially Resolved
- **Assigned**: Unassigned
- **Created**: [Current Date]
- **Updated**: [Current Date]

#### Description
Some test files have incorrect import paths that may prevent tests from running properly.

#### Impact
- Tests may not run properly
- Test coverage may be incomplete
- Quality assurance may be compromised

#### Root Cause
Test files were created before the modular refactoring and have outdated import paths.

#### Evidence
- Test files in `assets/scripts/tests/` have incorrect imports
- Some imports reference non-existent modules
- Test structure doesn't match current code structure

#### Proposed Solution for Test Import Issues

1. **Action**: Review all test files for incorrect imports
2. **Action**: Fix import paths to match current structure
3. **Action**: Ensure all tests can run successfully
4. **Action**: Verify test coverage is accurate
5. **Action**: Update test documentation

#### Acceptance Criteria for Test Import Issues

- [ ] All test files have correct import paths
- [ ] All tests can run successfully
- [ ] Test coverage is accurate
- [ ] No import errors in tests
- [ ] Test documentation is updated

#### Estimated Effort for Test Import Issues

- **Time**: 3 hours
- **Complexity**: Medium
- **Risk**: Medium

#### Dependencies for Test Import Issues

- None

#### Related Issues for Test Import Issues

- None

---

## Issue Resolution Workflow

### Issue Lifecycle
1. **Created**: Issue is identified and documented
2. **Assigned**: Issue is assigned to a developer
3. **In Progress**: Developer is working on the issue
4. **Review**: Issue solution is under review
5. **Resolved**: Issue is resolved and verified
6. **Closed**: Issue is closed and archived

### Issue Resolution Process
1. **Analysis**: Analyze the issue and understand root cause
2. **Planning**: Plan the solution and estimate effort
3. **Implementation**: Implement the solution
4. **Testing**: Test the solution thoroughly
5. **Validation**: Validate that the issue is resolved
6. **Documentation**: Update documentation if needed
7. **Closure**: Close the issue and update status

### Issue Escalation
- **Critical Issues**: Must be resolved within 24 hours
- **High Priority Issues**: Must be resolved within 1 week
- **Medium Priority Issues**: Must be resolved within 2 weeks
- **Low Priority Issues**: Must be resolved within 1 month

## Issue Tracking Tools

### Current Tools
- **Issue Tracking**: This document (manual tracking)
- **Version Control**: Git for code changes
- **Documentation**: Markdown files for documentation

### Recommended Tools
- **Issue Tracking**: GitHub Issues for better tracking
- **Project Management**: GitHub Projects for project management
- **CI/CD**: GitHub Actions for automated testing

## Issue Metrics

### Current Metrics
- **Total Issues**: 4
- **Open Issues**: 4
- **Resolved Issues**: 0
- **Average Resolution Time**: N/A
- **Issue Backlog**: 4

### Target Metrics
- **Issue Resolution Time**: < 1 week for critical issues
- **Issue Backlog**: < 5 open issues
- **Issue Quality**: All issues properly documented
- **Issue Tracking**: 100% of issues tracked

## Issue Prevention

### Prevention Strategies
1. **Code Reviews**: Regular code reviews to catch issues early
2. **Automated Testing**: Comprehensive automated testing
3. **Quality Gates**: Quality gates to prevent issues
4. **Documentation**: Good documentation to prevent confusion
5. **Standards**: Clear coding and development standards

### Prevention Tools
- **Linting**: Automated linting to catch code issues
- **Testing**: Automated testing to catch functional issues
- **Documentation**: Automated documentation validation
- **Standards**: Automated standards enforcement

## Issue Communication

### Communication Channels
- **Issue Updates**: Regular updates on issue status
- **Progress Reports**: Weekly progress reports
- **Escalation**: Immediate escalation for critical issues
- **Resolution**: Notification when issues are resolved

### Communication Standards
- **Update Frequency**: Daily updates for critical issues
- **Update Format**: Clear, concise updates with status
- **Escalation Criteria**: Clear escalation criteria
- **Resolution Notification**: Immediate notification of resolution

---

*This issue tracking document is updated daily and provides a comprehensive view of all project issues, their status, and resolution progress.*
