from setuptools import find_packages
from setuptools import setup

from arbitrage_opportunity import PROJECT_NAME, VERSION

PACKAGES = find_packages(
    exclude=[
        "tests"
    ]
)

# long description from README file
with open('README.md', encoding='utf-8') as f:
    DESCRIPTION = f.read()

REQUIRED = open('requirements.txt').readlines()
REQUIRES_PYTHON = '>=3.10'

setup(
    name=PROJECT_NAME,
    version=VERSION,
    url='https://github.com/Drakkar-Software/Triangular-Arbitrage',
    author='Drakkar-Software',
    author_email='contact@drakkar.software',
    description='Triangular arbitrage by OctoBot',
    packages=PACKAGES,
    long_description=DESCRIPTION,
    long_description_content_type='text/markdown',
    tests_require=["pytest"],
    test_suite="tests",
    zip_safe=False,
    data_files=[],
    include_package_data=True,
    install_requires=REQUIRED,
    python_requires=REQUIRES_PYTHON,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.10',
    ],
)