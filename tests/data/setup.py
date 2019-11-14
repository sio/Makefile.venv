from setuptools import setup

setup(
    name='hello',
    py_modules=['hello'],
    entry_points={
        'console_scripts': [
            'hello = hello',
        ],
    },
    install_requires=[
        'pyfiglet',
    ],
)
