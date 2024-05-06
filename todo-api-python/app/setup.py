from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()


setup(
    name="todo-api-python",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi==0.95.0",
        "uvicorn==0.21.1",
        "sqlalchemy==2.0.9",
        "psycopg2-binary==2.9.5",
        "wait-for-it==2.2.0",
        "pytest==7.2.2",
    ],
)
