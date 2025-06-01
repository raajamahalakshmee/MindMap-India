"""Setup script for the Mindmap India package."""
import os
from setuptools import setup, find_packages

# Read the contents of requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# Read the README for the long description
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="mindmap-india",
    version="1.0.0",
    author="Mindmap India Team",
    author_email="contact@mindmapindia.example.com",
    description="AI-powered career exploration and recommendation system for India",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mindmap-india",
    packages=find_packages(include=['mindmap', 'mindmap.*']),
    package_data={
        'mindmap': ['data/*.csv', 'config/*.yaml'],
    },
    install_requires=requirements,
    python_requires='>=3.8',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Education",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords=[
        'career guidance',
        'education',
        'machine learning',
        'data science',
        'clustering',
        'recommendation system'
    ],
    project_urls={
        'Bug Reports': 'https://github.com/yourusername/mindmap-india/issues',
        'Source': 'https://github.com/yourusername/mindmap-india',
    },
    entry_points={
        'console_scripts': [
            'mindmap=mindmap.cli:main',
        ],
    },
)
