Developer Guide
===============

This guide provides detailed information for developers working on the Mindmap India project, including architecture, code organization, and development workflows.

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2

   Architecture <#architecture>
   Project Structure <#project-structure>
   Development Workflow <#development-workflow>
   Testing <#testing>
   Code Style <#code-style>
   Documentation <#documentation>
   Deployment <#deployment>

Architecture
------------

Mindmap India follows a client-server architecture with the following components:

### Frontend

- **Framework**: Streamlit
- **Key Libraries**:
  - Streamlit for UI components
  - Plotly for interactive visualizations
  - Custom CSS for styling

### Backend

- **Language**: Python 3.8+
- **Machine Learning**:
  - scikit-learn for clustering and similarity analysis
  - NLTK for text processing
  - joblib for model persistence

### Data Layer

- **Data Storage**: CSV files (for now)
- **Data Processing**: pandas, numpy

### Caching

- **Purpose**: Improve performance by caching expensive computations
- **Implementation**: Streamlit's caching decorators and joblib.Memory

Project Structure
----------------

```
mindmap-india/
├── app/                      # Main application package
│   ├── __init__.py          # Package initialization
│   ├── app.py               # Streamlit application
│   ├── cluster_utils.py     # ML utilities for career clustering
│   └── assets/              # Static assets (CSS, images)
├── data/                    # Data files
│   └── careers.csv          # Career dataset
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── conftest.py          # Test fixtures and configuration
│   └── test_*.py            # Test modules
├── notebooks/               # Jupyter notebooks for analysis
│   ├── career_analysis.ipynb
│   ├── clustering_new.py
│   └── requirements.txt     # Notebook-specific dependencies
├── output/                  # Generated outputs
│   └── wordclouds/          # Generated word clouds
├── scripts/                 # Utility scripts
│   ├── career_clustering.py
│   └── career_clustering_fixed.py
├── .gitignore
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── LICENSE
├── pytest.ini
├── README.md
├── requirements.txt
├── requirements-dev.txt
└── setup_dev.py
```

Development Workflow
-------------------

### Setting Up the Development Environment

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/mindmap-india.git
   cd mindmap-india
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Set up pre-commit hooks**
   ```bash
   pre-commit install
   ```

### Making Changes

1. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the code style guidelines
   - Write tests for new functionality
   - Update documentation as needed

3. **Run tests**
   ```bash
   pytest
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Your detailed commit message"
   git push origin your-branch-name
   ```

5. **Open a pull request**
   - Go to the repository on GitHub
   - Click "New Pull Request"
   - Follow the PR template
   - Request reviews from team members

Testing
-------

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

### Writing Tests

- Place test files in the `tests/` directory
- Name test files with the prefix `test_`
- Use descriptive test function names starting with `test_`
- Use pytest fixtures for test data and setup/teardown
- Aim for high test coverage, especially for critical paths

Code Style
----------

We use several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Static type checking

Run these tools before committing:

```bash
black .
isort .
flake8 .
mypy .
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

### API Documentation

- Document all public APIs
- Include examples of usage
- Document any changes that might affect existing integrations

Deployment
----------

### Local Development

```bash
streamlit run app/app.py
```

### Production Deployment

1. **Build the Docker image**
   ```bash
   docker build -t mindmap-india .
   ```

2. **Run the container**
   ```bash
   docker run -p 8501:8501 mindmap-india
   ```

3. **Access the application**
   Open your browser to `http://localhost:8501`

### CI/CD

We use GitHub Actions for continuous integration and deployment. The workflow includes:

- Running tests on all pushes and pull requests
- Building and pushing Docker images on version tags
- Deploying to staging/production environments

Troubleshooting
--------------

### Common Issues

- **Import errors**: Make sure your virtual environment is activated and all dependencies are installed
- **Test failures**: Run tests with `-v` for more detailed output
- **Performance issues**: Check for unoptimized queries or computations

### Getting Help

- Check the project's GitHub issues
- Ask for help in the project's discussion forum
- Contact the maintainers if needed

Contributing
------------

We welcome contributions! Please see our :doc:`contributing` guide for more information on how to get involved.
