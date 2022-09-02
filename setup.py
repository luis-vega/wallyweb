from setuptools import find_packages
from setuptools import setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(name='wallyweb',
      version="0.0.1",
      description="wheres wally webpage (api_pred)",
      license="None",
      author="wheres wally group",
      author_email="blah_001100@hotmail.com",
      url="https:https://github.com/Krastro/whereswally",
      install_requires=requirements,
      packages=find_packages(),
      test_suite="tests",
      # include_package_data: to install data from MANIFEST.in
      include_package_data=True,
      zip_safe=False)
