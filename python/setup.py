from setuptools import setup, find_packages

setup(
    name="musiclib",
    version="0.0.1",
    description="musiclib is a library for music",
    license="private",
    keywords="Music Representation",
    url="http://melodrive.com",
    packages=find_packages(exclude=['tests'])
)
