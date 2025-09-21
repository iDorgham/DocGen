# DocGen CLI Installation Guide

## System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+, CentOS 7+)
- **Memory**: 512 MB RAM
- **Disk Space**: 100 MB free space

### Recommended Requirements
- **Python**: 3.11 or higher
- **Memory**: 1 GB RAM
- **Disk Space**: 500 MB free space

## Installation Methods

### Method 1: Install from PyPI (Recommended)

This is the easiest and most reliable installation method.

```bash
pip install docgen-cli
```

#### Verify Installation
```bash
docgen --version
```

Expected output:
```
DocGen CLI 1.0.0
```

### Method 2: Install from Source

If you want the latest development version or need to modify the source code:

#### Prerequisites
- Git
- Python 3.8+
- pip

#### Installation Steps
```bash
# Clone the repository
git clone https://github.com/docgen-cli/docgen-cli.git
cd docgen-cli

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev,test]"
```

#### Verify Installation
```bash
docgen --version
```

### Method 3: Using Conda

If you prefer using Conda:

```bash
# Create a new environment
conda create -n docgen python=3.11

# Activate the environment
conda activate docgen

# Install DocGen CLI
pip install docgen-cli
```

### Method 4: Using Docker

For containerized environments:

```bash
# Pull the official image
docker pull docgen-cli:latest

# Run DocGen CLI
docker run -it --rm -v $(pwd):/workspace docgen-cli:latest
```

## Platform-Specific Instructions

### Windows

#### Using pip (Recommended)
```cmd
# Open Command Prompt or PowerShell
pip install docgen-cli

# Verify installation
docgen --version
```

#### Using Chocolatey
```cmd
# Install Chocolatey if not already installed
# Then install DocGen CLI
choco install docgen-cli
```

#### Using Scoop
```cmd
# Install Scoop if not already installed
# Then install DocGen CLI
scoop install docgen-cli
```

### macOS

#### Using pip (Recommended)
```bash
# Install using pip
pip3 install docgen-cli

# Verify installation
docgen --version
```

#### Using Homebrew
```bash
# Install Homebrew if not already installed
# Then install DocGen CLI
brew install docgen-cli
```

#### Using MacPorts
```bash
# Install MacPorts if not already installed
# Then install DocGen CLI
sudo port install docgen-cli
```

### Linux

#### Ubuntu/Debian
```bash
# Update package list
sudo apt update

# Install Python and pip if not already installed
sudo apt install python3 python3-pip

# Install DocGen CLI
pip3 install docgen-cli

# Verify installation
docgen --version
```

#### CentOS/RHEL/Fedora
```bash
# Install Python and pip if not already installed
sudo yum install python3 python3-pip  # CentOS/RHEL
# or
sudo dnf install python3 python3-pip  # Fedora

# Install DocGen CLI
pip3 install docgen-cli

# Verify installation
docgen --version
```

#### Arch Linux
```bash
# Install using pacman
sudo pacman -S python-pip

# Install DocGen CLI
pip install docgen-cli

# Verify installation
docgen --version
```

## Virtual Environment Setup (Recommended)

Using a virtual environment is highly recommended to avoid conflicts with system packages.

### Create Virtual Environment
```bash
# Create virtual environment
python -m venv docgen-env

# Activate virtual environment
# On Windows:
docgen-env\Scripts\activate

# On macOS/Linux:
source docgen-env/bin/activate
```

### Install DocGen CLI
```bash
pip install docgen-cli
```

### Deactivate Virtual Environment
```bash
deactivate
```

## Dependencies

DocGen CLI has the following dependencies:

### Core Dependencies
- `click>=8.0.0` - Command-line interface framework
- `jinja2>=3.0.0` - Template engine
- `pyyaml>=6.0` - YAML file processing
- `rich>=13.0.0` - Rich text and beautiful formatting
- `pydantic>=2.0.0` - Data validation
- `email-validator>=2.0.0` - Email validation
- `requests>=2.28.0` - HTTP library
- `semantic-version>=2.10.0` - Version handling
- `markdown>=3.4.0` - Markdown processing
- `pdfkit>=1.0.0` - PDF generation
- `numpy>=1.24.0` - Numerical computing
- `scikit-learn>=1.3.0` - Machine learning
- `joblib>=1.3.0` - Parallel processing
- `watchdog>=6.0.0` - File system monitoring

### Optional Dependencies

#### Development Dependencies
```bash
pip install docgen-cli[dev]
```

