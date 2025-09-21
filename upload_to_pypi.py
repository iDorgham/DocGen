#!/usr/bin/env python3
"""
DocGen CLI - PyPI Upload Script
Uploads the DocGen CLI package to PyPI for public distribution.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt
import json

console = Console()

def run_command(command, description, check=True):
    """Run a command with rich progress indication."""
    with Progress(
        SpinnerColumn(),
        TextColumn(f"[bold blue]{description}..."),
        console=console,
    ) as progress:
        task = progress.add_task("", total=None)
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                check=check
            )
            progress.update(task, completed=True)
            return result
        except subprocess.CalledProcessError as e:
            console.print(f"[bold red]Error: {e}")
            console.print(f"[red]Command: {command}")
            console.print(f"[red]Output: {e.stdout}")
            console.print(f"[red]Error: {e.stderr}")
            return None

def check_prerequisites():
    """Check if all prerequisites are met."""
    console.print("\n[bold blue]🔍 Checking Prerequisites...")
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        console.print("[bold red]❌ pyproject.toml not found. Please run from project root.")
        return False
    
    # Check if virtual environment is activated
    if not os.environ.get('VIRTUAL_ENV'):
        console.print("[bold yellow]⚠️  Virtual environment not detected.")
        if not Confirm.ask("Continue anyway?"):
            return False
    
    # Check if build tools are installed
    try:
        import build
        import twine
        console.print("[bold green]✅ Build tools are available")
    except ImportError:
        console.print("[bold red]❌ Required packages not found.")
        console.print("Installing build and twine...")
        result = run_command("pip install build twine", "Installing build tools")
        if not result:
            return False
    
    return True

def clean_build_artifacts():
    """Clean previous build artifacts."""
    console.print("\n[bold blue]🧹 Cleaning Build Artifacts...")
    
    dirs_to_clean = ["dist", "build", "*.egg-info"]
    for pattern in dirs_to_clean:
        if pattern.endswith("*"):
            # Handle glob patterns
            import glob
            for path in glob.glob(pattern):
                if os.path.isdir(path):
                    shutil.rmtree(path)
                    console.print(f"[green]✅ Removed {path}")
        else:
            if os.path.exists(pattern):
                if os.path.isdir(pattern):
                    shutil.rmtree(pattern)
                else:
                    os.remove(pattern)
                console.print(f"[green]✅ Removed {pattern}")

def build_package():
    """Build the package for distribution."""
    console.print("\n[bold blue]🔨 Building Package...")
    
    # Build the package
    result = run_command("python -m build", "Building package")
    if not result:
        return False
    
    # Check if dist directory was created
    if not os.path.exists("dist"):
        console.print("[bold red]❌ Build failed - dist directory not created")
        return False
    
    # List built files
    dist_files = list(Path("dist").glob("*"))
    console.print(f"[bold green]✅ Package built successfully!")
    for file in dist_files:
        size = file.stat().st_size / 1024 / 1024  # MB
        console.print(f"  📦 {file.name} ({size:.2f} MB)")
    
    return True

def validate_package():
    """Validate the built package."""
    console.print("\n[bold blue]🔍 Validating Package...")
    
    # Check package with twine
    result = run_command("twine check dist/*", "Validating package")
    if not result:
        console.print("[bold red]❌ Package validation failed")
        return False
    
    console.print("[bold green]✅ Package validation passed!")
    return True

def upload_to_pypi():
    """Upload package to PyPI."""
    console.print("\n[bold blue]🚀 Uploading to PyPI...")
    
    # Check if we want to upload to test PyPI first
    use_test_pypi = Confirm.ask("Upload to Test PyPI first?", default=True)
    
    if use_test_pypi:
        console.print("[bold yellow]📤 Uploading to Test PyPI...")
        result = run_command(
            "twine upload --repository testpypi dist/*", 
            "Uploading to Test PyPI"
        )
        if not result:
            console.print("[bold red]❌ Test PyPI upload failed")
            return False
        
        console.print("[bold green]✅ Successfully uploaded to Test PyPI!")
        console.print("[bold blue]🔗 Test PyPI URL: https://test.pypi.org/project/docgen-cli/")
        
        # Ask if we should continue to production PyPI
        if not Confirm.ask("Upload to production PyPI?"):
            return True
    
    # Upload to production PyPI
    console.print("[bold yellow]📤 Uploading to Production PyPI...")
    result = run_command("twine upload dist/*", "Uploading to PyPI")
    if not result:
        console.print("[bold red]❌ PyPI upload failed")
        return False
    
    console.print("[bold green]✅ Successfully uploaded to PyPI!")
    console.print("[bold blue]🔗 PyPI URL: https://pypi.org/project/docgen-cli/")
    
    return True

def verify_upload():
    """Verify the upload was successful."""
    console.print("\n[bold blue]🔍 Verifying Upload...")
    
    # Wait a moment for PyPI to process
    import time
    console.print("Waiting for PyPI to process the upload...")
    time.sleep(10)
    
    # Try to install the package
    console.print("Testing package installation...")
    result = run_command(
        "pip install --no-cache-dir docgen-cli", 
        "Installing from PyPI", 
        check=False
    )
    
    if result and result.returncode == 0:
        console.print("[bold green]✅ Package successfully installed from PyPI!")
        
        # Test the CLI
        result = run_command("docgen --version", "Testing CLI", check=False)
        if result and result.returncode == 0:
            console.print("[bold green]✅ CLI is working correctly!")
        else:
            console.print("[bold yellow]⚠️  CLI test failed, but package was uploaded")
    else:
        console.print("[bold yellow]⚠️  Installation test failed, but package was uploaded")
    
    return True

def main():
    """Main upload process."""
    console.print(Panel.fit(
        "[bold blue]DocGen CLI - PyPI Upload Script[/bold blue]\n"
        "This script will upload DocGen CLI to PyPI for public distribution.",
        title="🚀 PyPI Upload"
    ))
    
    # Check prerequisites
    if not check_prerequisites():
        console.print("[bold red]❌ Prerequisites check failed")
        return 1
    
    # Clean build artifacts
    clean_build_artifacts()
    
    # Build package
    if not build_package():
        console.print("[bold red]❌ Package build failed")
        return 1
    
    # Validate package
    if not validate_package():
        console.print("[bold red]❌ Package validation failed")
        return 1
    
    # Upload to PyPI
    if not upload_to_pypi():
        console.print("[bold red]❌ PyPI upload failed")
        return 1
    
    # Verify upload
    verify_upload()
    
    # Success message
    console.print(Panel.fit(
        "[bold green]🎉 DocGen CLI Successfully Uploaded to PyPI![/bold green]\n\n"
        "📦 Package: docgen-cli\n"
        "🔗 PyPI URL: https://pypi.org/project/docgen-cli/\n"
        "📖 Installation: pip install docgen-cli\n\n"
        "Users can now install DocGen CLI with:\n"
        "[bold blue]pip install docgen-cli[/bold blue]",
        title="✅ Upload Complete"
    ))
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
