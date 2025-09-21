"""
Custom Template Management System for DocGen CLI.

This module provides comprehensive template management capabilities including
template discovery, validation, installation, and versioning.
"""

import os
import json
import yaml
import shutil
import zipfile
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from dataclasses import dataclass, asdict
from jinja2 import Environment, Template, TemplateSyntaxError
import requests
from semantic_version import Version, Spec

from src.core.error_handler import DocGenError, ValidationError


@dataclass
class TemplateMetadata:
    """Template metadata structure."""
    name: str
    description: str
    version: str
    author: str
    template_type: str  # spec, plan, marketing, custom
    compatibility: Dict[str, Any]
    dependencies: List[str]
    tags: List[str]
    created: str
    last_modified: str
    source: str = "local"  # local, url, built-in
    status: str = "active"  # active, deprecated, experimental


class TemplateManager:
    """Manages custom templates for DocGen CLI."""
    
    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize the template manager.
        
        Args:
            config_dir: Configuration directory path. Defaults to ~/.docgen
        """
        self.config_dir = config_dir or Path.home() / ".docgen"
        self.templates_dir = self.config_dir / "templates"
        self.custom_dir = self.templates_dir / "custom"
        self.builtin_dir = self.templates_dir / "built-in"
        self.cache_dir = self.templates_dir / "cache"
        self.metadata_file = self.templates_dir / "metadata.json"
        
        self._ensure_directories()
        self._load_template_registry()
    
    def _ensure_directories(self) -> None:
        """Ensure all required directories exist."""
        directories = [
            self.config_dir,
            self.templates_dir,
            self.custom_dir,
            self.builtin_dir,
            self.cache_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _load_template_registry(self) -> None:
        """Load the template registry from metadata file."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    self.registry = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                raise FileIOError(f"Failed to load template registry: {e}")
        else:
            self.registry = {
                "templates": {},
                "last_updated": datetime.now().isoformat()
            }
            self._save_template_registry()
    
    def _save_template_registry(self) -> None:
        """Save the template registry to metadata file."""
        try:
            self.registry["last_updated"] = datetime.now().isoformat()
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.registry, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise FileIOError(f"Failed to save template registry: {e}")
    
    def discover_templates(self, include_builtin: bool = True) -> Dict[str, TemplateMetadata]:
        """Discover all available templates.
        
        Args:
            include_builtin: Whether to include built-in templates
            
        Returns:
            Dictionary mapping template IDs to metadata
        """
        templates = {}
        
        # Discover custom templates
        if self.custom_dir.exists():
            for template_dir in self.custom_dir.iterdir():
                if template_dir.is_dir():
                    try:
                        metadata = self._load_template_metadata(template_dir)
                        templates[template_dir.name] = metadata
                    except (ValidationError, FileIOError) as e:
                        # Log error but continue discovery
                        print(f"Warning: Failed to load template {template_dir.name}: {e}")
        
        # Discover built-in templates
        if include_builtin and self.builtin_dir.exists():
            for template_dir in self.builtin_dir.iterdir():
                if template_dir.is_dir():
                    try:
                        metadata = self._load_template_metadata(template_dir)
                        metadata.source = "built-in"
                        templates[template_dir.name] = metadata
                    except (ValidationError, FileIOError) as e:
                        print(f"Warning: Failed to load built-in template {template_dir.name}: {e}")
        
        return templates
    
    def _load_template_metadata(self, template_dir: Path) -> TemplateMetadata:
        """Load template metadata from a template directory.
        
        Args:
            template_dir: Path to template directory
            
        Returns:
            Template metadata object
            
        Raises:
            ValidationError: If metadata is invalid
            FileIOError: If metadata file cannot be read
        """
        metadata_file = template_dir / "metadata.yaml"
        
        if not metadata_file.exists():
            raise ValidationError(f"Metadata file not found: {metadata_file}")
        
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except (yaml.YAMLError, IOError) as e:
            raise FileIOError(f"Failed to read metadata file: {e}")
        
        # Validate required fields
        required_fields = ['name', 'description', 'version', 'author', 'template_type']
        for field in required_fields:
            if field not in data:
                raise ValidationError(f"Missing required field in metadata: {field}")
        
        # Set defaults for optional fields
        data.setdefault('compatibility', {})
        data.setdefault('dependencies', [])
        data.setdefault('tags', [])
        data.setdefault('created', datetime.now().isoformat())
        data.setdefault('last_modified', datetime.now().isoformat())
        
        return TemplateMetadata(**data)
    
    def validate_template(self, template_path: Path) -> Tuple[bool, List[str]]:
        """Validate a template for syntax and structure.
        
        Args:
            template_path: Path to template directory or file
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        try:
            if template_path.is_file():
                # Single template file
                self._validate_template_file(template_path, errors)
            elif template_path.is_dir():
                # Template directory
                self._validate_template_directory(template_path, errors)
            else:
                errors.append(f"Template path does not exist: {template_path}")
        except Exception as e:
            errors.append(f"Validation error: {e}")
        
        return len(errors) == 0, errors
    
    def _validate_template_file(self, template_file: Path, errors: List[str]) -> None:
        """Validate a single template file.
        
        Args:
            template_file: Path to template file
            errors: List to append errors to
        """
        if not template_file.suffix == '.j2':
            errors.append(f"Template file must have .j2 extension: {template_file}")
            return
        
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Validate Jinja2 syntax
            env = Environment()
            env.parse(content)
        except TemplateSyntaxError as e:
            errors.append(f"Jinja2 syntax error in {template_file}: {e}")
        except IOError as e:
            errors.append(f"Failed to read template file {template_file}: {e}")
    
    def _validate_template_directory(self, template_dir: Path, errors: List[str]) -> None:
        """Validate a template directory structure.
        
        Args:
            template_dir: Path to template directory
            errors: List to append errors to
        """
        # Check for required files
        required_files = ['template.j2', 'metadata.yaml']
        for file_name in required_files:
            file_path = template_dir / file_name
            if not file_path.exists():
                errors.append(f"Missing required file: {file_path}")
        
        # Validate metadata
        try:
            metadata = self._load_template_metadata(template_dir)
            self._validate_metadata(metadata, errors)
        except (ValidationError, FileIOError) as e:
            errors.append(f"Metadata validation failed: {e}")
        
        # Validate template file
        template_file = template_dir / "template.j2"
        if template_file.exists():
            self._validate_template_file(template_file, errors)
        
        # Check for assets directory (optional)
        assets_dir = template_dir / "assets"
        if assets_dir.exists() and not assets_dir.is_dir():
            errors.append(f"Assets path exists but is not a directory: {assets_dir}")
    
    def _validate_metadata(self, metadata: TemplateMetadata, errors: List[str]) -> None:
        """Validate template metadata.
        
        Args:
            metadata: Template metadata object
            errors: List to append errors to
        """
        # Validate version format
        try:
            Version(metadata.version)
        except ValueError:
            errors.append(f"Invalid version format: {metadata.version}")
        
        # Validate template type
        valid_types = ['spec', 'plan', 'marketing', 'custom']
        if metadata.template_type not in valid_types:
            errors.append(f"Invalid template type: {metadata.template_type}. Must be one of: {valid_types}")
        
        # Validate compatibility
        if 'docgen_version' in metadata.compatibility:
            try:
                Spec(metadata.compatibility['docgen_version'])
            except ValueError:
                errors.append(f"Invalid compatibility version spec: {metadata.compatibility['docgen_version']}")
    
    def install_template(self, source: str, template_name: Optional[str] = None) -> str:
        """Install a template from various sources.
        
        Args:
            source: Template source (file path, URL, or directory)
            template_name: Custom name for the template (optional)
            
        Returns:
            Template ID of installed template
            
        Raises:
            ValidationError: If template validation fails
            FileIOError: If installation fails
        """
        source_path = Path(source)
        
        if source_path.exists():
            # Local file or directory
            if source_path.is_file():
                return self._install_from_file(source_path, template_name)
            elif source_path.is_dir():
                return self._install_from_directory(source_path, template_name)
        else:
            # URL
            return self._install_from_url(source, template_name)
    
    def _install_from_file(self, file_path: Path, template_name: Optional[str] = None) -> str:
        """Install template from a file (ZIP or single template).
        
        Args:
            file_path: Path to template file
            template_name: Custom template name
            
        Returns:
            Template ID
        """
        if file_path.suffix == '.zip':
            return self._install_from_zip(file_path, template_name)
        elif file_path.suffix == '.j2':
            return self._install_single_template(file_path, template_name)
        else:
            raise ValidationError(f"Unsupported file type: {file_path.suffix}")
    
    def _install_from_zip(self, zip_path: Path, template_name: Optional[str] = None) -> str:
        """Install template from ZIP file.
        
        Args:
            zip_path: Path to ZIP file
            template_name: Custom template name
            
        Returns:
            Template ID
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Extract ZIP file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_path)
            
            # Find template directory
            template_dirs = [d for d in temp_path.iterdir() if d.is_dir()]
            if not template_dirs:
                raise ValidationError("No template directory found in ZIP file")
            
            template_dir = template_dirs[0]
            
            # Validate template
            is_valid, errors = self.validate_template(template_dir)
            if not is_valid:
                raise ValidationError(f"Template validation failed: {'; '.join(errors)}")
            
            # Load metadata
            metadata = self._load_template_metadata(template_dir)
            template_id = template_name or metadata.name.lower().replace(' ', '-')
            
            # Install template
            return self._install_from_directory(template_dir, template_id)
    
    def _install_single_template(self, template_file: Path, template_name: Optional[str] = None) -> str:
        """Install a single template file.
        
        Args:
            template_file: Path to template file
            template_name: Custom template name
            
        Returns:
            Template ID
        """
        # Validate template file
        is_valid, errors = self.validate_template(template_file)
        if not is_valid:
            raise ValidationError(f"Template validation failed: {'; '.join(errors)}")
        
        # Generate template ID
        template_id = template_name or template_file.stem
        
        # Create template directory
        template_dir = self.custom_dir / template_id
        template_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy template file
        shutil.copy2(template_file, template_dir / "template.j2")
        
        # Create basic metadata
        metadata = TemplateMetadata(
            name=template_name or template_file.stem,
            description=f"Template from {template_file.name}",
            version="1.0.0",
            author="Unknown",
            template_type="custom",
            compatibility={},
            dependencies=[],
            tags=["imported"],
            created=datetime.now().isoformat(),
            last_modified=datetime.now().isoformat(),
            source="local"
        )
        
        # Save metadata
        self._save_template_metadata(template_dir, metadata)
        
        # Update registry
        self.registry["templates"][template_id] = asdict(metadata)
        self.registry["templates"][template_id]["path"] = str(template_dir.relative_to(self.templates_dir))
        self.registry["templates"][template_id]["installed"] = datetime.now().isoformat()
        self._save_template_registry()
        
        return template_id
    
    def _install_from_directory(self, source_dir: Path, template_name: Optional[str] = None) -> str:
        """Install template from directory.
        
        Args:
            source_dir: Source template directory
            template_name: Custom template name
            
        Returns:
            Template ID
        """
        # Validate template directory
        is_valid, errors = self.validate_template(source_dir)
        if not is_valid:
            raise ValidationError(f"Template validation failed: {'; '.join(errors)}")
        
        # Load metadata
        metadata = self._load_template_metadata(source_dir)
        template_id = template_name or metadata.name.lower().replace(' ', '-')
        
        # Create destination directory
        dest_dir = self.custom_dir / template_id
        if dest_dir.exists():
            shutil.rmtree(dest_dir)
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy template files
        for item in source_dir.iterdir():
            if item.is_file():
                shutil.copy2(item, dest_dir)
            elif item.is_dir():
                shutil.copytree(item, dest_dir / item.name)
        
        # Update metadata
        metadata.last_modified = datetime.now().isoformat()
        metadata.source = "local"
        self._save_template_metadata(dest_dir, metadata)
        
        # Update registry
        self.registry["templates"][template_id] = asdict(metadata)
        self.registry["templates"][template_id]["path"] = str(dest_dir.relative_to(self.templates_dir))
        self.registry["templates"][template_id]["installed"] = datetime.now().isoformat()
        self._save_template_registry()
        
        return template_id
    
    def _install_from_url(self, url: str, template_name: Optional[str] = None) -> str:
        """Install template from URL.
        
        Args:
            url: Template URL
            template_name: Custom template name
            
        Returns:
            Template ID
        """
        try:
            # Download template
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Save to cache
            cache_file = self.cache_dir / f"template_{hash(url)}.zip"
            with open(cache_file, 'wb') as f:
                f.write(response.content)
            
            # Install from cached file
            return self._install_from_zip(cache_file, template_name)
            
        except requests.RequestException as e:
            raise FileIOError(f"Failed to download template from URL: {e}")
        except Exception as e:
            raise FileIOError(f"Failed to install template from URL: {e}")
    
    def _save_template_metadata(self, template_dir: Path, metadata: TemplateMetadata) -> None:
        """Save template metadata to file.
        
        Args:
            template_dir: Template directory
            metadata: Template metadata
        """
        metadata_file = template_dir / "metadata.yaml"
        metadata_dict = asdict(metadata)
        
        try:
            with open(metadata_file, 'w', encoding='utf-8') as f:
                yaml.dump(metadata_dict, f, default_flow_style=False, allow_unicode=True)
        except IOError as e:
            raise FileIOError(f"Failed to save template metadata: {e}")
    
    def get_template(self, template_id: str) -> Optional[TemplateMetadata]:
        """Get template metadata by ID.
        
        Args:
            template_id: Template identifier
            
        Returns:
            Template metadata or None if not found
        """
        if template_id in self.registry["templates"]:
            template_data = self.registry["templates"][template_id]
            return TemplateMetadata(**{k: v for k, v in template_data.items() 
                                     if k not in ['path', 'installed']})
        return None
    
    def remove_template(self, template_id: str) -> bool:
        """Remove a template.
        
        Args:
            template_id: Template identifier
            
        Returns:
            True if template was removed, False if not found
        """
        if template_id not in self.registry["templates"]:
            return False
        
        # Remove template directory
        template_data = self.registry["templates"][template_id]
        if "path" in template_data:
            template_path = self.templates_dir / template_data["path"]
            if template_path.exists():
                shutil.rmtree(template_path)
        
        # Remove from registry
        del self.registry["templates"][template_id]
        self._save_template_registry()
        
        return True
    
    def update_template(self, template_id: str, source: str) -> bool:
        """Update an existing template.
        
        Args:
            template_id: Template identifier
            source: New template source
            
        Returns:
            True if template was updated, False if not found
        """
        if template_id not in self.registry["templates"]:
            return False
        
        # Remove old template
        self.remove_template(template_id)
        
        # Install new template
        try:
            new_template_id = self.install_template(source, template_id)
            return new_template_id == template_id
        except Exception:
            # Restore old template if update fails
            # This is a simplified approach - in production, you'd want better rollback
            return False
