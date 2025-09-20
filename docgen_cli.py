#!/usr/bin/env python3
"""
DocGen CLI - Production-ready command-line tool for generating project documentation.
Version: 1.0.0
"""

import sys
import os
import argparse
import json
from pathlib import Path
from typing import Dict, Any, Optional

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Global configuration
VERBOSE = False

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="DocGen CLI - Document Generation Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  docgen create my-project                    # Create a new project
  docgen spec --output docs/spec.md          # Generate technical specification
  docgen plan --format html                  # Generate project plan in HTML
  docgen marketing --template custom         # Generate marketing materials
  docgen validate --fix                      # Validate and fix project data
  docgen --version                           # Show version information
        """
    )
    
    parser.add_argument('command', nargs='?', help='Command to execute')
    parser.add_argument('--version', action='version', version='DocGen CLI 1.0.0')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--format', '-f', choices=['markdown', 'html', 'pdf'], 
                       default='markdown', help='Output format')
    parser.add_argument('--template', '-t', help='Template to use')
    parser.add_argument('--fix', action='store_true', help='Fix issues automatically')
    
    # Parse known args to handle subcommands
    args, remaining_args = parser.parse_known_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Set global verbose flag
    global VERBOSE
    VERBOSE = args.verbose
    
    try:
        if args.command == "help":
            show_help()
        elif args.command == "create":
            create_project(args, remaining_args)
        elif args.command == "spec":
            generate_spec(args)
        elif args.command == "plan":
            generate_plan(args)
        elif args.command == "marketing":
            generate_marketing(args)
        elif args.command == "validate":
            validate_project(args)
        else:
            print(f"❌ Unknown command: {args.command}")
            print("Run 'docgen help' for available commands")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        if VERBOSE:
            import traceback
            traceback.print_exc()
        else:
            print(f"❌ Error: {e}")
        sys.exit(1)

def show_help():
    """Show detailed help information."""
    print("DocGen CLI Help")
    print("===============")
    print()
    print("Commands:")
    print("  create <name> [path]     - Create a new project")
    print("  spec [output]            - Generate technical specification")
    print("  plan [output]            - Generate project plan")
    print("  marketing [output]       - Generate marketing materials")
    print("  validate                 - Validate current project")
    print()
    print("Examples:")
    print("  python docgen_cli.py create my-project")
    print("  python docgen_cli.py spec")
    print("  python docgen_cli.py plan output/plan.md")

def create_project(args, remaining_args):
    """Create a new project."""
    if not remaining_args:
        print("❌ Error: Project name required")
        print("Usage: docgen create <project-name> [path]")
        return
    
    project_name = remaining_args[0]
    project_path = remaining_args[1] if len(remaining_args) > 1 else f"./{project_name}"
    
    print(f"Creating project: {project_name}")
    print(f"Path: {project_path}")
    
    # Create project directory
    project_dir = Path(project_path)
    project_dir.mkdir(parents=True, exist_ok=True)
    
    # Create basic structure
    (project_dir / "docs").mkdir(exist_ok=True)
    (project_dir / "data").mkdir(exist_ok=True)
    
    # Create sample project data
    project_data = {
        "project": {
            "name": project_name,
            "description": f"A new project called {project_name}",
            "version": "1.0.0"
        }
    }
    
    import yaml
    with open(project_dir / "project_data.yaml", 'w') as f:
        yaml.dump(project_data, f, default_flow_style=False, indent=2)
    
    print(f"✓ Project '{project_name}' created successfully!")
    print(f"✓ Project data file created: {project_dir / 'project_data.yaml'}")
    print()
    print("Next steps:")
    print("1. Edit project_data.yaml with your project information")
    print("2. Run 'python docgen_cli.py spec' to generate technical specification")
    print("3. Run 'python docgen_cli.py plan' to generate project plan")

def generate_spec(args):
    """Generate technical specification."""
    print("📋 Generating technical specification...")
    
    # Look for project data file
    project_data_file = Path("project_data.yaml")
    if not project_data_file.exists():
        print("❌ Error: project_data.yaml not found")
        print("Make sure you're in a project directory or create a project first")
        return
    
    # Load project data
    import yaml
    with open(project_data_file, 'r') as f:
        project_data = yaml.safe_load(f)
    
    # Generate basic spec
    spec_content = f"""# Technical Specification

