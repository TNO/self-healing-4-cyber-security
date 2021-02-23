import os
from setuptools import setup, find_packages

setup(
    name="sh4cs_common",
    version="0.0.4",
    packages=["sh4cs_common"],
    author="TNO",
    author_email=["jeffrey.panneman@tno.nl"],
    python_requires=">=3.7",
    description="Common python files for the SH4CS PoC",
    license="TNO proprietary",
    keywords="SH4Cs anomaly detection PoC",
    long_description=open(os.path.join(os.path.dirname(__file__), "README.md")).read(),
    install_requires=["redis"],
    extras_require={},
)
