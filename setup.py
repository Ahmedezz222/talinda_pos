import os
from setuptools import setup, find_packages

def read_requirements():
    """Read the requirements.txt file and return list of requirements."""
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="talinda_pos",
    version="2.0.0",
    author="Talinda POS Team",
    description="A modern Point of Sale system built with PyQt5",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'talinda-pos=src.main:main',
        ],
    },
    include_package_data=True,
    package_data={
        'talinda_pos': [
            'resources/styles/*.qss',
            'resources/translations/*.json',
            'resources/images/*',
        ],
    },
)
