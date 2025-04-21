from setuptools import setup, find_packages

setup(
    name="deep-research",
    version="0.1.0",
    description="A news search and analysis application with LLM integration",
    author="",
    author_email="",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit>=1.18.0",
        "openai>=1.0.0",
        "beautifulsoup4>=4.10.0",
        "requests>=2.26.0",
        "python-dotenv>=0.19.0",
        "googlesearch-python>=1.1.0",
        "datetime",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Researchers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "deep-research=app:main",
        ],
    },
)