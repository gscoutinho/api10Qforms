# setup.py

from setuptools import setup, find_packages

setup(
    name='sec_10q_data',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pandas',
    ],
    author='Gabriel Coutinho',
    author_email='eng.gabrielcoutinho@outlook.com.br',
    description='Package to retrieve 10-Q form data from the SEC EDGAR database.',
    url='https://github.com/yourusername/sec_10q_data',
)
