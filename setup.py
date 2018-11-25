import setuptools

setuptools.setup(
    name="tmonitor",
    version="0.0.1",
    author="C. Ansel Horn",
    author_email="ansel@horn.name",
    description="A simple temperature monitor",
    license="WTFPL",
    url="https://github.com/cahorn/tmonitor",
    install_requires=['python-crontab'],
    packages=setuptools.find_packages(),
    scripts=['scripts/tmonitor'],
)

