from setuptools import find_packages, setup

setup(
    name='onlylegs',
    version='23.03.02',
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
        'platformdirs',
    ],
)
