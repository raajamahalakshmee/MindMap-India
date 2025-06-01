Contributing to Mindmap India
============================

Thank you for your interest in contributing to Mindmap India! We welcome contributions from everyone, whether you're a developer, designer, data scientist, or just someone who wants to help improve the project.

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2

   Code of Conduct <#code-of-conduct>
   How Can I Contribute? <#how-can-i-contribute>
   Setting Up for Development <#setting-up-for-development>
   Development Workflow <#development-workflow>
   Code Style Guide <#code-style-guide>
   Testing <#testing>
   Documentation <#documentation>
   Submitting Changes <#submitting-changes>
   Code Review Process <#code-review-process>
   Community <#community>

Code of Conduct
---------------

This project and everyone participating in it is governed by our :doc:`Code of Conduct <code_of_conduct>`. By participating, you are expected to uphold this code. Please report unacceptable behavior to [your-email@example.com].

How Can I Contribute?
---------------------

### Reporting Bugs

Before creating a bug report, please check if the issue has already been reported. If it hasn't, you can create a new issue with the following information:

1. **Clear, descriptive title**
2. **Steps to reproduce** the issue
3. **Expected behavior**
4. **Actual behavior**
5. **Screenshots** (if applicable)
6. **Environment** (OS, browser, Python version, etc.)

### Suggesting Enhancements

We welcome suggestions for new features or improvements. When suggesting an enhancement, please include:

1. A clear, descriptive title
2. A detailed description of the enhancement
3. Why you think this would be valuable
4. Any examples or mockups (if applicable)

### Your First Code Contribution

If you're new to open source or the project, look for issues labeled "good first issue" or "help wanted". These are typically smaller, well-defined tasks that are good for newcomers.

### Improving Documentation

Good documentation is crucial for any project. You can help by:

- Fixing typos and grammatical errors
- Improving existing documentation
- Adding examples or clarifying complex concepts
- Translating documentation to other languages

Setting Up for Development
-------------------------

### Prerequisites

- Python 3.8 or higher
- Git
- pip (Python package manager)

### Fork and Clone the Repository

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/mindmap-india.git
   cd mindmap-india
   ```
3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/yourusername/mindmap-india.git
   ```

### Set Up a Virtual Environment

We recommend using a virtual environment to manage dependencies:

```bash
# Create a virtual environment
python -m venv .venv

# Activate it
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### Install Dependencies

```bash
# Install core requirements
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### Verify Your Setup

```bash
# Run tests to verify everything is working
pytest
```

Development Workflow
-------------------

1. **Sync your fork** with the latest changes from upstream:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create a new branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b bugfix/issue-number-description
   ```

3. **Make your changes** following the code style guide

4. **Run tests** to ensure nothing is broken:
   ```bash
   pytest
   ```

5. **Commit your changes** with a descriptive message:
   ```bash
   git add .
   git commit -m "Your detailed commit message"
   ```

6. **Push to your fork**:
   ```bash
   git push origin your-branch-name
   ```

7. **Open a Pull Request** from your fork to the upstream repository

Code Style Guide
----------------

### Python

We use several tools to maintain code quality:

- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for static type checking

Run these before committing:

```bash
black .
isort .
flake8 .
mypy .
```

### JavaScript/TypeScript

(If applicable to your project)

- Follow the Airbnb JavaScript Style Guide
- Use Prettier for code formatting
- Use ESLint for linting

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally
- Consider starting the commit message with an applicable emoji:
  - ✨ `:sparkles:` When adding a new feature
  - 🐛 `:bug:` When fixing a bug
  - ♻️ `:recycle:` When refactoring code
  - 📚 `:books:` When writing docs
  - 🚀 `:rocket:` When improving performance
  - 🚧 `:construction:` WIP (Work In Progress) commits
  - 🔧 `:wrench:` When updating configuration
  - ✅ `:white_check_mark:` When adding or updating tests

Testing
-------

### Writing Tests

- Write tests for all new functionality
- Follow the Arrange-Act-Assert pattern
- Name test files with the prefix `test_`
- Place test files in the `tests/` directory
- Use descriptive test function names starting with `test_`

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html

# Run a specific test file
pytest tests/test_clustering.py -v

# Run tests in parallel
pytest -n auto
```

### Test Coverage

We aim for high test coverage. Before submitting a PR, ensure your changes are well-tested.

To generate a coverage report:

```bash
pytest --cov=app --cov-report=html
# Open htmlcov/index.html in your browser
```

Documentation
-------------

### Code Documentation

- Use Google-style docstrings for all public functions and classes
- Include type hints for function parameters and return values
- Document complex algorithms and non-obvious code

### User Documentation

- Keep the user guide up to date with new features
- Add screenshots for UI changes
- Document any changes to the user interface

### Building Documentation

To build the documentation locally:

```bash
cd docs
make html  # Requires make and sphinx to be installed
# The built documentation will be in docs/_build/html
```

Submitting Changes
-----------------

1. **Ensure tests pass** on your local machine
2. **Update documentation** for any new features or changes
3. **Squash your commits** into logical units of work
4. **Push your changes** to your fork
5. **Open a Pull Request** with a clear description of your changes

### Pull Request Guidelines

- Fill out the PR template completely
- Reference any related issues
- Include screenshots or GIFs for UI changes
- Ensure all tests pass on the CI
- Get a code review from at least one maintainer

Code Review Process
------------------

1. A maintainer will review your PR as soon as possible
2. We may request changes or ask for clarification
3. Once approved, a maintainer will merge your PR
4. Your contribution will be included in the next release

### Review Guidelines

When reviewing PRs:

- Be kind and constructive
- Focus on the code, not the person
- Explain your reasoning for requested changes
- Suggest improvements rather than just pointing out problems
- Thank the contributor for their time and effort

Community
---------

### Getting Help

- **GitHub Issues**: For bug reports and feature requests
- **Discussion Forum**: For questions and discussions (if applicable)
- **Chat**: Join our [Discord/Slack channel] (if applicable)

### Staying Updated

- **Watch** the repository on GitHub to be notified of new issues and discussions
- Follow us on [Twitter] (if applicable)
- Check the [Changelog](CHANGELOG.md) for updates

### Recognition

All contributors are recognized in our [CONTRIBUTORS.md](CONTRIBUTORS.md) file. We appreciate every contribution, no matter how small!

### Becoming a Maintainer

Interested in becoming a maintainer? Here's how:

1. Make several high-quality contributions to the project
2. Help review pull requests and issues
3. Be active in the community
4. Express your interest to the current maintainers

Thank you for contributing to Mindmap India! Your help makes this project better for everyone. 🚀
