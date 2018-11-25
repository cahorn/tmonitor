import setuptools

setuptools.setup(
    name="tmonitor",
    version="0.0.1",
    author="C. Ansel Horn",
    author_email="ansel@horn.name",
    description="A simple temperature monitor",
    license="WTFPL",
    install_requires=['python-crontab'],
    packages=setuptools.find_packages(),
)

