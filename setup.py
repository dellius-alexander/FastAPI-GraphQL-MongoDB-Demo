from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
    print(long_description)

setup(
    name="FastAPI_GraphQL_MongoDB_Demo",
    version="0.1.0",
    author="Dellius Alexander",
    author_email="info@hyfisolutions.com",
    maintainer="info@hyfisolutions.com",
    maintainer_email="info@hyfisolutions.com",
    description="Demo of FastAPI and GraphQL integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dellius-alexander/FastAPI-GraphQL-MongoDB-Demo.git",
    packages=find_packages(where="."),
    package_dir={"": "."},
    license="LICENSE",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: LICENSE",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    entry_points={"console_scripts": ["main_cli = main:app"]},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "backports.zoneinfo==0.2.1;python_version<=\"3.9\"",
        "bcrypt==4.0.1",
        "fastapi==0.95.1",
        "graphene==3.2.2",
        "graphene-mongo==0.2.15",
        "graphql-core==3.2.3",
        "mongoengine==0.24.2",
        "python-dotenv==0.21.0",
        "uvicorn==0.21.1"
    ],
)
