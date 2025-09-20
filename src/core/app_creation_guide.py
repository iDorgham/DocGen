"""
App and Website Creation Guide for DocGen CLI.

This module provides comprehensive guidance for users to create
their apps or websites with step-by-step assistance.
"""

from typing import Any, Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime
import json

from src.core.cli_enhancements import EnhancedConsole, ProgressIndicator
from src.core.error_handler import DocGenError, ErrorSeverity, ErrorCategory


class AppCreationGuide:
    """Comprehensive guide for app and website creation."""
    
    def __init__(self, console: EnhancedConsole):
        self.console = console
        self.progress = ProgressIndicator(console)
        self.app_templates = self._load_app_templates()
        self.website_templates = self._load_website_templates()
    
    def _load_app_templates(self) -> Dict[str, Any]:
        """Load available app templates."""
        return {
            "web-app": {
                "name": "Web Application",
                "description": "Full-stack web application with frontend and backend",
                "tech_stack": ["React", "Node.js", "Express", "MongoDB"],
                "features": ["User Authentication", "Database Integration", "API Endpoints", "Responsive Design"],
                "complexity": "Advanced",
                "estimated_time": "4-8 weeks"
            },
            "mobile-app": {
                "name": "Mobile Application",
                "description": "Cross-platform mobile application",
                "tech_stack": ["React Native", "Expo", "Firebase"],
                "features": ["Cross-platform", "Push Notifications", "Offline Support", "App Store Ready"],
                "complexity": "Advanced",
                "estimated_time": "6-10 weeks"
            },
            "desktop-app": {
                "name": "Desktop Application",
                "description": "Cross-platform desktop application",
                "tech_stack": ["Electron", "React", "Node.js"],
                "features": ["Cross-platform", "Native Integration", "Auto-updater", "System Tray"],
                "complexity": "Intermediate",
                "estimated_time": "3-6 weeks"
            },
            "api-service": {
                "name": "API Service",
                "description": "RESTful API service with documentation",
                "tech_stack": ["Node.js", "Express", "PostgreSQL", "Swagger"],
                "features": ["REST API", "Authentication", "Database", "API Documentation"],
                "complexity": "Intermediate",
                "estimated_time": "2-4 weeks"
            },
            "cli-tool": {
                "name": "CLI Tool",
                "description": "Command-line interface tool",
                "tech_stack": ["Python", "Click", "Rich"],
                "features": ["Command Interface", "Configuration", "Help System", "Cross-platform"],
                "complexity": "Beginner",
                "estimated_time": "1-2 weeks"
            }
        }
    
    def _load_website_templates(self) -> Dict[str, Any]:
        """Load available website templates."""
        return {
            "business-website": {
                "name": "Business Website",
                "description": "Professional business website with CMS",
                "tech_stack": ["Next.js", "Tailwind CSS", "Strapi"],
                "features": ["Responsive Design", "CMS", "Contact Forms", "SEO Optimized"],
                "complexity": "Intermediate",
                "estimated_time": "2-4 weeks"
            },
            "portfolio-website": {
                "name": "Portfolio Website",
                "description": "Personal or professional portfolio website",
                "tech_stack": ["React", "Gatsby", "Contentful"],
                "features": ["Portfolio Gallery", "Blog", "Contact Form", "Dark Mode"],
                "complexity": "Beginner",
                "estimated_time": "1-3 weeks"
            },
            "ecommerce-website": {
                "name": "E-commerce Website",
                "description": "Online store with payment integration",
                "tech_stack": ["Next.js", "Stripe", "PostgreSQL"],
                "features": ["Product Catalog", "Shopping Cart", "Payment Processing", "Order Management"],
                "complexity": "Advanced",
                "estimated_time": "6-12 weeks"
            },
            "blog-website": {
                "name": "Blog Website",
                "description": "Content management and blogging platform",
                "tech_stack": ["Next.js", "MDX", "Vercel"],
                "features": ["Markdown Support", "SEO", "Comments", "Search"],
                "complexity": "Beginner",
                "estimated_time": "1-2 weeks"
            },
            "landing-page": {
                "name": "Landing Page",
                "description": "Single-page marketing website",
                "tech_stack": ["HTML", "CSS", "JavaScript"],
                "features": ["Responsive Design", "Contact Form", "Analytics", "Fast Loading"],
                "complexity": "Beginner",
                "estimated_time": "3-7 days"
            }
        }
    
    def start_creation_guide(self):
        """Start the interactive app/website creation guide."""
        self.console.print_panel(
            "🚀 Welcome to the App & Website Creation Guide!\n\n"
            "This guide will help you create your perfect app or website\n"
            "with step-by-step assistance and best practices.",
            "App & Website Creation Guide",
            "blue"
        )
        
        # Choose project type
        project_type = self.console.prompt_choice(
            "What would you like to create?",
            ["App", "Website", "Both"],
            default="App"
        )
        
        if project_type == "App":
            self._guide_app_creation()
        elif project_type == "Website":
            self._guide_website_creation()
        else:
            self._guide_full_stack_creation()
    
    def _guide_app_creation(self):
        """Guide user through app creation process."""
        self.console.print_info("Let's create your app! 📱")
        
        # Show available app templates
        self._show_app_templates()
        
        # Get user preferences
        app_type = self.console.prompt_choice(
            "What type of app do you want to create?",
            list(self.app_templates.keys()),
            default="web-app"
        )
        
        app_template = self.app_templates[app_type]
        
        # Show app details
        self._show_app_details(app_template)
        
        # Get project requirements
        requirements = self._gather_app_requirements(app_template)
        
        # Generate project structure
        self._generate_app_project(requirements)
    
    def _guide_website_creation(self):
        """Guide user through website creation process."""
        self.console.print_info("Let's create your website! 🌐")
        
        # Show available website templates
        self._show_website_templates()
        
        # Get user preferences
        website_type = self.console.prompt_choice(
            "What type of website do you want to create?",
            list(self.website_templates.keys()),
            default="business-website"
        )
        
        website_template = self.website_templates[website_type]
        
        # Show website details
        self._show_website_details(website_template)
        
        # Get project requirements
        requirements = self._gather_website_requirements(website_template)
        
        # Generate project structure
        self._generate_website_project(requirements)
    
    def _guide_full_stack_creation(self):
        """Guide user through full-stack creation process."""
        self.console.print_info("Let's create your full-stack project! 🚀")
        
        # Get app type
        app_type = self.console.prompt_choice(
            "What type of app do you want?",
            list(self.app_templates.keys()),
            default="web-app"
        )
        
        # Get website type
        website_type = self.console.prompt_choice(
            "What type of website do you want?",
            list(self.website_templates.keys()),
            default="business-website"
        )
        
        app_template = self.app_templates[app_type]
        website_template = self.website_templates[website_type]
        
        # Show combined details
        self._show_full_stack_details(app_template, website_template)
        
        # Get project requirements
        requirements = self._gather_full_stack_requirements(app_template, website_template)
        
        # Generate project structure
        self._generate_full_stack_project(requirements)
    
    def _show_app_templates(self):
        """Show available app templates."""
        table = self.console.create_table(
            ["Type", "Name", "Complexity", "Time", "Key Features"],
            title="Available App Templates"
        )
        
        for app_type, template in self.app_templates.items():
            table.add_row(
                app_type,
                template["name"],
                template["complexity"],
                template["estimated_time"],
                ", ".join(template["features"][:2]) + "..."
            )
        
        self.console.print_table(table)
    
    def _show_website_templates(self):
        """Show available website templates."""
        table = self.console.create_table(
            ["Type", "Name", "Complexity", "Time", "Key Features"],
            title="Available Website Templates"
        )
        
        for website_type, template in self.website_templates.items():
            table.add_row(
                website_type,
                template["name"],
                template["complexity"],
                template["estimated_time"],
                ", ".join(template["features"][:2]) + "..."
            )
        
        self.console.print_table(table)
    
    def _show_app_details(self, template: Dict[str, Any]):
        """Show detailed app information."""
        details = f"""
**{template['name']}**

**Description:** {template['description']}

**Tech Stack:**
{chr(10).join(f"• {tech}" for tech in template['tech_stack'])}

**Features:**
{chr(10).join(f"• {feature}" for feature in template['features'])}

**Complexity:** {template['complexity']}
**Estimated Time:** {template['estimated_time']}
"""
        
        self.console.print_panel(details, "App Details", "green")
    
    def _show_website_details(self, template: Dict[str, Any]):
        """Show detailed website information."""
        details = f"""
**{template['name']}**

**Description:** {template['description']}

**Tech Stack:**
{chr(10).join(f"• {tech}" for tech in template['tech_stack'])}

**Features:**
{chr(10).join(f"• {feature}" for feature in template['features'])}

**Complexity:** {template['complexity']}
**Estimated Time:** {template['estimated_time']}
"""
        
        self.console.print_panel(details, "Website Details", "green")
    
    def _show_full_stack_details(self, app_template: Dict[str, Any], website_template: Dict[str, Any]):
        """Show combined app and website details."""
        details = f"""
**Full-Stack Project: {app_template['name']} + {website_template['name']}**

**App Component:**
• {app_template['description']}
• Tech Stack: {', '.join(app_template['tech_stack'])}

**Website Component:**
• {website_template['description']}
• Tech Stack: {', '.join(website_template['tech_stack'])}

**Combined Features:**
• {', '.join(app_template['features'][:3])}
• {', '.join(website_template['features'][:3])}

**Complexity:** Advanced
**Estimated Time:** 8-16 weeks
"""
        
        self.console.print_panel(details, "Full-Stack Project Details", "green")
    
    def _gather_app_requirements(self, template: Dict[str, Any]) -> Dict[str, Any]:
        """Gather app-specific requirements."""
        self.console.print_info("Let's gather your app requirements...")
        
        requirements = {
            "type": "app",
            "template": template,
            "project_name": self.console.prompt_input("Project name"),
            "description": self.console.prompt_input("Project description"),
            "target_platforms": self._get_target_platforms(),
            "features": self._select_features(template["features"]),
            "database": self._select_database(),
            "authentication": self.console.prompt_confirm("Do you need user authentication?"),
            "deployment": self._select_deployment_platform(),
            "budget": self._get_budget_range(),
            "timeline": self._get_timeline()
        }
        
        return requirements
    
    def _gather_website_requirements(self, template: Dict[str, Any]) -> Dict[str, Any]:
        """Gather website-specific requirements."""
        self.console.print_info("Let's gather your website requirements...")
        
        requirements = {
            "type": "website",
            "template": template,
            "project_name": self.console.prompt_input("Project name"),
            "description": self.console.prompt_input("Project description"),
            "target_audience": self.console.prompt_input("Target audience"),
            "features": self._select_features(template["features"]),
            "content_management": self.console.prompt_confirm("Do you need a CMS?"),
            "ecommerce": self.console.prompt_confirm("Do you need e-commerce features?"),
            "seo": self.console.prompt_confirm("Do you need SEO optimization?"),
            "analytics": self.console.prompt_confirm("Do you need analytics integration?"),
            "deployment": self._select_deployment_platform(),
            "budget": self._get_budget_range(),
            "timeline": self._get_timeline()
        }
        
        return requirements
    
    def _gather_full_stack_requirements(self, app_template: Dict[str, Any], website_template: Dict[str, Any]) -> Dict[str, Any]:
        """Gather full-stack project requirements."""
        self.console.print_info("Let's gather your full-stack project requirements...")
        
        requirements = {
            "type": "full-stack",
            "app_template": app_template,
            "website_template": website_template,
            "project_name": self.console.prompt_input("Project name"),
            "description": self.console.prompt_input("Project description"),
            "target_platforms": self._get_target_platforms(),
            "app_features": self._select_features(app_template["features"]),
            "website_features": self._select_features(website_template["features"]),
            "database": self._select_database(),
            "authentication": self.console.prompt_confirm("Do you need user authentication?"),
            "api_integration": self.console.prompt_confirm("Do you need API integration between app and website?"),
            "deployment": self._select_deployment_platform(),
            "budget": self._get_budget_range(),
            "timeline": self._get_timeline()
        }
        
        return requirements
    
    def _get_target_platforms(self) -> List[str]:
        """Get target platforms for the app."""
        platforms = self.console.prompt_multiple_choice(
            "Select target platforms:",
            ["Web", "iOS", "Android", "Desktop", "All Platforms"],
            default=["Web"]
        )
        return platforms
    
    def _select_features(self, available_features: List[str]) -> List[str]:
        """Select features from available options."""
        selected = self.console.prompt_multiple_choice(
            "Select features you need:",
            available_features,
            default=available_features[:3]
        )
        return selected
    
    def _select_database(self) -> str:
        """Select database type."""
        database = self.console.prompt_choice(
            "Select database type:",
            ["PostgreSQL", "MongoDB", "MySQL", "SQLite", "Firebase", "No Database"],
            default="PostgreSQL"
        )
        return database
    
    def _select_deployment_platform(self) -> str:
        """Select deployment platform."""
        platform = self.console.prompt_choice(
            "Select deployment platform:",
            ["Vercel", "Netlify", "AWS", "Google Cloud", "Azure", "Heroku", "DigitalOcean"],
            default="Vercel"
        )
        return platform
    
    def _get_budget_range(self) -> str:
        """Get budget range."""
        budget = self.console.prompt_choice(
            "What's your budget range?",
            ["$0-1,000", "$1,000-5,000", "$5,000-10,000", "$10,000-25,000", "$25,000+"],
            default="$1,000-5,000"
        )
        return budget
    
    def _get_timeline(self) -> str:
        """Get project timeline."""
        timeline = self.console.prompt_choice(
            "What's your timeline?",
            ["ASAP", "1-2 weeks", "1 month", "2-3 months", "3+ months"],
            default="1 month"
        )
        return timeline
    
    def _generate_app_project(self, requirements: Dict[str, Any]):
        """Generate app project structure and files."""
        self.console.print_info("Generating your app project...")
        
        with self.progress.create_progress() as progress:
            task = progress.add_task("Creating app project...", total=100)
            
            # Create project directory
            project_path = Path(requirements["project_name"])
            project_path.mkdir(exist_ok=True)
            progress.update(task, advance=20)
            
            # Generate project files
            self._generate_package_json(project_path, requirements)
            progress.update(task, advance=20)
            
            self._generate_readme(project_path, requirements)
            progress.update(task, advance=20)
            
            self._generate_project_structure(project_path, requirements)
            progress.update(task, advance=20)
            
            self._generate_config_files(project_path, requirements)
            progress.update(task, advance=20)
        
        self.console.print_success(f"✅ App project '{requirements['project_name']}' created successfully!")
        self._show_next_steps(requirements)
    
    def _generate_website_project(self, requirements: Dict[str, Any]):
        """Generate website project structure and files."""
        self.console.print_info("Generating your website project...")
        
        with self.progress.create_progress() as progress:
            task = progress.add_task("Creating website project...", total=100)
            
            # Create project directory
            project_path = Path(requirements["project_name"])
            project_path.mkdir(exist_ok=True)
            progress.update(task, advance=20)
            
            # Generate project files
            self._generate_package_json(project_path, requirements)
            progress.update(task, advance=20)
            
            self._generate_readme(project_path, requirements)
            progress.update(task, advance=20)
            
            self._generate_project_structure(project_path, requirements)
            progress.update(task, advance=20)
            
            self._generate_config_files(project_path, requirements)
            progress.update(task, advance=20)
        
        self.console.print_success(f"✅ Website project '{requirements['project_name']}' created successfully!")
        self._show_next_steps(requirements)
    
    def _generate_full_stack_project(self, requirements: Dict[str, Any]):
        """Generate full-stack project structure and files."""
        self.console.print_info("Generating your full-stack project...")
        
        with self.progress.create_progress() as progress:
            task = progress.add_task("Creating full-stack project...", total=100)
            
            # Create project directory
            project_path = Path(requirements["project_name"])
            project_path.mkdir(exist_ok=True)
            progress.update(task, advance=15)
            
            # Create app and website subdirectories
            app_path = project_path / "app"
            website_path = project_path / "website"
            app_path.mkdir(exist_ok=True)
            website_path.mkdir(exist_ok=True)
            progress.update(task, advance=15)
            
            # Generate app files
            self._generate_package_json(app_path, requirements, "app")
            progress.update(task, advance=20)
            
            # Generate website files
            self._generate_package_json(website_path, requirements, "website")
            progress.update(task, advance=20)
            
            # Generate shared files
            self._generate_readme(project_path, requirements)
            progress.update(task, advance=15)
            
            self._generate_project_structure(project_path, requirements)
            progress.update(task, advance=15)
        
        self.console.print_success(f"✅ Full-stack project '{requirements['project_name']}' created successfully!")
        self._show_next_steps(requirements)
    
    def _generate_package_json(self, project_path: Path, requirements: Dict[str, Any], component: str = None):
        """Generate package.json file."""
        template = requirements.get("template") or requirements.get("app_template") or requirements.get("website_template")
        
        package_data = {
            "name": requirements["project_name"],
            "version": "1.0.0",
            "description": requirements["description"],
            "main": "index.js",
            "scripts": {
                "dev": "next dev",
                "build": "next build",
                "start": "next start",
                "lint": "next lint"
            },
            "dependencies": {
                "next": "^14.0.0",
                "react": "^18.0.0",
                "react-dom": "^18.0.0"
            },
            "devDependencies": {
                "@types/node": "^20.0.0",
                "@types/react": "^18.0.0",
                "@types/react-dom": "^18.0.0",
                "typescript": "^5.0.0"
            }
        }
        
        # Add component-specific dependencies
        if component == "app":
            package_data["dependencies"].update({
                "express": "^4.18.0",
                "mongoose": "^7.0.0"
            })
        elif component == "website":
            package_data["dependencies"].update({
                "tailwindcss": "^3.3.0",
                "@tailwindcss/typography": "^0.5.0"
            })
        
        package_file = project_path / "package.json"
        with open(package_file, 'w') as f:
            json.dump(package_data, f, indent=2)
    
    def _generate_readme(self, project_path: Path, requirements: Dict[str, Any]):
        """Generate README.md file."""
        template = requirements.get("template") or requirements.get("app_template") or requirements.get("website_template")
        
        readme_content = f"""# {requirements['project_name']}

{requirements['description']}

## Project Type
{template['name']}

## Tech Stack
{', '.join(template['tech_stack'])}

## Features
{chr(10).join(f"- {feature}" for feature in requirements.get('features', template['features']))}

## Getting Started

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation
```bash
npm install
```

### Development
```bash
npm run dev
```

### Build
```bash
npm run build
```

## Project Structure
```
{requirements['project_name']}/
├── src/
├── public/
├── package.json
└── README.md
```

## Deployment
Deploy to: {requirements.get('deployment', 'Vercel')}

## Timeline
{requirements.get('timeline', '1 month')}

## Budget
{requirements.get('budget', '$1,000-5,000')}
"""
        
        readme_file = project_path / "README.md"
        with open(readme_file, 'w') as f:
            f.write(readme_content)
    
    def _generate_project_structure(self, project_path: Path, requirements: Dict[str, Any]):
        """Generate project directory structure."""
        # Create basic directory structure
        directories = [
            "src",
            "src/components",
            "src/pages",
            "src/styles",
            "public",
            "docs"
        ]
        
        for directory in directories:
            (project_path / directory).mkdir(parents=True, exist_ok=True)
    
    def _generate_config_files(self, project_path: Path, requirements: Dict[str, Any]):
        """Generate configuration files."""
        # Generate TypeScript config
        tsconfig = {
            "compilerOptions": {
                "target": "es5",
                "lib": ["dom", "dom.iterable", "es6"],
                "allowJs": True,
                "skipLibCheck": True,
                "strict": True,
                "forceConsistentCasingInFileNames": True,
                "noEmit": True,
                "esModuleInterop": True,
                "module": "esnext",
                "moduleResolution": "node",
                "resolveJsonModule": True,
                "isolatedModules": True,
                "jsx": "preserve",
                "incremental": True,
                "plugins": [{"name": "next"}]
            },
            "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
            "exclude": ["node_modules"]
        }
        
        tsconfig_file = project_path / "tsconfig.json"
        with open(tsconfig_file, 'w') as f:
            json.dump(tsconfig, f, indent=2)
    
    def _show_next_steps(self, requirements: Dict[str, Any]):
        """Show next steps for the user."""
        next_steps = f"""
## 🎉 Project Created Successfully!

### Next Steps:

1. **Navigate to your project:**
   ```bash
   cd {requirements['project_name']}
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   Visit http://localhost:3000

### Development Resources:

- **Documentation:** Check the `docs/` folder
- **Components:** Start building in `src/components/`
- **Pages:** Create pages in `src/pages/`
- **Styling:** Add styles in `src/styles/`

### Deployment:

When ready to deploy:
```bash
npm run build
npm run start
```

Deploy to: {requirements.get('deployment', 'Vercel')}

### Support:

- Check the README.md for detailed instructions
- Visit the documentation in the `docs/` folder
- Use `docgen help` for more assistance

Happy coding! 🚀
"""
        
        self.console.print_panel(next_steps, "Next Steps", "green")
    
    def show_app_templates(self):
        """Show all available app templates."""
        self._show_app_templates()
    
    def show_website_templates(self):
        """Show all available website templates."""
        self._show_website_templates()
    
    def show_tech_stack_guide(self):
        """Show tech stack selection guide."""
        guide = """
# Tech Stack Selection Guide

## Frontend Technologies

### React
- **Best for:** Interactive UIs, component-based architecture
- **Pros:** Large ecosystem, great developer tools, excellent performance
- **Cons:** Learning curve, frequent updates

### Vue.js
- **Best for:** Progressive web apps, easy learning curve
- **Pros:** Easy to learn, great documentation, flexible
- **Cons:** Smaller ecosystem than React

### Angular
- **Best for:** Enterprise applications, large teams
- **Pros:** Full framework, TypeScript support, enterprise-ready
- **Cons:** Steep learning curve, complex for small projects

## Backend Technologies

### Node.js
- **Best for:** JavaScript full-stack, real-time applications
- **Pros:** Same language as frontend, large ecosystem
- **Cons:** Single-threaded, callback complexity

### Python (Django/Flask)
- **Best for:** Rapid development, data-heavy applications
- **Pros:** Easy to learn, great for data science, secure
- **Cons:** Slower than compiled languages

### Go
- **Best for:** High-performance APIs, microservices
- **Pros:** Fast, concurrent, simple syntax
- **Cons:** Smaller ecosystem, less mature

## Databases

### PostgreSQL
- **Best for:** Complex queries, ACID compliance
- **Pros:** Powerful, reliable, JSON support
- **Cons:** More complex than NoSQL

### MongoDB
- **Best for:** Document storage, rapid prototyping
- **Pros:** Flexible schema, easy to scale
- **Cons:** Less ACID compliance, memory usage

### SQLite
- **Best for:** Small applications, development
- **Pros:** No setup, embedded, fast
- **Cons:** Limited concurrency, not for production

## Deployment Platforms

### Vercel
- **Best for:** Next.js, static sites, serverless
- **Pros:** Easy deployment, great DX, global CDN
- **Cons:** Vendor lock-in, limited backend

### AWS
- **Best for:** Enterprise, complex applications
- **Pros:** Comprehensive, scalable, reliable
- **Cons:** Complex, expensive, learning curve

### Netlify
- **Best for:** Static sites, JAMstack
- **Pros:** Easy deployment, form handling, CDN
- **Cons:** Limited backend functionality
"""
        
        self.console.print_markdown(guide, "Tech Stack Guide")
    
    def show_best_practices(self):
        """Show development best practices."""
        practices = """
# Development Best Practices

## Project Structure
- Keep components small and focused
- Use consistent naming conventions
- Separate concerns (UI, logic, data)
- Organize files by feature, not type

## Code Quality
- Write clean, readable code
- Use TypeScript for type safety
- Follow linting rules
- Write tests for critical functionality

## Performance
- Optimize images and assets
- Use lazy loading for components
- Implement caching strategies
- Monitor bundle size

## Security
- Validate all inputs
- Use HTTPS in production
- Implement proper authentication
- Keep dependencies updated

## Accessibility
- Use semantic HTML
- Provide alt text for images
- Ensure keyboard navigation
- Test with screen readers

## SEO
- Use proper meta tags
- Implement structured data
- Optimize page speed
- Create XML sitemaps

## Deployment
- Use environment variables
- Implement CI/CD pipelines
- Monitor application performance
- Set up error tracking
"""
        
        self.console.print_markdown(practices, "Best Practices Guide")


# Global app creation guide instance
app_creation_guide = AppCreationGuide(EnhancedConsole())
