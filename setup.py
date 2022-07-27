import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setuptools.setup(
    name="Py Utils",
    version="0.1.0",
    description="A collection of useful Python utilities to help with writing shell scripts in Python",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hamidzr/py-utils",
    author="Hamid Zare",
    author_email="contact@hamidza.re",
    keywords="python shell script utilities",
    license="GPLv2",
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python",
        # "Topic :: Multimedia :: Video",
        # "Topic :: Multimedia :: Video :: Capture",
    ],
    python_requires=">=3.8",
    package_dir={"": "src"},
    project_urls={
        "Homepage": "https://github.com/hamidzr/py-utils",
        "Bug Tracker": "https://github.com/hamidzr/py-utils/issues",
    },
    packages=setuptools.find_packages(where="src"),
    include_package_data=True,
    install_requires=[
        "typer"
    ],
    entry_points={"console_scripts": ["py_utils = py_utils.__main__:app",]},
)
