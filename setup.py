from setuptools import setup, find_packages

setup(
    name="off-pipeline",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "sqlalchemy>=1.4.0",
        "psycopg2-binary>=2.9.0",
        "python-dotenv>=0.19.0",
    ],
)
