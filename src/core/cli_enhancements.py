"""
Enhanced CLI interface components for DocGen.

This module provides rich terminal formatting, progress indicators,
and interactive components to enhance the developer experience.
"""

import time
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
from datetime import datetime

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn
from rich.prompt import Prompt, Confirm, IntPrompt, FloatPrompt
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.tree import Tree
from rich.align import Align
from rich.columns import Columns
from rich.layout import Layout
from rich.live import Live
from rich.status import Status
from rich.spinner import Spinner
from rich import box
from rich.rule import Rule

from src.core.error_handler import DocGenError, ErrorSeverity, ErrorCategory


class EnhancedConsole:
    """Enhanced console with rich formatting and interactive features."""
    
    def __init__(self):
        self.console = Console()
        self._progress_tasks = {}
    
    def print_success(self, message: str, title: str = "Success") -> None:
        """Print a success message with green styling."""
        panel = Panel(
            f"[green]✓[/green] {message}",
            title=f"[green]{title}[/green]",
            border_style="green",
            box=box.ROUNDED
        )
        self.console.print(panel)
    
    def print_error(self, message: str, title: str = "Error", suggestions: List[str] = None) -> None:
        """Print an error message with red styling and suggestions."""
        content = f"[red]✗[/red] {message}"
        if suggestions:
            content += "\n\n[yellow]Suggestions:[/yellow]"
            for suggestion in suggestions:
                content += f"\n  • {suggestion}"
        
        panel = Panel(
            content,
            title=f"[red]{title}[/red]",
            border_style="red",
            box=box.ROUNDED
        )
        self.console.print(panel)
    
    def print_warning(self, message: str, title: str = "Warning") -> None:
        """Print a warning message with yellow styling."""
        panel = Panel(
            f"[yellow]⚠[/yellow] {message}",
            title=f"[yellow]{title}[/yellow]",
            border_style="yellow",
            box=box.ROUNDED
        )
        self.console.print(panel)
    
    def print_info(self, message: str, title: str = "Info") -> None:
        """Print an info message with blue styling."""
        panel = Panel(
            f"[blue]ℹ[/blue] {message}",
            title=f"[blue]{title}[/blue]",
            border_style="blue",
            box=box.ROUNDED
        )
        self.console.print(panel)
    
    def print_header(self, title: str, subtitle: str = None) -> None:
        """Print a styled header."""
        header_text = f"[bold blue]{title}[/bold blue]"
        if subtitle:
            header_text += f"\n[dim]{subtitle}[/dim]"
        
        self.console.print()
        self.console.print(Rule(header_text, style="blue"))
        self.console.print()
    
    def print_footer(self, message: str = "Operation completed") -> None:
        """Print a styled footer."""
        self.console.print()
        self.console.print(Rule(f"[green]{message}[/green]", style="green"))
        self.console.print()
    
    def print_table(self, data: List[Dict[str, Any]], title: str = None, 
                   columns: List[str] = None, styles: Dict[str, str] = None) -> None:
        """Print data in a formatted table."""
        if not data:
            self.print_warning("No data to display")
            return
        
        table = Table(title=title, box=box.ROUNDED, show_header=True, header_style="bold blue")
        
        # Determine columns
        if columns:
            table_columns = columns
        else:
            table_columns = list(data[0].keys())
        
        # Add columns with styles
        for col in table_columns:
            style = styles.get(col, "white") if styles else "white"
            table.add_column(col.replace('_', ' ').title(), style=style)
        
        # Add rows
        for row in data:
            table.add_row(*[str(row.get(col, "")) for col in table_columns])
        
        self.console.print(table)
    
    def print_tree(self, data: Dict[str, Any], title: str = "Structure") -> None:
        """Print hierarchical data as a tree."""
        tree = Tree(f"[bold blue]{title}[/bold blue]")
        
        def add_node(parent, data_dict, prefix=""):
            for key, value in data_dict.items():
                if isinstance(value, dict):
                    node = parent.add(f"[cyan]{key}[/cyan]")
                    add_node(node, value, prefix + "  ")
                elif isinstance(value, list):
                    node = parent.add(f"[cyan]{key}[/cyan] ([yellow]{len(value)} items[/yellow])")
                    for i, item in enumerate(value[:5]):  # Show first 5 items
                        if isinstance(item, dict):
                            item_node = node.add(f"[dim]Item {i+1}[/dim]")
                            add_node(item_node, item, prefix + "    ")
                        else:
                            node.add(f"[dim]{item}[/dim]")
                    if len(value) > 5:
                        node.add(f"[dim]... and {len(value) - 5} more[/dim]")
                else:
                    parent.add(f"[cyan]{key}[/cyan]: [white]{value}[/white]")
        
        add_node(tree, data)
        self.console.print(tree)
    
    def print_code(self, code: str, language: str = "python", title: str = None) -> None:
        """Print code with syntax highlighting."""
        syntax = Syntax(code, language, theme="monokai", line_numbers=True)
        if title:
            panel = Panel(syntax, title=f"[bold blue]{title}[/bold blue]", border_style="blue")
            self.console.print(panel)
        else:
            self.console.print(syntax)
    
    def print_markdown(self, markdown_text: str, title: str = None) -> None:
        """Print markdown content."""
        markdown = Markdown(markdown_text)
        if title:
            panel = Panel(markdown, title=f"[bold blue]{title}[/bold blue]", border_style="blue")
            self.console.print(panel)
        else:
            self.console.print(markdown)