## Project Overview

**Project Name:** {project_data.get('project', {}).get('name', 'Unknown')}
**Description:** {project_data.get('project', {}).get('description', 'No description provided')}
**Version:** {project_data.get('project', {}).get('version', '1.0.0')}

## Technical Requirements

### Functional Requirements
- Core functionality implementation
- User interface development
- Data management capabilities

### Non-Functional Requirements
- Performance: Response time < 200ms
- Scalability: Support for 1000+ concurrent users
- Security: Data encryption and secure authentication

## Architecture

### System Architecture
- Frontend: Web-based interface
- Backend: RESTful API services
- Database: Relational database for data persistence

### Technology Stack
- Backend: Python, FastAPI
- Frontend: React, TypeScript
- Database: PostgreSQL
- Deployment: Docker, Kubernetes

## Implementation Plan

### Phase 1: Foundation
- Project setup and configuration
- Basic API structure
- Database schema design

### Phase 2: Core Features
- User authentication
- Core business logic
- API endpoints

### Phase 3: Frontend
- User interface development
- API integration
- Testing and validation

## Testing Strategy

### Unit Testing
- Component-level testing
- API endpoint testing
- Database operation testing

### Integration Testing
- End-to-end workflow testing
- API integration testing
- Performance testing

## Deployment

### Development Environment
- Local development setup
- Docker containerization
- Database setup

### Production Environment
- Cloud deployment
- Load balancing
- Monitoring and logging

## Maintenance

### Code Quality
- Code review process
- Automated testing
- Documentation updates

### Monitoring
- Application performance monitoring
- Error tracking and logging
- User analytics

---
*Generated by DocGen CLI*
"""
    
    # Determine output file
    if args.output:
        output_file = Path(args.output)
    else:
        output_file = Path("docs/technical_spec.md")
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Handle different output formats
    if args.format == 'html':
        # Convert markdown to HTML (basic conversion)
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Technical Specification - {project_data.get('project', {}).get('name', 'Project')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        h1, h2, h3 {{ color: #333; }}
        code {{ background: #f4f4f4; padding: 2px 4px; border-radius: 3px; }}
        pre {{ background: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }}
    </style>
</head>
<body>
{spec_content.replace('#', '<h1>').replace('##', '<h2>').replace('###', '<h3>')}
</body>
</html>"""
        with open(output_file.with_suffix('.html'), 'w') as f:
            f.write(html_content)
        output_file = output_file.with_suffix('.html')
    else:
        with open(output_file, 'w') as f:
            f.write(spec_content)
    
    print(f"✅ Technical specification generated: {output_file}")

