from setuptools import setup, find_packages

setup(
    name='ayuthos-ai',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'rich',
        'pydantic',
        'langgraph',
        'transformers',
        'asyncpg',
        'redis',
        'aiohttp',
        'websockets',
        'python-dotenv',
    ],
    entry_points={
        'console_scripts': [
            'ayuthos = cli.ayuthos:cli',
        ],
    },
)
