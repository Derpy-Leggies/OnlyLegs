from setuptools import find_packages, setup

setup(
    name='onlylegs',
    version='250123',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-compress',
        'libsass',
        'python-dotenv',
        'pillow',
        'colorthief',
        'pyyaml',
    ],
)
