from setuptools import setup, find_packages

setup(
    name="temperature-spike-detector",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "psutil",
        "pandas",
        "numpy",
        "scikit-learn",
        "pyyaml",
        "rich",
        "wmi",
        "py3nvml",
        "joblib"
    ],
    entry_points={
        'console_scripts': [
            'thermal-monitor=main:main',
        ],
    },
)
