import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-YOUR-USERNAME-HERE",
    version="0.0.1",
    author="Dmitry Frolov, Boris Mirkin, Susana Nascimento, Trevor Fenner",
    author_email="dmitsf@gmail.com",
    description="GOT (generalization over a taxonomy) package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dmitsf/ParGenFS",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
