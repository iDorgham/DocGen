---
description: File organization and project structure rules for clean root directories
alwaysApply: true
---

# FILE ORGANIZATION & PROJECT STRUCTURE RULES

## ROOT DIRECTORY CLEANLINESS RULES

### MANDATORY ROOT DIRECTORY STRUCTURE

#### ALLOWED ROOT FILES (Maximum 8 files)
1. **README.md** - Project overview and setup instructions
2. **package.json** - Node.js dependencies and scripts
3. **.gitignore** - Git ignore patterns
4. **.env.example** - Environment variables template
5. **docker-compose.yml** - Container orchestration (if applicable)
6. **Dockerfile** - Container definition (if applicable)
7. **LICENSE** - Project license
8. **CHANGELOG.md** - Version history and changes

#### FORBIDDEN ROOT FILES
- Configuration files (move to config/ directory)
- Documentation files (move to docs/ directory)
- Script files (move to scripts/ directory)
- Test files (move to tests/ or __tests__/ directory)
- Source code files (move to src/ or appropriate directories)
- Build artifacts (exclude via .gitignore)
- Temporary files (exclude via .gitignore)
- IDE-specific files (exclude via .gitignore)

#### REQUIRED ROOT DIRECTORIES
```
project-root/
├── src/                    # Source code
├── docs/                   # Documentation
├── scripts/                # Build and utility scripts
├── tests/                  # Test files
├── config/                 # Configuration files
├── public/                 # Static assets (web projects)
├── .github/                # GitHub workflows and templates
└── .cursor/                # Cursor IDE configuration
```

## FILE ORGANIZATION RULES

### 1. SOURCE CODE ORGANIZATION

#### Frontend Projects (React/Vue/Angular)
```
src/
├── components/             # Reusable UI components
│   ├── common/            # Shared components
│   ├── forms/             # Form components
│   └── layout/            # Layout components
├── pages/                 # Page components
├── hooks/                 # Custom hooks (React)
├── services/              # API services
├── utils/                 # Utility functions
├── types/                 # TypeScript type definitions
├── styles/                # Global styles
├── assets/                # Images, icons, fonts
└── constants/             # Application constants
```

#### Backend Projects (Node.js/Python/Go)
```
src/
├── controllers/           # Request handlers
├── models/                # Data models
├── services/              # Business logic
├── middleware/            # Express middleware
├── routes/                # API routes
├── utils/                 # Utility functions
├── config/                # Configuration modules
├── types/                 # Type definitions
└── tests/                 # Unit tests
```

#### Full-Stack Projects
```
├── frontend/              # Frontend application
│   └── src/              # Frontend source code
├── backend/               # Backend application
│   └── src/              # Backend source code
├── shared/                # Shared code between frontend/backend
│   ├── types/            # Shared TypeScript types
│   ├── utils/            # Shared utility functions
│   └── constants/        # Shared constants
└── docs/                  # Project documentation
```

### 2. DOCUMENTATION ORGANIZATION
```
docs/
├── README.md              # Main documentation index
├── setup/                 # Setup and installation guides
│   ├── development.md     # Development environment setup
│   ├── production.md      # Production deployment
│   └── troubleshooting.md # Common issues and solutions
├── api/                   # API documentation
│   ├── endpoints.md       # API endpoint reference
│   ├── authentication.md  # Auth documentation
│   └── examples.md        # API usage examples
├── architecture/          # System architecture
│   ├── overview.md        # High-level architecture
│   ├── database.md        # Database design
│   └── security.md        # Security considerations
├── development/           # Development guidelines
│   ├── coding-standards.md # Code style and standards
│   ├── git-workflow.md    # Git workflow and branching
│   └── testing.md         # Testing guidelines
└── deployment/            # Deployment documentation
    ├── staging.md         # Staging environment
    ├── production.md      # Production deployment
    └── monitoring.md      # Monitoring and logging
```

### 3. CONFIGURATION ORGANIZATION
```
config/
├── development.json       # Development environment config
├── staging.json           # Staging environment config
├── production.json        # Production environment config
├── database.json          # Database configuration
├── redis.json             # Redis configuration
├── email.json             # Email service configuration
└── logging.json           # Logging configuration
```

### 4. SCRIPT ORGANIZATION
```
scripts/
├── build/                 # Build scripts
│   ├── build.sh          # Main build script
│   ├── build-frontend.sh # Frontend build
│   └── build-backend.sh  # Backend build
├── deploy/                # Deployment scripts
│   ├── deploy.sh         # Main deployment script
│   ├── deploy-staging.sh # Staging deployment
│   └── deploy-prod.sh    # Production deployment
├── dev/                   # Development scripts
│   ├── setup.sh          # Development setup
│   ├── start.sh          # Start development servers
│   └── test.sh           # Run tests
└── utils/                 # Utility scripts
    ├── clean.sh          # Clean build artifacts
    ├── lint.sh           # Code linting
    └── format.sh         # Code formatting
```

