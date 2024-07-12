from setuptools import setup, find_packages

setup(
  name = 'ia',
  version = '0.1',
  author = 'Ha Hoang Hao',
  packages = find_packages(),
  description = 'Auto Generate SPSS syntax',
  install_requires = ['requests', 'bs4', 'pandas']
)
