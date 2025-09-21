# 🚀 PyPI Upload Guide for DocGen CLI

This guide will walk you through uploading DocGen CLI to PyPI for public distribution.

## 📋 Prerequisites

### 1. PyPI Account Setup

#### Create PyPI Account
1. Visit [https://pypi.org/account/register/](https://pypi.org/account/register/)
2. Create an account with your email
3. Verify your email address

#### Create Test PyPI Account (Recommended)
1. Visit [https://test.pypi.org/account/register/](https://test.pypi.org/account/register/)
2. Create a separate account for testing
3. Verify your email address

### 2. API Token Setup (Recommended)

#### Generate API Token
1. Go to [https://pypi.org/manage/account/](https://pypi.org/manage/account/)
2. Scroll to "API tokens" section
3. Click "Add API token"
4. Give it a name (e.g., "DocGen CLI Upload")
5. Set scope to "Entire account" or specific project
6. Copy the token (starts with `pypi-`)

#### Configure Credentials
Create `~/.pypirc` file:
```ini
[distutils]
index-servers = pypi testpypi

[pypi]
username = __token__
password = pypi-your-api-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-test-api-token-here
```

### 3. Environment Setup

#### Activate Virtual Environment
```bash
# Activate your virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
```

#### Install Required Tools
```bash
pip install build twine
```

## 🔧 Upload Process

### Method 1: Automated Script (Recommended)

Run the automated upload script:
```bash
python upload_to_pypi.py
```

The script will:
1. ✅ Check prerequisites
2. 🧹 Clean build artifacts
3. 🔨 Build the package
4. 🔍 Validate the package
5. 📤 Upload to Test PyPI (optional)
6. 📤 Upload to Production PyPI
7. 🔍 Verify the upload

### Method 2: Manual Process

#### Step 1: Clean Previous Builds
```bash
rm -rf dist/ build/ *.egg-info/
```

#### Step 2: Build Package
```bash
python -m build
```

#### Step 3: Validate Package
```bash
twine check dist/*
```

#### Step 4: Upload to Test PyPI (Recommended)
```bash
twine upload --repository testpypi dist/*
```

#### Step 5: Test Installation from Test PyPI
```bash
pip install --index-url https://test.pypi.org/simple/ docgen-cli
```

#### Step 6: Upload to Production PyPI
```bash
twine upload dist/*
```

## 📦 Package Information

### Current Package Details
- **Name**: `docgen-cli`
- **Version**: `1.0.0`
- **Description**: A powerful CLI tool for generating project documentation from specifications using spec-driven development principles
- **Author**: DocGen Team
- **License**: MIT
- **Python Versions**: 3.8+

### Package Contents
- Source code in `src/` directory
- CLI entry point: `docgen`
- Dependencies: click, jinja2, pyyaml, rich, pydantic, etc.
- Documentation: README.md, CHANGELOG.md

## 🔍 Verification

### After Upload, Verify:

1. **Package Installation**:
   ```bash
   pip install docgen-cli
   ```

2. **CLI Functionality**:
   ```bash
   docgen --version
   docgen --help
   ```

3. **PyPI Page**:
   Visit: https://pypi.org/project/docgen-cli/

## 🚨 Troubleshooting

### Common Issues

#### 1. Authentication Errors
```
HTTPError: 403 Client Error: Invalid or non-existent authentication information
```
**Solution**: Check your API token in `~/.pypirc`

#### 2. Package Already Exists
```
HTTPError: 400 Client Error: File already exists
```
**Solution**: Increment version in `pyproject.toml`

#### 3. Build Errors
```
error: invalid command 'bdist_wheel'
```
**Solution**: Install wheel: `pip install wheel`

#### 4. Import Errors
```
ModuleNotFoundError: No module named 'src'
```
**Solution**: Check package structure in `pyproject.toml`

### Getting Help

1. **PyPI Documentation**: https://packaging.python.org/
2. **Twine Documentation**: https://twine.readthedocs.io/
3. **Build Documentation**: https://pypa-build.readthedocs.io/

## 📈 Post-Upload Tasks

### 1. Update Documentation
- Update README.md with PyPI installation instructions
- Update any documentation that references installation methods

### 2. Announce Release
- Create GitHub release
- Update project website
- Announce on social media/community channels

### 3. Monitor
- Monitor PyPI download statistics
- Watch for user feedback and issues
- Track package health metrics

## 🔄 Future Updates

### Version Management
1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Build and upload new version
4. Create GitHub release

### Automated Uploads
Consider setting up GitHub Actions for automated uploads:
```yaml
name: Upload to PyPI
on:
  release:
    types: [published]
jobs:
  upload:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

## ✅ Success Checklist

- [ ] PyPI account created and verified
- [ ] API token configured
- [ ] Virtual environment activated
- [ ] Build tools installed
- [ ] Package built successfully
- [ ] Package validated
- [ ] Uploaded to Test PyPI (optional)
- [ ] Tested installation from Test PyPI
- [ ] Uploaded to Production PyPI
- [ ] Verified installation from PyPI
- [ ] Updated documentation
- [ ] Announced release

## 🎉 Congratulations!

Once uploaded, users can install DocGen CLI with:
```bash
pip install docgen-cli
```

Your package will be available at: https://pypi.org/project/docgen-cli/
