from setuptools import setup, find_packages

setup(
  name = 'InsightAsiaDataProcessor',
  version = '0.1',
  author = 'Ha Hoang Hao',
  packages = find_packages(),
  description = 'Auto Generate SPSS syntax',
  install_requires = ['re>=2.2.1', 'requests', 'bs4', 'pandas']
)
