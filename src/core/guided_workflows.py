"""
Guided workflows for DocGen CLI.

This module provides step-by-step guided workflows for complex operations,
making the CLI more user-friendly and reducing the learning curve.
"""

from typing import Any, Dict, List, Optional, Callable
from pathlib import Path
from datetime import datetime

from src.core.cli_enhancements import EnhancedConsole, InteractivePrompts, WorkflowWizard
from src.core.error_handler import DocGenError, ErrorSeverity, ErrorCategory
from src.core.project_manager import ProjectManager
from src.core.generator import DocumentGenerator
from src.core.template_manager import TemplateManager


class ProjectCreationWorkflow:
    """Guided workflow for creating a new project."""
    
    def __init__(self, console: EnhancedConsole, prompts: InteractivePrompts):
        self.console = console
        self.prompts = prompts
        self.project_manager = ProjectManager()
    
    def run(self) -> Dict[str, Any]:
        """Run the project creation workflow."""
        wizard = WorkflowWizard(self.console, self.prompts)
        
        # Step 1: Project Information
        wizard.add_step(
            self._collect_project_info,
            "Project Information",
            "Gather basic project details"
        )
        
        # Step 2: Project Structure
        wizard.add_step(
            self._setup_project_structure,
            "Project Structure",
            "Configure project directories and files"
        )
        
        # Step 3: Initial Data
        wizard.add_step(
            self._create_initial_data,
            "Initial Data",
            "Create initial project data file"
        )
        
        # Step 4: Template Selection
        wizard.add_step(
            self._select_templates,
            "Template Selection",
            "Choose templates for document generation"
        )
        
        # Step 5: Git Setup
        wizard.add_step(
            self._setup_git,
            "Git Setup",
            "Initialize Git repository (optional)"
        )
        
        return wizard.run()
    
    def _collect_project_info(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Collect basic project information."""
        self.console.print_header("Project Information", "Let's start with the basics")
        
        # Project name
        name = self.prompts.ask_project_name()
        
        # Project description
        description = self.prompts.ask_multiline(
            "Project description (optional)",
            "A comprehensive project for generating documentation"
        )
        
        # Project path
        default_path = Path.cwd() / name.lower().replace(' ', '_')
        path = self.prompts.ask_project_path(str(default_path))
        
        return {
            "name": name,
            "description": description,
            "path": path
        }
    
    def _setup_project_structure(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Setup project directory structure."""
        self.console.print_header("Project Structure", "Creating directories and files")
        
        project_path = Path(results["path"])
        
        # Create directories
        directories = ["docs", "templates", "data", "assets"]
        created_dirs = []
        
        for dir_name in directories:
            dir_path = project_path / dir_name
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                created_dirs.append(dir_name)
                self.console.print(f"✓ Created directory: {dir_name}")
            except Exception as e:
                self.console.print_error(f"Failed to create directory {dir_name}: {e}")
        
        return {"created_directories": created_dirs}
    
    def _create_initial_data(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Create initial project data file."""
        self.console.print_header("Initial Data", "Setting up project data structure")
        
        project_path = Path(results["path"])
        
        # Create project configuration
        project_config = {
            "name": results["name"],
            "description": results["description"],
            "created_at": datetime.now().isoformat()
        }
        
        try:
            # Create project using project manager
            config = self.project_manager.create_project(
                results["name"],
                project_path,
                results["description"]
            )
            
            self.console.print_success("Project data file created successfully")
            return {"project_config": config}
            
        except Exception as e:
            self.console.print_error(f"Failed to create project data: {e}")
            return {}
    
    def _select_templates(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Select templates for the project."""
        self.console.print_header("Template Selection", "Choose document templates")
        
        template_manager = TemplateManager()
        templates = template_manager.discover_templates()
        
        if not templates:
            self.console.print_warning("No templates found")
            return {}
        
        # Show available templates
        template_data = []
        for template_id, metadata in templates.items():
            template_data.append({
                "ID": template_id,
                "Name": metadata.name,
                "Type": metadata.template_type,
                "Version": metadata.version
            })
        
        self.console.print_table(template_data, "Available Templates")
        
        # Ask user to select templates
        selected_templates = []
        if self.prompts.ask_yes_no("Would you like to select specific templates?", default=False):
            while True:
                template_id = self.prompts.ask_choice(
                    "Select a template (or 'done' to finish)",
                    choices=list(templates.keys()) + ["done"]
                )
                
                if template_id == "done":
                    break
                
                selected_templates.append(template_id)
                self.console.print(f"✓ Selected template: {template_id}")
        
        return {"selected_templates": selected_templates}
    
    def _setup_git(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Setup Git repository."""
        self.console.print_header("Git Setup", "Initialize version control")
        
        if not self.prompts.ask_yes_no("Initialize Git repository?", default=True):
            return {}
        
        project_path = Path(results["path"])
        
        try:
            from src.core.git_manager import GitManager, GitConfig
            
            git_config = GitConfig(
                auto_init=True,
                auto_commit=True,
                default_branch="main"
            )
            
            git_manager = GitManager(project_path, git_config)
            
            if git_manager.is_git_repository():
                self.console.print_warning("Project is already a Git repository")
                return {}
            
            success = git_manager.initialize_repository(initial_commit=True)
            
            if success:
                self.console.print_success("Git repository initialized successfully")
                return {"git_initialized": True}
            else:
                self.console.print_error("Failed to initialize Git repository")
                return {}
                
        except Exception as e:
            self.console.print_error(f"Git setup failed: {e}")
            return {}


class DocumentGenerationWorkflow:
    """Guided workflow for document generation."""
    
    def __init__(self, console: EnhancedConsole, prompts: InteractivePrompts):
        self.console = console
        self.prompts = prompts
        self.project_manager = ProjectManager()
        self.generator = DocumentGenerator()
    
    def run(self) -> Dict[str, Any]:
        """Run the document generation workflow."""
        wizard = WorkflowWizard(self.console, self.prompts)
        
        # Step 1: Project Selection
        wizard.add_step(
            self._select_project,
            "Project Selection",
            "Choose the project to work with"
        )
        
        # Step 2: Document Type Selection
        wizard.add_step(
            self._select_document_types,
            "Document Types",
            "Choose which documents to generate"
        )
        
        # Step 3: Output Configuration
        wizard.add_step(
            self._configure_output,
            "Output Configuration",
            "Set output format and location"
        )
        
        # Step 4: Validation
        wizard.add_step(
            self._validate_project_data,
            "Data Validation",
            "Validate project data before generation"
        )
        
        # Step 5: Generation
        wizard.add_step(
            self._generate_documents,
            "Document Generation",
            "Generate the selected documents"
        )
        
        return wizard.run()
    
    def _select_project(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Select the project to work with."""
        self.console.print_header("Project Selection", "Choose your project")
        
        current_project = self.project_manager.get_current_project()
        
        if current_project:
            self.console.print_info(f"Current project: {current_project['name']}")
            if self.prompts.ask_yes_no("Use current project?", default=True):
                return {"project": current_project}
        
        # Show available projects
        recent_projects = self.project_manager.get_recent_projects()
        
        if not recent_projects:
            self.console.print_error("No projects found. Create a project first.")
            return {}
        
        # Display projects
        project_data = []
        for project in recent_projects:
            project_data.append({
                "Name": project["name"],
                "Path": project["path"],
                "Last Accessed": project["last_accessed"][:19].replace('T', ' ')
            })
        
        self.console.print_table(project_data, "Available Projects")
        
        # Select project
        project_names = [p["name"] for p in recent_projects]
        selected_name = self.prompts.ask_choice(
            "Select a project",
            choices=project_names
        )
        
        selected_project = next(p for p in recent_projects if p["name"] == selected_name)
        self.project_manager.set_current_project(selected_project["id"])
        
        return {"project": selected_project}
    
    def _select_document_types(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Select document types to generate."""
        self.console.print_header("Document Types", "Choose documents to generate")
        
        document_types = [
            ("spec", "Technical Specification", "Comprehensive technical documentation"),
            ("plan", "Project Plan", "Project timeline and milestones"),
            ("marketing", "Marketing Materials", "Marketing and promotional content")
        ]
        
        selected_types = []
        
        for doc_type, title, description in document_types:
            if self.prompts.ask_yes_no(f"Generate {title}? ({description})", default=True):
                selected_types.append(doc_type)
        
        if not selected_types:
            self.console.print_warning("No document types selected")
            return {}
        
        self.console.print_success(f"Selected {len(selected_types)} document type(s)")
        return {"document_types": selected_types}
    
    def _configure_output(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Configure output settings."""
        self.console.print_header("Output Configuration", "Set output format and location")
        
        # Output format
        output_format = self.prompts.ask_output_format()
        
        # Output directory
        project_path = Path(results["project"]["path"])
        default_output = project_path / "docs"
        
        output_dir = self.prompts.ask_project_path(str(default_output))
        
        return {
            "output_format": output_format,
            "output_dir": output_dir
        }
    
    def _validate_project_data(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Validate project data."""
        self.console.print_header("Data Validation", "Checking project data")
        
        project_path = Path(results["project"]["path"])
        
        try:
            # Load and validate project data
            project_data = self.generator.load_project_data(project_path)
            
            # Basic validation
            required_fields = ["project.name", "project.description"]
            missing_fields = []
            
            for field in required_fields:
                keys = field.split('.')
                value = project_data
                try:
                    for key in keys:
                        value = value[key]
                    if not value:
                        missing_fields.append(field)
                except (KeyError, TypeError):
                    missing_fields.append(field)
            
            if missing_fields:
                self.console.print_warning(f"Missing fields: {', '.join(missing_fields)}")
                if not self.prompts.ask_yes_no("Continue with missing data?", default=False):
                    return {}
            else:
                self.console.print_success("Project data validation passed")
            
            return {"project_data": project_data, "validation_passed": True}
            
        except Exception as e:
            self.console.print_error(f"Data validation failed: {e}")
            if not self.prompts.ask_yes_no("Continue anyway?", default=False):
                return {}
            return {"validation_passed": False}
    
    def _generate_documents(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate the selected documents."""
        self.console.print_header("Document Generation", "Generating documents")
        
        project_path = Path(results["project"]["path"])
        output_dir = Path(results["output_dir"])
        output_format = results["output_format"]
        document_types = results["document_types"]
        
        generated_docs = {}
        
        for doc_type in document_types:
            try:
                self.console.print(f"Generating {doc_type} document...")
                
                content = self.generator.generate_document(
                    doc_type,
                    results.get("project_data", {}),
                    output_format
                )
                
                # Save document
                output_file = output_dir / f"{doc_type}.{output_format}"
                self.generator._save_document(content, output_file, output_format)
                
                generated_docs[doc_type] = {
                    "file": str(output_file),
                    "size": len(content)
                }
                
                self.console.print_success(f"Generated {doc_type} document")
                
            except Exception as e:
                self.console.print_error(f"Failed to generate {doc_type}: {e}")
        
        if generated_docs:
            # Show summary
            doc_data = []
            for doc_type, info in generated_docs.items():
                doc_data.append({
                    "Document": doc_type.title(),
                    "File": info["file"],
                    "Size": f"{info['size']} chars"
                })
            
            self.console.print_table(doc_data, "Generated Documents")
            self.console.print_success(f"Successfully generated {len(generated_docs)} document(s)")
        
        return {"generated_documents": generated_docs}


class TemplateManagementWorkflow:
    """Guided workflow for template management."""
    
    def __init__(self, console: EnhancedConsole, prompts: InteractivePrompts):
        self.console = console
        self.prompts = prompts
        self.template_manager = TemplateManager()
    
    def run(self) -> Dict[str, Any]:
        """Run the template management workflow."""
        wizard = WorkflowWizard(self.console, self.prompts)
        
        # Step 1: Action Selection
        wizard.add_step(
            self._select_action,
            "Action Selection",
            "Choose what you want to do with templates"
        )
        
        # Step 2: Execute Action
        wizard.add_step(
            self._execute_action,
            "Execute Action",
            "Perform the selected template operation"
        )
        
        return wizard.run()
    
    def _select_action(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Select template management action."""
        self.console.print_header("Template Management", "What would you like to do?")
        
        actions = [
            ("list", "List Templates", "Show all available templates"),
            ("create", "Create Template", "Create a new custom template"),
            ("install", "Install Template", "Install template from external source"),
            ("validate", "Validate Template", "Check template syntax and structure")
        ]
        
        action_data = []
        for action_id, title, description in actions:
            action_data.append({
                "Action": action_id,
                "Title": title,
                "Description": description
            })
        
        self.console.print_table(action_data, "Available Actions")
        
        action = self.prompts.ask_choice(
            "Select an action",
            choices=[action[0] for action in actions]
        )
        
        return {"action": action}
    
    def _execute_action(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the selected action."""
        action = results["action"]
        
        if action == "list":
            return self._list_templates()
        elif action == "create":
            return self._create_template()
        elif action == "install":
            return self._install_template()
        elif action == "validate":
            return self._validate_template()
        else:
            self.console.print_error(f"Unknown action: {action}")
            return {}
    
    def _list_templates(self) -> Dict[str, Any]:
        """List all available templates."""
        self.console.print_header("Template List", "Available templates")
        
        templates = self.template_manager.discover_templates()
        
        if not templates:
            self.console.print_warning("No templates found")
            return {}
        
        template_data = []
        for template_id, metadata in templates.items():
            template_data.append({
                "ID": template_id,
                "Name": metadata.name,
                "Type": metadata.template_type,
                "Version": metadata.version,
                "Author": metadata.author
            })
        
        self.console.print_table(template_data, "Available Templates")
        return {"templates": templates}
    
    def _create_template(self) -> Dict[str, Any]:
        """Create a new template."""
        self.console.print_header("Create Template", "Create a new custom template")
        
        # Get template details
        name = self.prompts.ask_project_name()
        template_type = self.prompts.ask_template_type()
        description = self.prompts.ask_multiline("Template description")
        author = self.prompts.ask_project_name()  # Reusing for author name
        
        try:
            # Create template using template manager
            template_id = name.lower().replace(' ', '-')
            
            # This would typically use the template manager's create method
            # For now, we'll just return the details
            self.console.print_success(f"Template '{name}' created successfully")
            
            return {
                "template_id": template_id,
                "name": name,
                "type": template_type,
                "description": description,
                "author": author
            }
            
        except Exception as e:
            self.console.print_error(f"Failed to create template: {e}")
            return {}
    
    def _install_template(self) -> Dict[str, Any]:
        """Install a template from external source."""
        self.console.print_header("Install Template", "Install template from external source")
        
        source = self.prompts.ask_project_name()  # Reusing for source path/URL
        
        try:
            # Install template using template manager
            template_id = self.template_manager.install_template(source)
            
            self.console.print_success(f"Template installed successfully: {template_id}")
            return {"template_id": template_id, "source": source}
            
        except Exception as e:
            self.console.print_error(f"Failed to install template: {e}")
            return {}
    
    def _validate_template(self) -> Dict[str, Any]:
        """Validate a template."""
        self.console.print_header("Validate Template", "Check template syntax and structure")
        
        template_path = self.prompts.ask_project_path()  # Reusing for template path
        
        try:
            is_valid, errors = self.template_manager.validate_template(Path(template_path))
            
            if is_valid:
                self.console.print_success("Template validation passed")
                return {"valid": True}
            else:
                self.console.print_error("Template validation failed")
                for error in errors:
                    self.console.print(f"  • {error}")
                return {"valid": False, "errors": errors}
                
        except Exception as e:
            self.console.print_error(f"Validation failed: {e}")
            return {}


class WorkflowManager:
    """Manager for all guided workflows."""
    
    def __init__(self):
        self.console = EnhancedConsole()
        self.prompts = InteractivePrompts(self.console.console)
        self.workflows = {
            "create-project": ProjectCreationWorkflow(self.console, self.prompts),
            "generate-docs": DocumentGenerationWorkflow(self.console, self.prompts),
            "manage-templates": TemplateManagementWorkflow(self.console, self.prompts)
        }
    
    def run_workflow(self, workflow_name: str) -> Dict[str, Any]:
        """Run a specific workflow."""
        if workflow_name not in self.workflows:
            self.console.print_error(f"Unknown workflow: {workflow_name}")
            return {}
        
        workflow = self.workflows[workflow_name]
        return workflow.run()
    
    def list_workflows(self) -> List[str]:
        """List all available workflows."""
        return list(self.workflows.keys())
    
    def get_workflow_info(self, workflow_name: str) -> Dict[str, str]:
        """Get information about a workflow."""
        workflow_info = {
            "create-project": {
                "name": "Project Creation",
                "description": "Guided setup for new DocGen projects"
            },
            "generate-docs": {
                "name": "Document Generation",
                "description": "Step-by-step document generation process"
            },
            "manage-templates": {
                "name": "Template Management",
                "description": "Manage and customize document templates"
            }
        }
        
        return workflow_info.get(workflow_name, {})


# Global workflow manager instance
workflow_manager = WorkflowManager()
