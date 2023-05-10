from setuptools import setup, find_namespace_packages

setup(
    name='clean-folder',
    version='0.0.1',
    description='Very useful code',
    url='https://github.com/SergNest/clean_proj',
    author='Nester',
    author_email='sy.nesterenko@gmail.com',
    packages=find_namespace_packages(),
    entry_points = {"console_scripts": ['clean-folder=clean_folder.clean:run']}
)
