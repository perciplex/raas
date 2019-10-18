import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# What license are we?
setuptools.setup(
    name="raasgym",
    version="0.0.1",
    author="Max King, Benjamin Wiener, Declan Oller, Philip Zucker",
    author_email="team@perciplex.com",
    description="A mock OpenAI gym library for use with the Perciplex RaaS platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ishmandoo/raas",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)