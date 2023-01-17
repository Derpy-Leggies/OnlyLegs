from setuptools import find_packages, setup

setup(
    name='onlylegs',
    version='170123',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'libsass',
        'python-dotenv',
        'pillow',
        'colorthief',
        'pyyaml',
    ],
)
