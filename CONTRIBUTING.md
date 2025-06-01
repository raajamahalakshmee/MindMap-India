# Contributing to Mindmap India

Thank you for your interest in contributing to Mindmap India! We welcome contributions from everyone, whether you're a developer, designer, data scientist, or just someone who wants to help improve the project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Setting Up the Development Environment](#setting-up-the-development-environment)
- [Making Changes](#making-changes)
  - [Code Style](#code-style)
  - [Testing](#testing)
  - [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Feature Requests](#feature-requests)
- [Code Review Process](#code-review-process)
- [Community](#community)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [your-email@example.com].

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- pip (Python package manager)
- (Optional) A virtual environment (venv, conda, etc.)

### Setting Up the Development Environment

1. **Fork the repository**
   
   Click the "Fork" button in the top-right corner of the [repository page](https://github.com/yourusername/mindmap-india).

2. **Clone your fork**
   ```bash
   git clone https://github.com/your-username/mindmap-india.git
   cd mindmap-india
   ```

3. **Set up a virtual environment** (recommended)
   ```bash
   # Using venv (built into Python)
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   # Install core requirements
   pip install -r requirements.txt
   
   # Install development dependencies
   pip install -r requirements-dev.txt
   
   # Install pre-commit hooks
   pre-commit install
   ```

5. **Verify your setup**
   ```bash
   # Run tests to verify everything is working
   pytest
   ```

## Making Changes

1. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b bugfix/issue-number-description
   ```

### Code Style

We use several tools to maintain code quality and style:

- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

These are automatically checked when you commit changes if you've set up pre-commit hooks.

To manually run all code style checks:

```bash
black .
isort .
flake8 .
mypy .
```

### Testing

We use pytest for testing. Please add tests for any new functionality or bug fixes.

To run all tests:
```bash
pytest
```

To run tests with coverage:
```bash
pytest --cov=app --cov-report=html
```

### Documentation

We use Sphinx for documentation. When adding new features, please update the relevant documentation.

To build the documentation locally:
```bash
cd docs
make html
```

## Submitting Changes

1. **Commit your changes**
   ```bash
   git add .
   git commit -m "Your detailed description of changes"
   ```

2. **Push to your fork**
   ```bash
   git push origin your-branch-name
   ```

3. **Create a Pull Request**
   - Go to the [repository page](https://github.com/yourusername/mindmap-india)
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill out the PR template with details about your changes
   - Submit the PR

## Reporting Bugs

If you find a bug, please open an issue with:

1. A clear, descriptive title
2. Steps to reproduce the issue
3. Expected vs. actual behavior
4. Any relevant error messages
5. Your environment (OS, Python version, etc.)

## Feature Requests

We welcome feature requests! Please open an issue with:

1. A clear, descriptive title
2. A detailed description of the feature
3. Any relevant use cases or examples
4. Any potential implementation ideas (optional)

## Code Review Process

1. A maintainer will review your PR as soon as possible
2. We may request changes or ask for clarification
3. Once approved, a maintainer will merge your PR
4. Your contribution will be included in the next release

## Community

- Join our [Discord/Slack channel] (if applicable)
- Follow us on [Twitter] (if applicable)
- Check out our [blog] (if applicable)

Thank you for contributing to Mindmap India! 🚀