## FILE NAMING CONVENTIONS

### GENERAL NAMING RULES
- Use kebab-case for directories: `user-management/`
- Use PascalCase for React components: `UserProfile.tsx`
- Use camelCase for JavaScript/TypeScript files: `userService.js`
- Use UPPERCASE for constants: `API_ENDPOINTS.js`
- Use lowercase for configuration files: `database.json`

### SPECIFIC FILE NAMING

#### Component Files
- React Components: `ComponentName.tsx`
- Vue Components: `ComponentName.vue`
- Angular Components: `component-name.component.ts`

#### Service Files
- API Services: `apiService.ts`
- Business Logic: `userService.ts`
- Utility Services: `dateUtils.ts`

#### Test Files
- Unit Tests: `componentName.test.ts`
- Integration Tests: `componentName.integration.test.ts`
- E2E Tests: `featureName.e2e.test.ts`

#### Configuration Files
- Environment: `.env.development`, `.env.production`
- Package Managers: `package.json`, `yarn.lock`, `pnpm-lock.yaml`
- Build Tools: `webpack.config.js`, `vite.config.ts`
- Linting: `.eslintrc.js`, `.prettierrc`

## AUTOMATED FILE ORGANIZATION

### GITIGNORE RULES
```gitignore
# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# Build outputs
dist/
build/
out/
.next/
.nuxt/
.vuepress/dist/

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE files
.vscode/
.idea/
*.swp
*.swo
*~

# OS files
.DS_Store
Thumbs.db

# Logs
logs/
*.log

# Runtime data
pids/
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/
*.lcov

# Temporary folders
tmp/
temp/
```

### AUTOMATED ORGANIZATION SCRIPTS
```bash
#!/bin/bash
# scripts/organize-project.sh

echo "Organizing project structure..."

# Move configuration files to config/
find . -maxdepth 1 -name "*.json" -not -name "package.json" -exec mv {} config/ \;

# Move documentation to docs/
find . -maxdepth 1 -name "*.md" -not -name "README.md" -exec mv {} docs/ \;

# Move scripts to scripts/
find . -maxdepth 1 -name "*.sh" -exec mv {} scripts/ \;

# Create required directories
mkdir -p src/{components,pages,services,utils,types,styles,assets,constants}
mkdir -p tests/{unit,integration,e2e}
mkdir -p docs/{setup,api,architecture,development,deployment}
mkdir -p config
mkdir -p scripts/{build,deploy,dev,utils}

echo "Project structure organized successfully!"
```

## ENFORCEMENT RULES

### PRECOMMIT HOOKS
- Check for files in root directory (except allowed files)
- Validate file naming conventions
- Ensure proper directory structure
- Run linting and formatting
- Verify no build artifacts in repository

### CI/CD VALIDATION
1. Check root directory cleanliness
2. Validate file naming conventions
3. Ensure proper directory structure
4. Verify documentation completeness
5. Check configuration file organization

## MIGRATION STRATEGY

### EXISTING PROJECT CLEANUP
1. Audit current file structure
2. Identify misplaced files
3. Create proper directory structure
4. Move files to appropriate locations
5. Update import paths and references
6. Update documentation
7. Commit changes with clear messages

### TEAM ADOPTION
1. Share organization rules with team
2. Provide migration scripts
3. Set up pre-commit hooks
4. Conduct code reviews for compliance
5. Document exceptions and special cases
6. Regular cleanup sessions

## EXCEPTIONS AND SPECIAL CASES

### ALLOWED EXCEPTIONS
- Framework-specific files (e.g., `next.config.js` for Next.js)
- Tool-specific files (e.g., `tailwind.config.js`)
- Platform-specific files (e.g., `vercel.json`, `netlify.toml`)

### SPECIAL PROJECT TYPES
- Monorepos: Use workspace-specific organization
- Microservices: Each service follows standard structure
- Libraries: Focus on source organization and documentation
- CLI tools: Emphasize script and configuration organization

## MAINTENANCE RULES

### REGULAR AUDITS
- Weekly file structure review
- Monthly documentation updates
- Quarterly organization rule updates
- Annual cleanup and optimization

### AUTOMATION
- Automated file organization scripts
- Pre-commit hooks for validation
- CI/CD pipeline checks
- Regular cleanup automation

---

*These file organization rules ensure clean, maintainable, and scalable project structures while maintaining flexibility for different project types and requirements.*
