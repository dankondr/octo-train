from setuptools import setup, find_packages

setup(name="octo-train",
      description="Console application to make you a great programmer.",
      version="0.1.0",
      packages=find_packages(),
      install_requires=["tinydb>=3.15.2", 'colorful', 'requests', 'beautifulsoup4'],
      author="dankondr"
      )
