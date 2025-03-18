from setuptools import setup, find_packages

setup(
    name="notion_github",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "notion-client>=2.0.0",
        "PyYAML>=6.0",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
        "pytest>=7.4.0",
    ],
) 