Includes:
- `pytest>=7.0.0` - Testing framework
- `pytest-cov>=4.0.0` - Coverage testing
- `black>=23.0.0` - Code formatting
- `isort>=5.0.0` - Import sorting
- `flake8>=6.0.0` - Linting
- `mypy>=1.0.0` - Type checking

#### Testing Dependencies
```bash
pip install docgen-cli[test]
```

#### Documentation Dependencies
```bash
pip install docgen-cli[docs]
```

#### Performance Dependencies
```bash
pip install docgen-cli[performance]
```

## Troubleshooting Installation

### Common Issues

#### "command not found: docgen"
**Cause:** DocGen CLI is not in your PATH.

**Solutions:**
1. **Check installation:**
   ```bash
   pip show docgen-cli
   ```

2. **Reinstall with user flag:**
   ```bash
   pip install --user docgen-cli
   ```

3. **Add to PATH manually:**
   ```bash
   # Find the installation directory
   python -m site --user-base
   
   # Add to PATH (Linux/macOS)
   export PATH="$PATH:$(python -m site --user-base)/bin"
   
   # Add to PATH (Windows)
   # Add the Scripts directory to your PATH environment variable
   ```

#### "Permission denied" errors
**Cause:** Insufficient permissions to install packages.

**Solutions:**
1. **Use virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install docgen-cli
   ```

2. **Install with user flag:**
   ```bash
   pip install --user docgen-cli
   ```

3. **Use sudo (Linux/macOS only):**
   ```bash
   sudo pip install docgen-cli
   ```

#### "No module named 'docgen'" errors
**Cause:** Installation failed or incomplete.

**Solutions:**
1. **Reinstall:**
   ```bash
   pip uninstall docgen-cli
   pip install docgen-cli
   ```

2. **Check Python version:**
   ```bash
   python --version
   # Should be 3.8 or higher
   ```

3. **Upgrade pip:**
   ```bash
   pip install --upgrade pip
   pip install docgen-cli
   ```

#### Import errors for dependencies
**Cause:** Missing or incompatible dependencies.

**Solutions:**
1. **Install all dependencies:**
   ```bash
   pip install docgen-cli[dev,test,docs,performance]
   ```

2. **Check for conflicts:**
   ```bash
   pip check
   ```

3. **Reinstall in clean environment:**
   ```bash
   python -m venv clean-env
   source clean-env/bin/activate
   pip install docgen-cli
   ```

### Platform-Specific Issues

#### Windows
- **Long path issues:** Enable long path support in Windows 10/11
- **Antivirus interference:** Add Python and pip directories to antivirus exclusions
- **PowerShell execution policy:** Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

#### macOS
- **Xcode command line tools:** Install with `xcode-select --install`
- **Homebrew conflicts:** Use virtual environments to avoid conflicts
- **Permission issues:** Use `pip install --user` or virtual environments

#### Linux
- **Missing system packages:** Install `python3-dev` and `build-essential`
- **pip not found:** Install with `sudo apt install python3-pip`
- **Permission issues:** Use virtual environments or `pip install --user`

## Uninstallation

### Remove DocGen CLI
```bash
pip uninstall docgen-cli
```

### Remove with dependencies
```bash
pip uninstall docgen-cli -y
```

### Clean up virtual environment
```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment directory
rm -rf docgen-env
```

## Upgrading

### Upgrade to latest version
```bash
pip install --upgrade docgen-cli
```

### Upgrade from source
```bash
cd docgen-cli
git pull origin main
pip install -e .
```

## Verification

After installation, verify that everything is working correctly:

```bash
# Check version
docgen --version

# Check help
docgen help

# Create a test project
docgen create test-project
cd test-project

# Generate test documentation
docgen spec
docgen plan
docgen marketing

# Validate project
docgen validate

# Clean up
cd ..
rm -rf test-project
```

## Getting Help

If you encounter issues during installation:

1. **Check the documentation:** [User Guide](USER_GUIDE.md)
2. **Search existing issues:** [GitHub Issues](https://github.com/docgen-cli/docgen-cli/issues)
3. **Create a new issue:** Include:
   - Operating system and version
   - Python version
   - Installation method used
   - Complete error message
   - Steps to reproduce

## Next Steps

After successful installation:

1. **Read the User Guide:** [USER_GUIDE.md](USER_GUIDE.md)
2. **Create your first project:** `docgen create my-project`
3. **Explore the features:** `docgen help`
4. **Join the community:** [GitHub Discussions](https://github.com/docgen-cli/docgen-cli/discussions)

---

Welcome to DocGen CLI! 🎉
