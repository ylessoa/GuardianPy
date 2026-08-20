from setuptools import setup, find_packages

setup(
    name="GuardianPy",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "psutil==6.1.0",
        "requests==2.32.3",
        "yara-python==4.5.4",
        "pytest==9.1.1",
        "colorama==0.4.6",
        "cryptography==43.0.1",
        "pyinstaller==6.10.0",
        "watchdog==4.0.1",
    ],
)
