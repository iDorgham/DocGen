"""
Integration tests for performance requirements.

Tests performance benchmarks and resource usage.
"""

import os
import tempfile
import time
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from src.cli_main import main as cli


class TestPerformanceRequirements:
    """Test cases for performance requirements."""
    
    def test_project_creation_performance(self, cli_runner: CliRunner, temp_dir: Path):
        """Test project creation meets < 2 seconds requirement."""
        project_path = temp_dir / "performance_project.yaml"
        
        start_time = time.time()
        
        result = cli_runner.invoke(cli, [
            'project', 'create',
            '--name', 'Performance Test Project',
            '--description', 'A project for performance testing',
            '--version', '1.0.0',
            '--author', 'Performance Tester',
            '--email', 'perf@example.com',
            '--output', str(project_path)
        ])
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        assert result.exit_code == 0
        assert execution_time < 2.0, f"Project creation took {execution_time:.2f} seconds, should be < 2 seconds"
    
    def test_document_generation_performance(self, cli_runner: CliRunner, temp_dir: Path):
        """Test document generation meets < 5 seconds requirement."""
        # Create project
        project_path = temp_dir / "perf_project.yaml"
        create_result = cli_runner.invoke(cli, [
            'project', 'create',
            '--name', 'Performance Project',
            '--description', 'A project for performance testing',
            '--output', str(project_path)
        ])
        assert create_result.exit_code == 0
        
        # Create template
        templates_dir = temp_dir / "templates"
        templates_dir.mkdir()
        template_path = templates_dir / "perf_template.j2"
        template_path.write_text("""
# {{ project.name }}

## Description
{{ project.description }}

## Version
{{ project.version }}

## Author
{{ project.author }}

## Features
{% for feature in project.features %}
- {{ feature }}
{% endfor %}

## Requirements
{% for req in project.requirements %}
- {{ req }}
{% endfor %}
""")
        
        # Generate document and measure time
        output_dir = temp_dir / "output"
        output_dir.mkdir()
        output_path = output_dir / "perf_output.md"
        
        start_time = time.time()
        
        result = cli_runner.invoke(cli, [
            'generate',
            '--project', str(project_path),
            '--template', str(template_path),
            '--output', str(output_path)
        ])
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        assert result.exit_code == 0
        assert execution_time < 5.0, f"Document generation took {execution_time:.2f} seconds, should be < 5 seconds"
    
    def test_project_validation_performance(self, cli_runner: CliRunner, temp_dir: Path):
        """Test project validation meets < 3 seconds requirement."""
        # Create project
        project_path = temp_dir / "validation_project.yaml"
        create_result = cli_runner.invoke(cli, [
            'project', 'create',
            '--name', 'Validation Project',
            '--description', 'A project for validation performance testing',
            '--output', str(project_path)
        ])
        assert create_result.exit_code == 0
        
        # Validate project and measure time
        start_time = time.time()
        
        result = cli_runner.invoke(cli, [
            'project', 'validate',
            '--project', str(project_path)
        ])
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        assert result.exit_code == 0
        assert execution_time < 3.0, f"Project validation took {execution_time:.2f} seconds, should be < 3 seconds"
    
    def test_template_rendering_performance(self, cli_runner: CliRunner, temp_dir: Path):
        """Test template rendering meets < 2 seconds requirement."""
        # Create project
        project_path = temp_dir / "template_project.yaml"
        create_result = cli_runner.invoke(cli, [
            'project', 'create',
            '--name', 'Template Project',
            '--description', 'A project for template performance testing',
            '--output', str(project_path)
        ])
        assert create_result.exit_code == 0
        
        # Create complex template
        templates_dir = temp_dir / "templates"
        templates_dir.mkdir()
        template_path = templates_dir / "complex_template.j2"
        template_path.write_text("""
# {{ project.name }} - Complex Template

## Overview
{{ project.description }}

## Project Details
- **Name**: {{ project.name }}
- **Version**: {{ project.version }}
- **Author**: {{ project.author }}
- **Email**: {{ project.email }}

## Features
{% if project.features %}
{% for feature in project.features %}
### {{ loop.index }}. {{ feature }}
This is a detailed description of the feature.
{% endfor %}
{% else %}
No features specified.
{% endif %}

## Requirements
{% if project.requirements %}
{% for req in project.requirements %}
- {{ req }}
{% endfor %}
{% else %}
No requirements specified.
{% endif %}

## Keywords
{% if project.keywords %}
{% for keyword in project.keywords %}
- {{ keyword }}
{% endfor %}
{% else %}
No keywords specified.
{% endif %}

## Repository
{% if project.repository %}
Repository: {{ project.repository }}
{% else %}
No repository specified.
{% endif %}

## License
{% if project.license %}
License: {{ project.license }}
{% else %}
No license specified.
{% endif %}
""")
        
        # Generate document and measure template rendering time
        output_dir = temp_dir / "output"
        output_dir.mkdir()
        output_path = output_dir / "template_output.md"
        
        start_time = time.time()
        
        result = cli_runner.invoke(cli, [
            'generate',
            '--project', str(project_path),
            '--template', str(template_path),
            '--output', str(output_path)
        ])
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        assert result.exit_code == 0
        assert execution_time < 2.0, f"Template rendering took {execution_time:.2f} seconds, should be < 2 seconds"
    
    def test_concurrent_operations_performance(self, cli_runner: CliRunner, temp_dir: Path):
        """Test concurrent operations performance."""
        # Create multiple projects
        projects_dir = temp_dir / "projects"
        projects_dir.mkdir()
        
        project_paths = []
        for i in range(5):  # Test with 5 concurrent operations
            project_path = projects_dir / f"concurrent_project_{i}.yaml"
            create_result = cli_runner.invoke(cli, [
                'project', 'create',
                '--name', f'Concurrent Project {i}',
                '--description', f'A project for concurrent testing {i}',
                '--output', str(project_path)
            ])
            assert create_result.exit_code == 0
            project_paths.append(project_path)
        
        # Create template
        templates_dir = temp_dir / "templates"
        templates_dir.mkdir()
        template_path = templates_dir / "concurrent_template.j2"
        template_path.write_text("# {{ project.name }}\n\n{{ project.description }}")
        
        # Generate documents concurrently (simulate concurrent operations)
        output_dir = temp_dir / "output"
        output_dir.mkdir()
        
        start_time = time.time()
        
        for i, project_path in enumerate(project_paths):
            output_path = output_dir / f"concurrent_output_{i}.md"
            result = cli_runner.invoke(cli, [
                'generate',
                '--project', str(project_path),
                '--template', str(template_path),
                '--output', str(output_path)
            ])
            assert result.exit_code == 0
            assert output_path.exists()
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should handle 5 concurrent operations efficiently
        assert execution_time < 10.0, f"Concurrent operations took {execution_time:.2f} seconds, should be < 10 seconds"
    
    def test_memory_usage_performance(self, cli_runner: CliRunner, temp_dir: Path):
        """Test memory usage meets < 512MB requirement."""
        import psutil
        import os
        
        # Get current process
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Create large project with many features and requirements
        project_path = temp_dir / "memory_project.yaml"
        
        # Create project with large data
        large_features = [f"Feature {i}" for i in range(100)]
        large_requirements = [f"Requirement {i}" for i in range(100)]
        large_keywords = [f"keyword{i}" for i in range(50)]
        
        project_data = {
            "name": "Memory Test Project",
            "description": "A project for memory usage testing with large data",
            "version": "1.0.0",
            "author": "Memory Tester",
            "email": "memory@example.com",
            "features": large_features,
            "requirements": large_requirements,
            "keywords": large_keywords
        }
        
        import yaml
        with open(project_path, 'w') as f:
            yaml.dump(project_data, f)
        
        # Create template that processes all data
        templates_dir = temp_dir / "templates"
        templates_dir.mkdir()
        template_path = templates_dir / "memory_template.j2"
        template_path.write_text("""
# {{ project.name }}

## Description
{{ project.description }}

## Features ({{ project.features|length }} total)
{% for feature in project.features %}
- {{ feature }}
{% endfor %}

## Requirements ({{ project.requirements|length }} total)
{% for req in project.requirements %}
- {{ req }}
{% endfor %}

## Keywords ({{ project.keywords|length }} total)
{% for keyword in project.keywords %}
- {{ keyword }}
{% endfor %}
""")
        
        # Generate document
        output_dir = temp_dir / "output"
        output_dir.mkdir()
        output_path = output_dir / "memory_output.md"
        
        result = cli_runner.invoke(cli, [
            'generate',
            '--project', str(project_path),
            '--template', str(template_path),
            '--output', str(output_path)
        ])
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_used = final_memory - initial_memory
        
        assert result.exit_code == 0
        assert memory_used < 512, f"Memory usage was {memory_used:.2f}MB, should be < 512MB"
    
    def test_file_size_performance(self, cli_runner: CliRunner, temp_dir: Path):
        """Test generated file size meets < 10MB requirement."""
        # Create project
        project_path = temp_dir / "filesize_project.yaml"
        create_result = cli_runner.invoke(cli, [
            'project', 'create',
            '--name', 'File Size Project',
            '--description', 'A project for file size testing',
            '--output', str(project_path)
        ])
        assert create_result.exit_code == 0
        
        # Create template that generates large content
        templates_dir = temp_dir / "templates"
        templates_dir.mkdir()
        template_path = templates_dir / "large_template.j2"
        template_path.write_text("""
# {{ project.name }}

## Description
{{ project.description }}

## Large Content Section
{% for i in range(1000) %}
### Section {{ i }}
This is a large content section with detailed information about the project.
The content is repeated many times to test file size limits.
This section contains comprehensive documentation that would typically
be found in a large project documentation file.

**Details:**
- Item 1: Detailed description of the first item
- Item 2: Detailed description of the second item
- Item 3: Detailed description of the third item
- Item 4: Detailed description of the fourth item
- Item 5: Detailed description of the fifth item

**Additional Information:**
This section provides additional context and information that helps
understand the project better. It includes various details that would
be useful for developers and users of the project.

{% endfor %}
""")
        
        # Generate document
        output_dir = temp_dir / "output"
        output_dir.mkdir()
        output_path = output_dir / "large_output.md"
        
        result = cli_runner.invoke(cli, [
            'generate',
            '--project', str(project_path),
            '--template', str(template_path),
            '--output', str(output_path)
        ])
        
        assert result.exit_code == 0
        assert output_path.exists()
        
        # Check file size
        file_size = output_path.stat().st_size / 1024 / 1024  # MB
        assert file_size < 10, f"Generated file size was {file_size:.2f}MB, should be < 10MB"
