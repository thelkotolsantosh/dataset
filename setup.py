"""
Setup configuration for dataset analysis package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="dataset-analyzer",
    version="1.0.0",
    author="santosh thelkotlol",
    author_email="thelkotolsantosh@gmail.com",
    description="A comprehensive data analysis and exploration toolkit for data scientists",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/dataset",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    keywords="data analysis pandas visualization exploratory-data-analysis",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/dataset/issues",
        "Source": "https://github.com/yourusername/dataset",
        "Documentation": "https://github.com/yourusername/dataset/blob/main/README.md",
    },
)
