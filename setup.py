from setuptools import setup, find_packages

setup(
    name="app-product-workflow",
    version="0.1.0",
    description="基于 CrewAI 的 App 全自动生产工作流",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "crewai>=0.76.0",
        "langchain>=0.3.0",
        "langchain-openai>=0.2.0",
        "langchain-anthropic>=0.2.0",
        "python-dotenv>=1.0.0",
        "rich>=13.7.0",
        "click>=8.1.0",
        "pyyaml>=6.0.0",
        "pydantic>=2.0.0",
    ],
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "app-product=main:cli",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
