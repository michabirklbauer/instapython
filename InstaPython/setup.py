import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="InstaPython",
    version="1.0.1",
    author="Micha Birklbauer",
    author_email="micha.birklbauer@gmail.com",
    description="A set of classes and functions to access Instagram",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/t0xic-m/instapython",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
