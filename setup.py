"""Setup script for gitlabenv2csv"""

import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="gitlabenv2csv",
    version="1.0.2",
    description="""gitlabenv2csv allows you to download GitLab ENV variables to a csv file. 
                   Manually edit and upload back to the project / group.""",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/zales/gitlabenv2csv",
    author="Ondrej Zalesky",
    author_email="o.zalesky@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["gitlabenv2csv"],
    include_package_data=True,
    install_requires=[
        "ConfigArgParse", "python-dateutil", "python-gitlab", "pandas-schema"
    ],
    entry_points={"console_scripts": ["gitlabenv2csv=gitlabenv2csv.__main__:main"]},
)