class ProgressManager:
    """Manager for progress indicators and long-running operations."""
    
    def __init__(self, console: Console):
        self.console = console
        self._progress = None
        self._tasks = {}
    
    def start_progress(self, total: int = 100, description: str = "Processing...") -> str:
        """Start a progress bar and return task ID."""
        if self._progress is None:
            self._progress = Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                TimeElapsedColumn(),
                console=self.console
            )
            self._progress.start()
        
        task_id = self._progress.add_task(description, total=total)
        self._tasks[task_id] = {"total": total, "description": description}
        return str(task_id)
    
    def update_progress(self, task_id: str, advance: int = 1, description: str = None) -> None:
        """Update progress for a task."""
        if self._progress and task_id in self._tasks:
            if description:
                self._progress.update(task_id, description=description)
            self._progress.advance(task_id, advance)
    
    def complete_progress(self, task_id: str, description: str = "Completed") -> None:
        """Mark a task as completed."""
        if self._progress and task_id in self._tasks:
            self._progress.update(task_id, description=description, completed=True)
            del self._tasks[task_id]
    
    def stop_progress(self) -> None:
        """Stop all progress indicators."""
        if self._progress:
            self._progress.stop()
            self._progress = None
            self._tasks.clear()
    
    def with_progress(self, total: int, description: str = "Processing..."):
        """Context manager for progress tracking."""
        return ProgressContext(self, total, description)


class ProgressContext:
    """Context manager for progress tracking."""
    
    def __init__(self, progress_manager: ProgressManager, total: int, description: str):
        self.progress_manager = progress_manager
        self.total = total
        self.description = description
        self.task_id = None
    
    def __enter__(self):
        self.task_id = self.progress_manager.start_progress(self.total, self.description)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.task_id:
            if exc_type is None:
                self.progress_manager.complete_progress(self.task_id, "Completed")
            else:
                self.progress_manager.complete_progress(self.task_id, "Failed")
    
    def update(self, advance: int = 1, description: str = None):
        """Update progress."""
        if self.task_id:
            self.progress_manager.update_progress(self.task_id, advance, description)


class InteractivePrompts:
    """Enhanced interactive prompts with validation and suggestions."""
    
    def __init__(self, console: Console):
        self.console = console
    
    def ask_project_name(self, default: str = None) -> str:
        """Ask for project name with validation."""
        while True:
            name = Prompt.ask(
                "[bold blue]Project name[/bold blue]",
                default=default or ""
            ).strip()
            
            if not name:
                self.console.print("[red]Project name cannot be empty[/red]")
                continue
            
            if len(name) < 2:
                self.console.print("[red]Project name must be at least 2 characters[/red]")
                continue
            
            if not name.replace('_', '').replace('-', '').isalnum():
                self.console.print("[red]Project name can only contain letters, numbers, hyphens, and underscores[/red]")
                continue
            
            return name
    
    def ask_project_path(self, default: str = None) -> Path:
        """Ask for project path with validation."""
        while True:
            path_str = Prompt.ask(
                "[bold blue]Project directory path[/bold blue]",
                default=default or ""
            ).strip()
            
            if not path_str:
                self.console.print("[red]Project path cannot be empty[/red]")
                continue
            
            try:
                path = Path(path_str).resolve()
                
                if path.exists() and any(path.iterdir()):
                    if not Confirm.ask(f"[yellow]Directory {path} already exists and is not empty. Continue?[/yellow]"):
                        continue
                
                return path
            except Exception as e:
                self.console.print(f"[red]Invalid path: {e}[/red]")
                continue
    
    def ask_template_type(self) -> str:
        """Ask for template type with choices."""
        return Prompt.ask(
            "[bold blue]Template type[/bold blue]",
            choices=["spec", "plan", "marketing", "custom"],
            default="custom"
        )
    
    def ask_output_format(self) -> str:
        """Ask for output format with choices."""
        return Prompt.ask(
            "[bold blue]Output format[/bold blue]",
            choices=["markdown", "html", "pdf"],
            default="markdown"
        )
    
    def ask_yes_no(self, question: str, default: bool = True) -> bool:
        """Ask a yes/no question with default."""
        return Confirm.ask(f"[bold blue]{question}[/bold blue]", default=default)
    
    def ask_number(self, question: str, min_value: int = None, max_value: int = None, default: int = None) -> int:
        """Ask for a number with validation."""
        return IntPrompt.ask(
            f"[bold blue]{question}[/bold blue]",
            default=default,
            min=min_value,
            max=max_value
        )
    
    def ask_choice(self, question: str, choices: List[str], default: str = None) -> str:
        """Ask for a choice from a list."""
        return Prompt.ask(
            f"[bold blue]{question}[/bold blue]",
            choices=choices,
            default=default
        )
    
    def ask_multiline(self, question: str, default: str = "") -> str:
        """Ask for multiline input."""
        self.console.print(f"[bold blue]{question}[/bold blue]")
        self.console.print("[dim]Press Ctrl+D (Unix) or Ctrl+Z (Windows) when finished[/dim]")
        
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass
        
        return "\n".join(lines) if lines else default


