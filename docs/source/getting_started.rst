Getting Started
===============

This guide will help you get started with Mindmap India, whether you're a user looking to explore career options or a developer looking to contribute to the project.

For Users
---------

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/mindmap-india.git
   cd mindmap-india
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   # Windows
   .\run_analysis.bat
   
   # Or directly with Python
   streamlit run run.py
   ```

5. **Access the application**
   Open your web browser and go to `http://localhost:8501`

For Developers
--------------

### Additional Prerequisites

- Git
- (Optional) A code editor like VS Code, PyCharm, etc.

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/mindmap-india.git
   cd mindmap-india
   ```

2. **Set up a virtual environment** (if not already done)
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install development dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Set up pre-commit hooks**
   ```bash
   pre-commit install
   ```

5. **Run tests**
   ```bash
   pytest
   ```

### Running the Development Server

To run the application in development mode:

```bash
# Start the Streamlit app with auto-reload
streamlit run app/app.py
```

### Building Documentation

To build the documentation locally:

```bash
cd docs
make html  # Requires make and sphinx to be installed
# The built documentation will be in docs/_build/html
```

Next Steps
----------

- Read the :doc:`user_guide` to learn how to use Mindmap India
- Check out the :doc:`developer_guide` for information on the codebase
- Learn how to :doc:`contributing` to the project
