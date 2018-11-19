import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django_rulebase",
    version="0.0.2",
    author="Mojtaba Asadi",
    author_email="m.asadi.al@outlook.com",
    description="Django rule base validation , inspired by laravel Request",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mojtabaasadi/django-rulebase",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GNU 3",
        "Operating System :: OS Independent",
    ],
)