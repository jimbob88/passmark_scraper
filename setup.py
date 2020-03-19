import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="passmark_scraper-jimbob88", # Replace with your own username
    version="0.0.1",
    author="James Blackburn",
    author_email="blackburnfjames@gmail.com",
    description="A ( for personal use only ) scraper for CPU + GPU data from passmark.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jimbob88/passmark_scraper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)