class WorkflowWizard:
    """Guided workflow wizard for complex operations."""
    
    def __init__(self, console: EnhancedConsole, prompts: InteractivePrompts):
        self.console = console
        self.prompts = prompts
        self.steps = []
        self.current_step = 0
    
    def add_step(self, step_func, title: str, description: str = None):
        """Add a step to the workflow."""
        self.steps.append({
            "func": step_func,
            "title": title,
            "description": description
        })
    
    def run(self) -> Dict[str, Any]:
        """Run the complete workflow."""
        results = {}
        
        self.console.print_header("Workflow Wizard", "Guided setup process")
        
        for i, step in enumerate(self.steps, 1):
            self.console.print(f"[bold blue]Step {i}/{len(self.steps)}: {step['title']}[/bold blue]")
            if step['description']:
                self.console.print(f"[dim]{step['description']}[/dim]")
            self.console.print()
            
            try:
                step_result = step['func'](results)
                if step_result:
                    results.update(step_result)
                self.console.print_success(f"Step {i} completed")
            except KeyboardInterrupt:
                self.console.print_warning("Workflow cancelled by user")
                return results
            except Exception as e:
                self.console.print_error(f"Step {i} failed: {str(e)}")
                if not self.prompts.ask_yes_no("Continue with next step?", default=False):
                    return results
            
            self.console.print()
        
        self.console.print_footer("Workflow completed successfully")
        return results


class HelpSystem:
    """Enhanced help system with examples and cross-references."""
    
    def __init__(self, console: EnhancedConsole):
        self.console = console
        self.commands = {}
        self.examples = {}
    
    def add_command(self, name: str, description: str, examples: List[str] = None, 
                   related_commands: List[str] = None):
        """Add a command to the help system."""
        self.commands[name] = {
            "description": description,
            "examples": examples or [],
            "related_commands": related_commands or []
        }
    
    def show_command_help(self, command_name: str):
        """Show detailed help for a command."""
        if command_name not in self.commands:
            self.console.print_error(f"Command '{command_name}' not found")
            return
        
        cmd_info = self.commands[command_name]
        
        # Description
        self.console.print_header(f"Command: {command_name}")
        self.console.print(f"[bold]{cmd_info['description']}[/bold]")
        
        # Examples
        if cmd_info['examples']:
            self.console.print("\n[bold blue]Examples:[/bold blue]")
            for i, example in enumerate(cmd_info['examples'], 1):
                self.console.print(f"{i}. [cyan]{example}[/cyan]")
        
        # Related commands
        if cmd_info['related_commands']:
            self.console.print("\n[bold blue]Related Commands:[/bold blue]")
            for related in cmd_info['related_commands']:
                self.console.print(f"  • [cyan]{related}[/cyan]")
    
    def show_quick_start(self):
        """Show quick start guide."""
        quick_start = """
# DocGen CLI Quick Start

## 1. Create a New Project
```bash
docgen create --name "My Project" --path "./my-project"
```

## 2. Generate Documents
```bash
docgen spec --format markdown
docgen plan --format html
docgen marketing --format pdf
```

## 3. Validate Project
```bash
docgen validate
```

## 4. Git Integration
```bash
docgen git init
docgen git commit --auto
```

## Common Commands
- `docgen recent` - Show recent projects
- `docgen status` - Show current project status
- `docgen switch` - Switch between projects
- `docgen template list` - List available templates
"""
        self.console.print_markdown(quick_start, "Quick Start Guide")
    
    def show_troubleshooting(self):
        """Show troubleshooting guide."""
        troubleshooting = """
# Troubleshooting Guide

## Common Issues

### Project Not Found
- Use `docgen recent` to see available projects
- Use `docgen switch` to change current project
- Create a new project with `docgen create`

### Validation Errors
- Run `docgen validate` to check project data
- Use `--fix-issues` flag to attempt automatic fixes
- Check project_data.yaml file format

### Template Errors
- Use `docgen template list` to see available templates
- Use `docgen template validate <path>` to check template syntax
- Install missing templates with `docgen template install`

### Git Issues
- Run `docgen git status` to check repository status
- Initialize Git with `docgen git init`
- Check remote configuration with `docgen git remote`
"""
        self.console.print_markdown(troubleshooting, "Troubleshooting Guide")


# Global instances
enhanced_console = EnhancedConsole()
progress_manager = ProgressManager(enhanced_console.console)
interactive_prompts = InteractivePrompts(enhanced_console.console)
help_system = HelpSystem(enhanced_console)
