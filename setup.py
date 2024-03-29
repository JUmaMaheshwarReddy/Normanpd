from setuptools import setup, find_packages

setup(
    name='project0',
    version='1.0',
    author='J Uma Maheshwar Reddy',
    author_email='umamaheshwarreddy.jangalapalli@ou.edu',
    packages=find_packages(exclude=('tests', 'docs')),
    setup_requires=['pytest-runner'],
    tests_require=['pytest']
)
