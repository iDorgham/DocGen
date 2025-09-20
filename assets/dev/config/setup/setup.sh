#!/bin/bash
# DocGen CLI Configuration Setup Script
# Sets up development environment and validates configuration

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CONFIG_DIR="$PROJECT_ROOT/assets/config"
VENV_DIR="$PROJECT_ROOT/venv"
REQUIREMENTS_FILE="$PROJECT_ROOT/requirements.txt"

echo -e "${BLUE}🚀 DocGen CLI Configuration Setup${NC}"
echo "=================================="
echo "Project Root: $PROJECT_ROOT"
echo "Config Directory: $CONFIG_DIR"
echo ""

# Function to print status
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "$PROJECT_ROOT/pyproject.toml" ]; then
    print_error "pyproject.toml not found. Please run this script from the DocGen project root."
    exit 1
fi

# Check Python version
echo -e "${BLUE}🐍 Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
required_version="3.8"

if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    print_status "Python $python_version is compatible (>= $required_version)"
else
    print_error "Python $required_version or higher is required. Found: $python_version"
    exit 1
fi

# Create virtual environment if it doesn't exist
echo -e "${BLUE}📦 Setting up virtual environment...${NC}"
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    print_status "Virtual environment created at $VENV_DIR"
else
    print_status "Virtual environment already exists at $VENV_DIR"
fi

# Activate virtual environment
echo -e "${BLUE}🔧 Activating virtual environment...${NC}"
source "$VENV_DIR/bin/activate"
print_status "Virtual environment activated"

# Upgrade pip
echo -e "${BLUE}⬆️  Upgrading pip...${NC}"
pip install --upgrade pip
print_status "pip upgraded to latest version"

# Install dependencies
echo -e "${BLUE}📚 Installing dependencies...${NC}"
if [ -f "$REQUIREMENTS_FILE" ]; then
    pip install -r "$REQUIREMENTS_FILE"
    print_status "Dependencies installed from requirements.txt"
else
    print_warning "requirements.txt not found, installing from pyproject.toml"
    pip install -e .
fi

# Install development dependencies
echo -e "${BLUE}🛠️  Installing development dependencies...${NC}"
pip install pytest pytest-cov black isort flake8 mypy bandit safety
print_status "Development dependencies installed"

# Install in development mode
echo -e "${BLUE}🔧 Installing DocGen CLI in development mode...${NC}"
pip install -e .
print_status "DocGen CLI installed in development mode"

# Validate configuration files
echo -e "${BLUE}🔍 Validating configuration files...${NC}"
if [ -f "$CONFIG_DIR/validation.py" ]; then
    python "$CONFIG_DIR/validation.py" --config-dir "$CONFIG_DIR"
    if [ $? -eq 0 ]; then
        print_status "Configuration validation passed"
    else
        print_warning "Configuration validation found issues (see report above)"
    fi
else
    print_warning "Configuration validation script not found"
fi

# Run initial tests
echo -e "${BLUE}🧪 Running initial tests...${NC}"
if [ -d "$PROJECT_ROOT/tests" ] || [ -d "$PROJECT_ROOT/assets/dev/tests" ]; then
    # Find test directory
    if [ -d "$PROJECT_ROOT/tests" ]; then
        TEST_DIR="$PROJECT_ROOT/tests"
    else
        TEST_DIR="$PROJECT_ROOT/assets/dev/tests"
    fi
    
    # Run tests with coverage
    python -m pytest "$TEST_DIR" -v --cov=src --cov-report=term-missing --maxfail=3
    if [ $? -eq 0 ]; then
        print_status "Initial tests passed"
    else
        print_warning "Some tests failed (this is normal for initial setup)"
    fi
else
    print_warning "No test directory found"
fi

# Check code quality
echo -e "${BLUE}🔍 Running code quality checks...${NC}"

# Format check
echo "Checking code formatting..."
if black --check src/ 2>/dev/null; then
    print_status "Code formatting is correct"
else
    print_warning "Code formatting issues found (run 'black src/' to fix)"
fi

# Import sorting check
echo "Checking import sorting..."
if isort --check-only src/ 2>/dev/null; then
    print_status "Import sorting is correct"
else
    print_warning "Import sorting issues found (run 'isort src/' to fix)"
fi

# Linting check
echo "Checking code linting..."
if flake8 src/ 2>/dev/null; then
    print_status "Code linting passed"
else
    print_warning "Code linting issues found (see output above)"
fi

# Type checking
echo "Checking type hints..."
if mypy src/ 2>/dev/null; then
    print_status "Type checking passed"
else
    print_warning "Type checking issues found (see output above)"
fi

# Security check
echo "Checking security vulnerabilities..."
if bandit -r src/ 2>/dev/null; then
    print_status "Security check passed"
else
    print_warning "Security issues found (see output above)"
fi

# Dependency security check
echo "Checking dependency vulnerabilities..."
if safety check 2>/dev/null; then
    print_status "Dependency security check passed"
else
    print_warning "Dependency vulnerabilities found (see output above)"
fi

# Create useful aliases and scripts
echo -e "${BLUE}📝 Creating development scripts...${NC}"

