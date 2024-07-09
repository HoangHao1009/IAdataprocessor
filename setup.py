from setuptools import setup

setup(
  name = 'InsightAsiaDataProcessor',
  version = '0.1',
  author = 'Ha Hoang Hao',
  packages = setup.find_packages(),
  description = 'Auto Generate SPSS syntax',
  install_requires = ['re', 'requests', 'bs4', 'pandas']
)
