import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django_rulebase",
    version="0.0.4",
    author="Mojtaba Asadi",
    author_email="m.asadi.al@outlook.com",
    description="Django rule base validation , inspired by laravel Request",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mojtabaasadi/django-rulebase",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Framework :: Django",
        "Operating System :: OS Independent",
    ],
)