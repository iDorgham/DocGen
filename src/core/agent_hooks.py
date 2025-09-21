"""
Agent Hooks Framework for DocGen CLI Phase 3.

This module provides event-driven workflows, intelligent automation,
and automated quality gate enforcement for the driven workflow integration.
"""

import os
import time
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable, Set
from dataclasses import dataclass, asdict
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent, FileDeletedEvent
import threading
import queue

from src.core.error_handler import DocGenError, handle_error
from src.core.spec_validator import SpecValidator, create_spec_validator


@dataclass
class HookEvent:
    """Represents a hook event."""
    event_type: str
    file_path: str
    timestamp: datetime
    metadata: Dict[str, Any]
    event_id: str


@dataclass
class HookAction:
    """Represents an action to be taken by a hook."""
    action_type: str
    target: str
    parameters: Dict[str, Any]
    priority: int = 0
    retry_count: int = 0
    max_retries: int = 3


@dataclass
class HookRule:
    """Represents a hook rule configuration."""
    name: str
    pattern: str
    event_types: List[str]
    actions: List[HookAction]
    enabled: bool = True
    conditions: Dict[str, Any] = None


class FileSystemHookHandler(FileSystemEventHandler):
    """
    File system event handler for agent hooks.
    
    Monitors file system changes and triggers appropriate hooks.
    """
    
    def __init__(self, hook_manager: 'AgentHookManager'):
        """Initialize the file system hook handler."""
        self.hook_manager = hook_manager
        self.ignored_patterns = {
            '.git/', '__pycache__/', '.pytest_cache/', 'venv/', '.env',
            '*.pyc', '*.pyo', '*.log', '*.tmp', '.DS_Store'
        }
    
    def should_ignore(self, file_path: str) -> bool:
        """Check if a file should be ignored."""
        for pattern in self.ignored_patterns:
            if pattern in file_path or file_path.endswith(pattern.rstrip('/')):
                return True
        return False
    
    def on_modified(self, event):
        """Handle file modification events."""
        if not event.is_directory and not self.should_ignore(event.src_path):
            self._trigger_hook('file_modified', event.src_path, {
                'event_type': 'modified',
                'file_size': os.path.getsize(event.src_path) if os.path.exists(event.src_path) else 0
            })
    
    def on_created(self, event):
        """Handle file creation events."""
        if not event.is_directory and not self.should_ignore(event.src_path):
            self._trigger_hook('file_created', event.src_path, {
                'event_type': 'created',
                'file_size': os.path.getsize(event.src_path) if os.path.exists(event.src_path) else 0
            })
    
    def on_deleted(self, event):
        """Handle file deletion events."""
        if not event.is_directory and not self.should_ignore(event.src_path):
            self._trigger_hook('file_deleted', event.src_path, {
                'event_type': 'deleted'
            })
    
    def _trigger_hook(self, event_type: str, file_path: str, metadata: Dict[str, Any]):
        """Trigger a hook for the given event."""
        try:
            hook_event = HookEvent(
                event_type=event_type,
                file_path=file_path,
                timestamp=datetime.now(),
                metadata=metadata,
                event_id=self._generate_event_id(event_type, file_path)
            )
            
            self.hook_manager.process_event(hook_event)
            
        except Exception as e:
            print(f"Error processing hook event: {e}")