# Create development script
cat > "$PROJECT_ROOT/dev.sh" << 'EOF'
#!/bin/bash
# Development helper script

# Activate virtual environment
source venv/bin/activate

# Set environment variables
export DOCGEN_TEST_MODE=true
export DOCGEN_LOG_LEVEL=DEBUG

# Run development commands
case "$1" in
    "test")
        pytest tests/ -v --cov=src --cov-report=html
        ;;
    "test-fast")
        pytest tests/ -v -m "not slow"
        ;;
    "format")
        black src/ tests/
        isort src/ tests/
        ;;
    "lint")
        flake8 src/ tests/
        mypy src/
        ;;
    "quality")
        black --check src/ tests/
        isort --check-only src/ tests/
        flake8 src/ tests/
        mypy src/
        bandit -r src/
        safety check
        ;;
    "install")
        pip install -e .
        ;;
    "clean")
        find . -type f -name "*.pyc" -delete
        find . -type d -name "__pycache__" -delete
        find . -type d -name "*.egg-info" -exec rm -rf {} +
        rm -rf build/ dist/ .coverage htmlcov/
        ;;
    *)
        echo "Usage: $0 {test|test-fast|format|lint|quality|install|clean}"
        echo ""
        echo "Commands:"
        echo "  test        Run all tests with coverage"
        echo "  test-fast   Run fast tests only"
        echo "  format      Format code with black and isort"
        echo "  lint        Run linting and type checking"
        echo "  quality     Run all quality checks"
        echo "  install     Install in development mode"
        echo "  clean       Clean build artifacts"
        ;;
esac
EOF

chmod +x "$PROJECT_ROOT/dev.sh"
print_status "Development script created: dev.sh"

# Create pre-commit hook
echo -e "${BLUE}🪝 Setting up pre-commit hooks...${NC}"
mkdir -p "$PROJECT_ROOT/.git/hooks"

cat > "$PROJECT_ROOT/.git/hooks/pre-commit" << 'EOF'
#!/bin/bash
# Pre-commit hook for DocGen CLI

echo "🔍 Running pre-commit checks..."

# Activate virtual environment
source venv/bin/activate

# Run code quality checks
echo "Checking code formatting..."
black --check src/ tests/ || {
    echo "❌ Code formatting issues found. Run 'black src/ tests/' to fix."
    exit 1
}

echo "Checking import sorting..."
isort --check-only src/ tests/ || {
    echo "❌ Import sorting issues found. Run 'isort src/ tests/' to fix."
    exit 1
}

echo "Checking linting..."
flake8 src/ tests/ || {
    echo "❌ Linting issues found."
    exit 1
}

echo "Checking type hints..."
mypy src/ || {
    echo "❌ Type checking issues found."
    exit 1
}

echo "Running tests..."
pytest tests/ -x --maxfail=1 || {
    echo "❌ Tests failed."
    exit 1
}

echo "✅ Pre-commit checks passed!"
EOF

chmod +x "$PROJECT_ROOT/.git/hooks/pre-commit"
print_status "Pre-commit hook installed"

# Create .env.example if it doesn't exist
if [ ! -f "$PROJECT_ROOT/.env.example" ]; then
    echo -e "${BLUE}📄 Creating .env.example...${NC}"
    cat > "$PROJECT_ROOT/.env.example" << 'EOF'
# DocGen CLI Environment Configuration

# Logging
DOCGEN_LOG_LEVEL=INFO
DOCGEN_LOG_FILE=logs/docgen.log

# Output
DOCGEN_OUTPUT_DIR=./output
DOCGEN_TEMPLATE_DIR=./templates

# Development
DOCGEN_TEST_MODE=false
DOCGEN_DEBUG_MODE=false

# MCP Integration
BYTEROVER_ENABLED=true
TESTSPRITE_ENABLED=true
CONTEXT7_ENABLED=true
BROWSER_TOOLS_ENABLED=true
EOF
    print_status ".env.example created"
fi

# Create logs directory
mkdir -p "$PROJECT_ROOT/logs"
print_status "Logs directory created"

# Final summary
echo ""
echo -e "${GREEN}🎉 DocGen CLI Configuration Setup Complete!${NC}"
echo "=============================================="
echo ""
echo -e "${BLUE}📋 Next Steps:${NC}"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run tests: ./dev.sh test"
echo "3. Format code: ./dev.sh format"
echo "4. Check quality: ./dev.sh quality"
echo "5. Start development: docgen --help"
echo ""
echo -e "${BLUE}🛠️  Development Commands:${NC}"
echo "• ./dev.sh test        - Run all tests"
echo "• ./dev.sh format      - Format code"
echo "• ./dev.sh lint        - Run linting"
echo "• ./dev.sh quality     - Run all quality checks"
echo "• ./dev.sh clean       - Clean build artifacts"
echo ""
echo -e "${BLUE}📚 Configuration Files:${NC}"
echo "• assets/config/development.yaml"
echo "• assets/config/testing.yaml"
echo "• assets/config/quality.yaml"
echo "• assets/config/deployment.yaml"
echo "• assets/config/workflow.yaml"
echo ""
echo -e "${GREEN}✅ Setup complete! Happy coding! 🚀${NC}"
