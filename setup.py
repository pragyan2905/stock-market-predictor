from setuptools import find_packages, setup

setup(
    name='stock_market_predictor',
    version='0.0.1',
    author='pragyan2905',
    author_email='your-email@example.com',
    package_dir={'': 'src'},
    packages=find_packages(where='src')
)
