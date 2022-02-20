from setuptools import setup

setup(
    name='wordle',
    entry_points={
        'console_scripts': [
            'wordle = wordle:main',
        ],
    }
)