def generate_plan(args):
    """Generate project plan."""
    print("📅 Generating project plan...")
    
    # Look for project data file
    project_data_file = Path("project_data.yaml")
    if not project_data_file.exists():
        print("❌ Error: project_data.yaml not found")
        print("Make sure you're in a project directory or create a project first")
        return
    
    # Load project data
    import yaml
    with open(project_data_file, 'r') as f:
        project_data = yaml.safe_load(f)
    
    # Generate basic plan
    plan_content = f"""# Project Plan

## Project Information

**Project Name:** {project_data.get('project', {}).get('name', 'Unknown')}
**Description:** {project_data.get('project', {}).get('description', 'No description provided')}
**Version:** {project_data.get('project', {}).get('version', '1.0.0')}

## Project Timeline

### Phase 1: Planning and Setup (Week 1-2)
- [ ] Project requirements gathering
- [ ] Technical architecture design
- [ ] Development environment setup
- [ ] Team onboarding and training

**Deliverables:**
- Requirements document
- Technical architecture document
- Development environment setup guide

### Phase 2: Core Development (Week 3-8)
- [ ] Backend API development
- [ ] Database design and implementation
- [ ] Core business logic implementation
- [ ] Unit testing implementation

**Deliverables:**
- Backend API
- Database schema
- Unit test suite
- API documentation

### Phase 3: Frontend Development (Week 9-12)
- [ ] User interface design
- [ ] Frontend application development
- [ ] API integration
- [ ] User acceptance testing

**Deliverables:**
- Frontend application
- User interface components
- Integration tests
- User documentation

### Phase 4: Testing and Deployment (Week 13-14)
- [ ] System integration testing
- [ ] Performance testing
- [ ] Security testing
- [ ] Production deployment

**Deliverables:**
- Tested application
- Performance benchmarks
- Security audit report
- Production deployment

## Resource Allocation

### Team Structure
- **Project Manager:** Overall project coordination
- **Backend Developer:** API and database development
- **Frontend Developer:** User interface development
- **QA Engineer:** Testing and quality assurance

### Timeline Summary
- **Total Duration:** 14 weeks
- **Development:** 10 weeks
- **Testing:** 2 weeks
- **Deployment:** 2 weeks

## Risk Management

### Identified Risks
1. **Technical Complexity:** Mitigation through prototyping and early testing
2. **Resource Constraints:** Regular resource monitoring and adjustment
3. **Timeline Delays:** Buffer time allocation and milestone tracking

### Risk Mitigation Strategies
- Regular progress reviews
- Early identification of blockers
- Contingency planning for critical path items

## Success Criteria

### Functional Requirements
- All core features implemented and tested
- User acceptance testing passed
- Performance benchmarks met

### Quality Requirements
- Code coverage > 80%
- Zero critical security vulnerabilities
- User satisfaction score > 4.0/5.0

## Communication Plan

### Regular Meetings
- **Daily Standups:** Progress updates and blocker identification
- **Weekly Reviews:** Milestone progress and risk assessment
- **Monthly Reports:** Stakeholder updates and project status

### Documentation
- Technical documentation maintained throughout development
- User documentation created during development
- Project documentation updated regularly

---
*Generated by DocGen CLI*
"""
    
    # Save plan
    output_file = Path("docs/project_plan.md")
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write(plan_content)
    
    print(f"✓ Project plan generated: {output_file}")

