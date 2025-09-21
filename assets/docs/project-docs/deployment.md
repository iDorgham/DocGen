# DocGen CLI Production Deployment Guide

This guide provides comprehensive instructions for deploying DocGen CLI to production environments.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Package Distribution](#package-distribution)
- [Docker Deployment](#docker-deployment)
- [CI/CD Pipeline](#cicd-pipeline)
- [Monitoring and Health Checks](#monitoring-and-health-checks)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)

## Overview

DocGen CLI is a production-ready Python CLI tool that can be deployed in multiple ways:

- **PyPI Package**: Installable via pip for end users
- **Docker Container**: Containerized deployment for consistent environments
- **CI/CD Pipeline**: Automated testing, building, and deployment
- **Monitoring**: Production monitoring and health checks

## Prerequisites

### System Requirements

- Python 3.8 or higher
- Docker (for containerized deployment)
- Git (for CI/CD pipeline)
- PyPI account (for package distribution)

### Development Tools

```bash
# Install development dependencies
pip install -e .[dev]

# Install build tools
pip install build twine
```

## Package Distribution

### Building the Package

```bash
# Clean previous builds
rm -rf dist/ build/

# Build the package
python -m build

# Check the package
twine check dist/*
```

### Publishing to PyPI

#### TestPyPI (Recommended for testing)

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ docgen-cli
```

#### Production PyPI

```bash
# Upload to production PyPI
twine upload dist/*
```

### Package Installation

```bash
# Install from PyPI
pip install docgen-cli

# Verify installation
docgen --version
```

## Docker Deployment

### Building Docker Images

#### Development Image

```bash
# Build development image
docker build -t docgen-cli:dev -f Dockerfile .

# Run development container
docker run --rm docgen-cli:dev --help
```

#### Production Image

```bash
# Build production image
docker build -t docgen-cli:prod -f Dockerfile.prod .

# Run production container
docker run --rm docgen-cli:prod --help
```

### Docker Compose

```bash
# Development environment
docker-compose --profile dev up

# Production environment
docker-compose --profile prod up

# Testing environment
docker-compose --profile test up
```

### Docker Hub Deployment

```bash
# Tag for Docker Hub
docker tag docgen-cli:prod username/docgen-cli:latest
docker tag docgen-cli:prod username/docgen-cli:v1.0.0

# Push to Docker Hub
docker push username/docgen-cli:latest
docker push username/docgen-cli:v1.0.0
```

## CI/CD Pipeline

### GitHub Actions Setup

The project includes comprehensive GitHub Actions workflows:

- **CI Pipeline** (`.github/workflows/ci.yml`): Automated testing, linting, security scans, and building
- **Release Pipeline** (`.github/workflows/release.yml`): Automated releases and PyPI publishing

### Required Secrets

Configure the following secrets in your GitHub repository:

- `PYPI_API_TOKEN`: PyPI API token for package publishing
- `DOCKER_USERNAME`: Docker Hub username
- `DOCKER_PASSWORD`: Docker Hub password

### Pipeline Features

- **Multi-Python Testing**: Tests on Python 3.8-3.13
- **Code Quality**: Black, isort, flake8, mypy
- **Security Scanning**: Safety and Bandit
- **Package Building**: Automated package and Docker image building
- **Automated Publishing**: PyPI and Docker Hub publishing on releases

## Monitoring and Health Checks

### Health Check Script

```bash
# Run health check
python scripts/health_check.py

# Health check returns:
# - 0 exit code for healthy
# - 1 exit code for unhealthy
```

### Production Monitoring

```bash
# Run continuous monitoring
python scripts/monitor.py

# Run single monitoring cycle
python scripts/monitor.py --once

# Custom monitoring interval
python scripts/monitor.py --interval 30
```

### Monitoring Features

- **CLI Health**: Version check and response time monitoring
- **Dependencies**: Module availability verification
- **File System**: Required paths and permissions check
- **System Resources**: CPU, memory, and disk usage monitoring
- **Alerting**: Webhook notifications for critical issues

### Docker Health Checks

The Docker images include built-in health checks:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD docgen --version || exit 1
```

## Security Considerations

### Package Security

- **Dependency Scanning**: Automated security scanning with Safety
- **Code Analysis**: Security analysis with Bandit
- **Minimal Dependencies**: Only essential dependencies included
- **Non-root User**: Docker containers run as non-root user

### Runtime Security

- **Input Validation**: Comprehensive input validation and sanitization
- **Error Handling**: Secure error messages without sensitive information
- **File Permissions**: Proper file system permissions
- **Environment Variables**: Secure handling of configuration

### Deployment Security

- **HTTPS Only**: All external communications use HTTPS
- **Secret Management**: Secure handling of API keys and tokens
- **Access Control**: Proper access controls for deployment environments
- **Audit Logging**: Comprehensive logging for security auditing

## Deployment Scripts

### Automated Deployment

```bash
# Full deployment (dry run)
python scripts/deploy.py

# Full deployment with publishing
python scripts/deploy.py --publish

# Skip certain steps
python scripts/deploy.py --skip-tests --skip-docker

# Publish to TestPyPI
python scripts/deploy.py --testpypi
```

### Deployment Features

- **Prerequisites Check**: Validates system requirements
- **Automated Testing**: Runs full test suite
- **Code Quality**: Performs linting and formatting checks
- **Package Building**: Builds and validates packages
- **Docker Building**: Creates Docker images
- **Publishing**: Publishes to PyPI and Docker Hub

## Environment Configuration

### Environment Variables

```bash
# Development
export DOCGEN_ENV=development
export DOCGEN_DEBUG=true

# Production
export DOCGEN_ENV=production
export DOCGEN_DEBUG=false
export DOCGEN_LOG_LEVEL=INFO
```

### Configuration Files

- `pyproject.toml`: Package configuration and dependencies
- `docker-compose.yml`: Docker deployment configuration
- `.github/workflows/`: CI/CD pipeline configuration
- `scripts/`: Deployment and monitoring scripts

## Performance Optimization

### Package Optimization

- **Minimal Dependencies**: Only essential dependencies included
- **Optimized Imports**: Lazy loading of heavy modules
- **Caching**: Template and configuration caching
- **Compression**: Optimized package size

### Runtime Optimization

- **Memory Management**: Efficient memory usage
- **Response Time**: Sub-2-second response times
- **Concurrent Processing**: Multi-threaded operations where appropriate
- **Resource Monitoring**: Continuous performance monitoring

## Troubleshooting

### Common Issues

#### Package Installation Issues

```bash
# Clear pip cache
pip cache purge

# Reinstall with verbose output
pip install -v docgen-cli

# Check Python version compatibility
python --version
```

#### Docker Issues

```bash
# Check Docker daemon
docker info

# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -t docgen-cli:prod -f Dockerfile.prod .
```

#### CI/CD Issues

- Check GitHub Actions logs for detailed error messages
- Verify all required secrets are configured
- Ensure branch protection rules allow automated deployments
- Check PyPI and Docker Hub API token permissions

### Health Check Failures

```bash
# Run detailed health check
python scripts/health_check.py

# Check specific components
python -c "import src.cli_main; print('CLI import successful')"
python -c "import jinja2; print('Jinja2 available')"
```

### Performance Issues

```bash
# Monitor system resources
python scripts/monitor.py --once

# Check response times
time docgen --version

# Profile memory usage
python -m memory_profiler scripts/health_check.py
```

## Support and Maintenance

### Regular Maintenance

- **Dependency Updates**: Regular updates of dependencies
- **Security Patches**: Apply security updates promptly
- **Performance Monitoring**: Continuous performance monitoring
- **Log Rotation**: Regular log file cleanup

### Monitoring Alerts

Configure alerts for:
- CLI health check failures
- Performance degradation
- High resource usage
- Dependency issues
- File system problems

### Backup and Recovery

- **Configuration Backup**: Regular backup of configuration files
- **Docker Image Backup**: Backup of production Docker images
- **Package Backup**: Backup of PyPI packages
- **Documentation Backup**: Regular backup of documentation

## Conclusion

This deployment guide provides comprehensive instructions for deploying DocGen CLI to production environments. Follow the security considerations and monitoring recommendations to ensure a robust and secure deployment.

For additional support, refer to the project documentation or create an issue in the project repository.
