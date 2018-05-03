from setuptools import setup, find_packages

setup(
        name="spectre",
        packages=find_packages(where="src"),
        package_dir={'': 'src'},
        )