class AgentHookManager:
    """
    Manages agent hooks and event-driven workflows.
    
    Provides intelligent automation, context-aware task execution,
    and automated quality gate enforcement.
    """
    
    def __init__(self, project_root: Path):
        """Initialize the agent hook manager."""
        self.project_root = project_root
        self.hooks: Dict[str, HookRule] = {}
        self.event_queue = queue.Queue()
        self.observer = None
        self.running = False
        self.worker_thread = None
        
        # Initialize default hooks
        self._initialize_default_hooks()
        
        # Initialize spec validator for compliance checking
        self.spec_validator = create_spec_validator(project_root)
    
    def _initialize_default_hooks(self):
        """Initialize default hook rules."""
        default_hooks = [
            {
                "name": "spec_validation",
                "pattern": "assets/specs/*.md",
                "event_types": ["file_modified", "file_created"],
                "actions": [
                    {
                        "action_type": "validate_specs",
                        "target": "spec_compliance",
                        "parameters": {"auto_fix": False}
                    }
                ]
            },
            {
                "name": "code_quality_check",
                "pattern": "src/**/*.py",
                "event_types": ["file_modified", "file_created"],
                "actions": [
                    {
                        "action_type": "run_tests",
                        "target": "unit_tests",
                        "parameters": {"coverage": True}
                    },
                    {
                        "action_type": "lint_code",
                        "target": "code_quality",
                        "parameters": {"auto_fix": True}
                    }
                ]
            },
            {
                "name": "documentation_sync",
                "pattern": "assets/docs/**/*.md",
                "event_types": ["file_modified", "file_created"],
                "actions": [
                    {
                        "action_type": "update_docs",
                        "target": "documentation",
                        "parameters": {"auto_commit": True}
                    }
                ]
            },
            {
                "name": "template_validation",
                "pattern": "src/templates/*.j2",
                "event_types": ["file_modified", "file_created"],
                "actions": [
                    {
                        "action_type": "validate_template",
                        "target": "template_syntax",
                        "parameters": {"check_variables": True}
                    }
                ]
            }
        ]
        
        for hook_config in default_hooks:
            actions = [HookAction(**action) for action in hook_config["actions"]]
            hook_rule = HookRule(
                name=hook_config["name"],
                pattern=hook_config["pattern"],
                event_types=hook_config["event_types"],
                actions=actions
            )
            self.hooks[hook_config["name"]] = hook_rule
    
    def start_monitoring(self):
        """Start file system monitoring."""
        if self.running:
            return
        
        try:
            # Set up file system observer
            self.observer = Observer()
            event_handler = FileSystemHookHandler(self)
            
            # Watch the project root
            self.observer.schedule(event_handler, str(self.project_root), recursive=True)
            
            # Start the observer
            self.observer.start()
            
            # Start worker thread for processing events
            self.running = True
            self.worker_thread = threading.Thread(target=self._process_events, daemon=True)
            self.worker_thread.start()
            
            print(f"Agent hooks monitoring started for: {self.project_root}")
            
        except Exception as e:
            raise DocGenError(f"Failed to start agent hooks monitoring: {e}")
    
    def stop_monitoring(self):
        """Stop file system monitoring."""
        if not self.running:
            return
        
        self.running = False
        
        if self.observer:
            self.observer.stop()
            self.observer.join()
        
        if self.worker_thread:
            self.worker_thread.join(timeout=5)
        
        print("Agent hooks monitoring stopped")
    
    def process_event(self, event: HookEvent):
        """Process a hook event."""
        try:
            # Add event to queue for processing
            self.event_queue.put(event)
            
        except Exception as e:
            print(f"Error queuing hook event: {e}")
    
    def _process_events(self):
        """Process events from the queue."""
        while self.running:
            try:
                # Get event from queue with timeout
                event = self.event_queue.get(timeout=1)
                
                # Process the event
                self._execute_hooks_for_event(event)
                
                # Mark task as done
                self.event_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error processing event: {e}")
    
    def _execute_hooks_for_event(self, event: HookEvent):
        """Execute hooks for a specific event."""
        matching_hooks = self._find_matching_hooks(event)
        
        for hook in matching_hooks:
            if hook.enabled:
                self._execute_hook_actions(hook, event)
    
    def _find_matching_hooks(self, event: HookEvent) -> List[HookRule]:
        """Find hooks that match the event."""
        matching_hooks = []
        
        for hook in self.hooks.values():
            if event.event_type in hook.event_types:
                if self._matches_pattern(event.file_path, hook.pattern):
                    matching_hooks.append(hook)
        
        return matching_hooks
    
    def _matches_pattern(self, file_path: str, pattern: str) -> bool:
        """Check if a file path matches a pattern."""
        import fnmatch
        
        # Convert pattern to relative path from project root
        try:
            rel_path = os.path.relpath(file_path, self.project_root)
            return fnmatch.fnmatch(rel_path, pattern)
        except ValueError:
            return False
    
    def _execute_hook_actions(self, hook: HookRule, event: HookEvent):
        """Execute actions for a hook."""
        for action in hook.actions:
            try:
                self._execute_action(action, event)
            except Exception as e:
                print(f"Error executing action {action.action_type}: {e}")
                
                # Retry if configured
                if action.retry_count < action.max_retries:
                    action.retry_count += 1
                    time.sleep(1)  # Brief delay before retry
                    try:
                        self._execute_action(action, event)
                    except Exception as retry_error:
                        print(f"Retry failed for action {action.action_type}: {retry_error}")
    
    def _execute_action(self, action: HookAction, event: HookEvent):
        """Execute a specific action."""
        action_handlers = {
            'validate_specs': self._handle_validate_specs,
            'run_tests': self._handle_run_tests,
            'lint_code': self._handle_lint_code,
            'update_docs': self._handle_update_docs,
            'validate_template': self._handle_validate_template,
            'auto_commit': self._handle_auto_commit,
            'notify': self._handle_notify
        }
        
        handler = action_handlers.get(action.action_type)
        if handler:
            handler(action, event)
        else:
            print(f"Unknown action type: {action.action_type}")
    
    def _handle_validate_specs(self, action: HookAction, event: HookEvent):
        """Handle spec validation action."""
        print(f"Validating specs after {event.event_type}: {event.file_path}")
        
        try:
            validation_result = self.spec_validator.validate_spec_compliance()
            
            if not validation_result.is_valid:
                print(f"Spec validation failed: {validation_result.errors}")
                
                if action.parameters.get('auto_fix', False):
                    self._auto_fix_spec_issues(validation_result)
            else:
                print("Spec validation passed")
                
        except Exception as e:
            print(f"Error validating specs: {e}")
    
    def _handle_run_tests(self, action: HookAction, event: HookEvent):
        """Handle test execution action."""
        print(f"Running tests after {event.event_type}: {event.file_path}")
        
        try:
            # Import test runner
            import subprocess
            import sys
            
            # Run tests with coverage if requested
            cmd = [sys.executable, '-m', 'pytest']
            if action.parameters.get('coverage', False):
                cmd.extend(['--cov=src', '--cov-report=term-missing'])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("Tests passed")
            else:
                print(f"Tests failed: {result.stderr}")
                
        except Exception as e:
            print(f"Error running tests: {e}")
    
    def _handle_lint_code(self, action: HookAction, event: HookEvent):
        """Handle code linting action."""
        print(f"Linting code after {event.event_type}: {event.file_path}")
        
        try:
            import subprocess
            import sys
            
            # Run linter
            cmd = [sys.executable, '-m', 'flake8', event.file_path]
            if action.parameters.get('auto_fix', False):
                cmd.append('--fix')
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("Code linting passed")
            else:
                print(f"Code linting issues: {result.stdout}")
                
        except Exception as e:
            print(f"Error linting code: {e}")
    
    def _handle_update_docs(self, action: HookAction, event: HookEvent):
        """Handle documentation update action."""
        print(f"Updating documentation after {event.event_type}: {event.file_path}")
        
        try:
            # Update documentation index or regenerate related docs
            self._update_documentation_index(event.file_path)
            
            if action.parameters.get('auto_commit', False):
                self._auto_commit_docs(event.file_path)
                
        except Exception as e:
            print(f"Error updating documentation: {e}")
    
    def _handle_validate_template(self, action: HookAction, event: HookEvent):
        """Handle template validation action."""
        print(f"Validating template after {event.event_type}: {event.file_path}")
        
        try:
            from src.core.template_manager import TemplateManager
            
            template_manager = TemplateManager()
            is_valid, errors = template_manager.validate_template(Path(event.file_path))
            
            if is_valid:
                print("Template validation passed")
            else:
                print(f"Template validation failed: {errors}")
                
        except Exception as e:
            print(f"Error validating template: {e}")
    
    def _handle_auto_commit(self, action: HookAction, event: HookEvent):
        """Handle automatic commit action."""
        print(f"Auto-committing changes for: {event.file_path}")
        
        try:
            from src.core.git_manager import GitManager
            
            git_manager = GitManager(self.project_root)
            
            if git_manager.is_git_repository():
                commit_message = f"auto: {event.event_type} {os.path.basename(event.file_path)}"
                git_manager.commit_changes(commit_message, [event.file_path])
                print(f"Auto-committed: {commit_message}")
            else:
                print("Not a git repository, skipping auto-commit")
                
        except Exception as e:
            print(f"Error auto-committing: {e}")
    
    def _handle_notify(self, action: HookAction, event: HookEvent):
        """Handle notification action."""
        print(f"Notification: {action.parameters.get('message', 'Event occurred')}")
        
        # Could integrate with notification systems here
        # For now, just log the notification
    
    def _auto_fix_spec_issues(self, validation_result):
        """Attempt to auto-fix spec validation issues."""
        print("Attempting to auto-fix spec issues...")
        
        # This would implement automatic fixes for common spec issues
        # For now, just log the attempt
        print("Auto-fix functionality not yet implemented")
    
    def _update_documentation_index(self, file_path: str):
        """Update documentation index."""
        # This would update documentation indices or regenerate related docs
        print(f"Updating documentation index for: {file_path}")
    
    def _auto_commit_docs(self, file_path: str):
        """Auto-commit documentation changes."""
        try:
            from src.core.git_manager import GitManager
            
            git_manager = GitManager(self.project_root)
            
            if git_manager.is_git_repository():
                commit_message = f"docs: update {os.path.basename(file_path)}"
                git_manager.commit_changes(commit_message, [file_path])
                print(f"Auto-committed docs: {commit_message}")
                
        except Exception as e:
            print(f"Error auto-committing docs: {e}")
    
    def add_hook(self, hook: HookRule):
        """Add a new hook rule."""
        self.hooks[hook.name] = hook
        print(f"Added hook: {hook.name}")
    
    def remove_hook(self, hook_name: str):
        """Remove a hook rule."""
        if hook_name in self.hooks:
            del self.hooks[hook_name]
            print(f"Removed hook: {hook_name}")
        else:
            print(f"Hook not found: {hook_name}")
    
    def enable_hook(self, hook_name: str):
        """Enable a hook rule."""
        if hook_name in self.hooks:
            self.hooks[hook_name].enabled = True
            print(f"Enabled hook: {hook_name}")
        else:
            print(f"Hook not found: {hook_name}")
    
    def disable_hook(self, hook_name: str):
        """Disable a hook rule."""
        if hook_name in self.hooks:
            self.hooks[hook_name].enabled = False
            print(f"Disabled hook: {hook_name}")
        else:
            print(f"Hook not found: {hook_name}")
    
    def get_hook_status(self) -> Dict[str, Any]:
        """Get status of all hooks."""
        return {
            "total_hooks": len(self.hooks),
            "enabled_hooks": len([h for h in self.hooks.values() if h.enabled]),
            "disabled_hooks": len([h for h in self.hooks.values() if not h.enabled]),
            "monitoring_active": self.running,
            "hooks": {name: {
                "enabled": hook.enabled,
                "pattern": hook.pattern,
                "event_types": hook.event_types,
                "actions": len(hook.actions)
            } for name, hook in self.hooks.items()}
        }
    
    def _generate_event_id(self, event_type: str, file_path: str) -> str:
        """Generate a unique event ID."""
        content = f"{event_type}:{file_path}:{time.time()}"
        return hashlib.md5(content.encode()).hexdigest()[:8]


def create_agent_hook_manager(project_root: Path) -> AgentHookManager:
    """
    Factory function to create an agent hook manager.
    
    Args:
        project_root: Root directory of the project
        
    Returns:
        Initialized AgentHookManager instance
    """
    return AgentHookManager(project_root)
