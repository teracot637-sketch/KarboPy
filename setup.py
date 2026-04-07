from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="karboai",
    version="1.0.0",
    description="Python library for https://karboai.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/karboai-python",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "aiohttp>=3.9",
        "python-socketio>=5.10",
        "pydantic>=2.0",
    ],
    license="MIT",
)
