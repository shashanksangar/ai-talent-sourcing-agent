from setuptools import setup, find_packages

setup(
    name="ai-talent-sourcing-agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "anthropic",
        "requests",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "sourcing-agent=src.sourcing_agent:main",
        ],
    },
    python_requires=">=3.8",
)