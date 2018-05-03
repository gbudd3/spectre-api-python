from setuptools import setup, find_packages

setup(
        name="spectre-api",
        description="Wrapper to use the Lumeta Spectre API",
        version="0.0.1",
        license="MIT",
        install_requires=['requests'],
        packages=find_packages(where="src"),
        package_dir={'': 'src'},
        )

