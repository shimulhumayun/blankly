from setuptools import find_packages, setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, './README.md'), encoding='utf-8') as f:
    long_description = f.read()

"""
Build Info:
python3 -m build
twine upload dist/*
"""

setup(
    name='blankly',  # How you named your package folder (MyLib)
    packages=find_packages(),
    # packages=['blankly'],  # Potentially should be the same thing as name
    version='v1.18.25-beta',
    license='lgpl-3.0',  # Licenses: https://help.github.com/articles/licensing-a-repository
    description='Rapidly build, backtest & deploy trading bots',  # Give a short description about your library
    long_description=long_description,
    long_description_content_type='text/markdown',
    ext_modules=[
        # Extension("blankly.deployment.hello", [path.join("blankly", "deployment", "hello.cpp")])  # Disabled extension
    ],
    author='blankly',
    entry_points={'console_scripts': ['blankly_old = blankly.deployment.cli:main',
                                      'blankly = blankly.deployment.new_cli:main']},
    author_email='contact@blankly.finance',
    url='https://github.com/Blankly-Finance/Blankly',  # Could be github or website
    # download_url='https://github.com/EmersonDove/Blankly/archive/v0.1.1-alpha.tar.gz',
    keywords=['Crypto', 'Stocks', 'Quantitative Finance', 'Exchanges', 'Bot'],  # Keywords
    install_requires=[
        'questionary >= 2.1.0',
        'yaspin >= 3.1.0',
        'alpaca-trade-api >= 3.2.0',
        'bokeh >= 3.7.3',
        'dateparser >= 1.2.2',
        'pandas-ta >= 0.3.14b0',
        'numpy >= 2.3.2',
        'pandas >= 2.3.1',
        'python-binance >= 1.0.29',
        'requests >= 2.32.4',
        'websocket-client >= 1.8.0',
    ],
    python_requires='>=3.12',
    classifiers=[
        # Possible: "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 3.12'
    ],
)
