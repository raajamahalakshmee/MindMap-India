# 🇮🇳 Mindmap India: AI-Powered Career Explorer

**Mindmap India** is an interactive web application that helps students and professionals explore career options based on their interests using AI-powered clustering and similarity analysis. The application provides personalized career recommendations by analyzing skills, descriptions, and domains of various careers in the Indian context.

![Mindmap India Screenshot](https://via.placeholder.com/800x400?text=Mindmap+India+Screenshot)

---

## 🚀 Features

- 🧠 **AI-Powered Recommendations**: Get personalized career suggestions based on your interests
- 📊 **Comprehensive Career Database**: Explore detailed information about various careers
- 📈 **Interactive Visualizations**: View career distributions and relationships
- 💡 **Skill & Domain-Based Matching**: Find careers that match your skills and domain interests
- 🛠 **User-Friendly Interface**: Intuitive and responsive design for all devices
- ⚡ **Performance Optimized**: Caching and efficient data processing for fast recommendations
- 🔒 **Data Validation**: Robust error handling and data quality checks

---

## 💻 Technologies Used

- **Backend**: Python 3.8+, scikit-learn, pandas, numpy, joblib
- **Frontend**: Streamlit, Plotly, Custom CSS
- **Machine Learning**: K-Means Clustering, TF-IDF, Cosine Similarity
- **Data Processing**: Text preprocessing, Feature engineering, Caching
- **Development Tools**: Git, pre-commit, mypy, black, flake8

## 📁 Project Structure

```
mindmap-india/
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
├── pytest.ini             # Configuration for pytest
├── run.py                 # Main entry point
├── run_analysis.bat       # Windows batch file to run the analysis
├── setup_dev.py           # Development environment setup script
├── .gitignore            # Git ignore file
├── data/                 # Data files
│   └── careers.csv       # Career dataset
├── app/                  # Main application package
│   ├── __init__.py       # Package initialization
│   ├── app.py            # Streamlit application
│   ├── cluster_utils.py  # AI/ML utilities for career clustering
│   └── assets/           # Static assets (CSS, images)
├── tests/                # Test suite
│   ├── __init__.py
│   ├── conftest.py       # Test fixtures and configuration
│   └── test_*.py         # Test modules
├── notebooks/            # Jupyter notebooks for analysis
│   ├── career_analysis.ipynb
│   ├── clustering_new.py
│   └── requirements.txt  # Notebook-specific dependencies
├── output/               # Generated outputs and visualizations
│   └── wordclouds/       # Generated word clouds
└── scripts/              # Utility scripts
    ├── career_clustering.py
    └── career_clustering_fixed.py
```

## 🛠️ Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for version control)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/mindmap-india.git
   cd mindmap-india
   ```

2. **Create a virtual environment (recommended)**:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   # Using the provided script (Windows)
   .\run_analysis.bat
   
   # Or directly with Python
   python run.py
   ```

5. **Access the application**:
   Open your web browser and go to `http://localhost:8501`

## 🧪 Running Tests

To ensure the application works as expected, run the test suite:

```bash
# Install test dependencies
pip install -r requirements.txt
pip install pytest pytest-cov

# Run all tests
pytest

# Run tests with coverage report
pytest --cov=app --cov-report=html
```

Test coverage reports will be generated in the `htmlcov` directory.

## 🚀 Usage

1. Select a career that interests you from the dropdown menu
2. View AI-powered career recommendations
3. Explore detailed information about each recommended career
4. Use the interactive visualizations to understand career distributions

## 🧪 Testing

To run the test suite:

1. **Report Bugs**: Open an issue with detailed steps to reproduce
2. **Suggest Enhancements**: Share your ideas for new features
3. **Contribute Code**: Submit pull requests with bug fixes or new features

### Development Workflow

1. Fork the repository and create a feature branch
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. Set up the development environment
   ```bash
   # Create and activate virtual environment
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux

   # Install dependencies
   pip install -r requirements.txt
   pip install -r notebooks/requirements.txt
   ```

3. Make your changes and run tests
   ```bash
   # Run all tests
   pytest

   # Run a specific test file
   pytest tests/test_clustering.py -v
   ```

4. Format and lint your code
   ```bash
   # Auto-format code
   black .

   # Check for style issues
   flake8 .
   
   # Check type hints
   mypy .
   ```

5. Commit your changes with a descriptive message
   ```bash
   git add .
   git commit -m "Add amazing new feature"
   git push origin feature/amazing-feature
   ```

6. Open a pull request with a clear description of your changes

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Keep lines under 88 characters (Black's default line length)
- Write tests for new functionality

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with ❤️ for students and career seekers in India
- Thanks to all contributors who have helped improve this project
- Special thanks to the open-source community for the amazing tools and libraries used in this project

## Contact

For questions or feedback, please open an issue on GitHub or contact the maintainers.

## Contact

For any questions or feedback, please contact [Your Email] or open an issue on GitHub.

---

<div align="center">
  Made with ❤️ in India
</div>

## 🚀 Quick Start

### Option 1: Using pip (recommended)

```bash
# Install the package
pip install git+https://github.com/yourusername/mindmap-india.git

# Run the web application
mindmap serve
```

### Option 2: From source

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/mindmap-india.git
   cd mindmap-india
   ```

2. **Set up the environment**
   ```bash
   # Create and activate virtual environment (recommended)
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows
   
   # Install the package in development mode
   pip install -e .
   ```

3. **Run the application**
   ```bash
   # Start the web interface
   python -m mindmap.cli serve
   
   # Or use the batch file on Windows
   run_analysis.bat
   ```
   
4. **Access the web interface**
   Open your browser and navigate to `http://localhost:8501`

### Command-Line Interface (CLI)
   ```

### Running the Application

```
1. **Start the Streamlit app**

   ```bash
   streamlit run app/app.py
   ```

2. **Open your browser** and navigate to `http://localhost:8501`

## 📋 Usage

1. **Select a Career**: Choose a career that interests you from the dropdown menu
2. **View Details**: See detailed information about the selected career
3. **Get Recommendations**: Click "Find Similar Careers" to get AI-powered recommendations
4. **Explore**: Click on any recommended career to see more details

## 📊 Data

The application uses a custom dataset containing information about various careers, including:

- Career titles
- Required skills
- Relevant entrance exams
- Career domains
- Detailed descriptions

## 🔄 How It Works

1. **Data Preprocessing**:
   - Text cleaning and normalization
   - Feature extraction from career descriptions
   - Skills and domain encoding

2. **AI/ML Pipeline**:
   - TF-IDF vectorization of text data
   - K-Means clustering of similar careers
   - Cosine similarity for personalized recommendations

3. **User Interface**:
   - Interactive Streamlit dashboard
   - Real-time career recommendations
   - Data visualizations

## 👋 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👍 Acknowledgments

- Icons by [Icons8](https://icons8.com)
- Built with ❤️ using Streamlit and scikit-learn
- Inspired by the need for better career guidance tools in India

---

👋 **Happy Career Exploring!** 🚀
