from setuptools import setup, find_packages

setup(
    name="public-transit-api",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "pydantic-settings",
        "pandas",
        "pytest",
        "httpx",
        "requests",
        "mangum",
    ],
)