def generate_marketing(args):
    """Generate marketing materials."""
    print("📢 Generating marketing materials...")
    
    # Look for project data file
    project_data_file = Path("project_data.yaml")
    if not project_data_file.exists():
        print("❌ Error: project_data.yaml not found")
        print("Make sure you're in a project directory or create a project first")
        return
    
    # Load project data
    import yaml
    with open(project_data_file, 'r') as f:
        project_data = yaml.safe_load(f)
    
    # Generate basic marketing content
    marketing_content = f"""# Marketing Materials

## Product Overview

**Product Name:** {project_data.get('project', {}).get('name', 'Unknown')}
**Tagline:** Streamline your workflow with our innovative solution

## Value Proposition

{project_data.get('project', {}).get('description', 'A powerful tool designed to improve productivity and efficiency.')}

## Key Benefits

### 🚀 **Increased Productivity**
- Automate repetitive tasks
- Streamline workflows
- Reduce manual effort by 50%

### 💡 **Easy to Use**
- Intuitive user interface
- Quick setup and onboarding
- Comprehensive documentation

### 🔒 **Secure & Reliable**
- Enterprise-grade security
- 99.9% uptime guarantee
- Regular updates and support

## Target Audience

### Primary Users
- **Small to Medium Businesses:** Looking to optimize operations
- **Project Managers:** Need better project tracking and management
- **Development Teams:** Require efficient collaboration tools

### User Personas
- **Sarah, Project Manager:** Needs better visibility into project progress
- **Mike, Team Lead:** Wants to streamline team communication
- **Lisa, Business Owner:** Looking to improve operational efficiency

## Competitive Advantages

### Unique Features
- **Smart Automation:** AI-powered workflow optimization
- **Real-time Collaboration:** Seamless team communication
- **Customizable Interface:** Adapts to your workflow

### Why Choose Us?
- **Proven Results:** 95% customer satisfaction rate
- **Expert Support:** Dedicated customer success team
- **Continuous Innovation:** Regular feature updates

## Pricing Strategy

### Starter Plan - $29/month
- Up to 5 team members
- Basic features
- Email support

### Professional Plan - $79/month
- Up to 25 team members
- Advanced features
- Priority support

### Enterprise Plan - Custom
- Unlimited team members
- All features
- Dedicated support

## Marketing Channels

### Digital Marketing
- **Website:** SEO-optimized landing pages
- **Social Media:** LinkedIn, Twitter, Facebook
- **Content Marketing:** Blog posts, case studies, whitepapers

### Traditional Marketing
- **Industry Events:** Trade shows and conferences
- **Partnerships:** Integration with popular tools
- **Referral Program:** Customer referral incentives

## Success Metrics

### Key Performance Indicators
- **Customer Acquisition Cost (CAC):** < $200
- **Customer Lifetime Value (CLV):** > $2,000
- **Conversion Rate:** > 3%
- **Churn Rate:** < 5% monthly

### Marketing Goals
- **Q1:** 100 new customers
- **Q2:** 250 new customers
- **Q3:** 500 new customers
- **Q4:** 1,000 new customers

## Call to Action

### Get Started Today
1. **Sign up** for a free trial
2. **Explore** our features
3. **Connect** with our team
4. **Scale** your business

### Contact Information
- **Website:** [Your Website URL]
- **Email:** contact@yourcompany.com
- **Phone:** (555) 123-4567

---
*Generated by DocGen CLI*
"""
    
    # Save marketing content
    output_file = Path("docs/marketing.md")
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write(marketing_content)
    
    print(f"✓ Marketing materials generated: {output_file}")

def validate_project(args):
    """Validate project data."""
    print("🔍 Validating project...")
    
    # Look for project data file
    project_data_file = Path("project_data.yaml")
    if not project_data_file.exists():
        print("❌ Error: project_data.yaml not found")
        print("Make sure you're in a project directory or create a project first")
        return
    
    # Load and validate project data
    import yaml
    try:
        with open(project_data_file, 'r') as f:
            project_data = yaml.safe_load(f)
        
        print("✓ Project data file found and loaded")
        
        # Basic validation
        if 'project' not in project_data:
            print("❌ Error: 'project' section missing from project data")
            return
        
        project_info = project_data['project']
        
        if 'name' not in project_info:
            print("❌ Error: Project name missing")
        else:
            print(f"✓ Project name: {project_info['name']}")
        
        if 'description' not in project_info:
            print("⚠️  Warning: Project description missing")
        else:
            print(f"✓ Project description: {project_info['description']}")
        
        if 'version' not in project_info:
            print("⚠️  Warning: Project version missing")
        else:
            print(f"✓ Project version: {project_info['version']}")
        
        # Check for generated documents
        docs_dir = Path("docs")
        if docs_dir.exists():
            doc_files = list(docs_dir.glob("*.md"))
            if doc_files:
                print(f"✓ Found {len(doc_files)} generated documents:")
                for doc_file in doc_files:
                    print(f"  - {doc_file.name}")
            else:
                print("⚠️  No generated documents found in docs/ directory")
        else:
            print("⚠️  No docs/ directory found")
        
        print("\n✅ Project validation completed!")
        
    except yaml.YAMLError as e:
        print(f"❌ Error parsing YAML file: {e}")
    except Exception as e:
        print(f"❌ Error validating project: {e}")

if __name__ == "__main__":
    main()
