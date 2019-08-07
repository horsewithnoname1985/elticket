from setuptools import setup
from os.path import abspath, dirname, join, isfile
from setuptools.command.install import install
from os import listdir, mkdir
from shutil import copy
from pathlib import Path
import site
import re

from elticket import config

CURDIR = Path(dirname(abspath(__file__)))
VERSION = re.search(r'^__version__\s*=\s*"(.*)"',
                    open('elticket/elticket.py').read(), re.M).group(1)


class InstallWithCopyUserConfigFilesIfNotExisting(install):
    INSTALL_DIR = Path(site.getsitepackages()[0]).joinpath("elticket")
    files = []

    for file in listdir(CURDIR.joinpath("elticket/templates")):
        files.append("templates/" + file)

    def run(self):
        import logging
        try:
            mkdir(config.BASE_DIR)
            mkdir(config.TEMPLATE_DIR)
        except FileExistsError:
            pass

        for filename in self.files:
            logging.warning(str(config.BASE_DIR.joinpath(filename)))
            if isfile(config.BASE_DIR.joinpath(filename)):
                pass
            else:
                copy(src=CURDIR.joinpath("elticket/" + filename),
                     dst=str(config.TEMPLATE_DIR))

        install.run(self)


with open("README.rst", "rb") as f:
    LONG_DESCR = f.read().decode("utf-8")

with open(join(CURDIR, 'requirements.txt')) as f:
    REQUIREMENTS = f.read().splitlines()

setup(
    name="elticket",
    version=VERSION,
    package_dir={
        "elticket": "elticket",
        "elticket.elements": "elticket/elements",
    },
    packages=["elticket", "elticket.elements"],
    include_package_data=True,
    package_data={
        "elticket.templates": ["elticket/templates/*.txt"],
        "elticket": ["elticket/*.ini"],
    },
    cmdclass={
        "install": InstallWithCopyUserConfigFilesIfNotExisting,
    },
    entry_points={
        "console_scripts": ["elticket = elticket.elticket:main"]
    },
    long_description=LONG_DESCR,
    author="Arne Wohletz",
    author_email="a.wohletz@erhardt-leimer.com",
    url="http://www.erhardt-leimer.com",
    description="Automatic creation of E+L Jira tickets",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
    install_requires=REQUIREMENTS
)
