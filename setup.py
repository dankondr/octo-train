from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='octo_train',
      description='Console application to make you a great programmer.',
      version='0.1.2',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'octo-train = octo_train.main:main'
          ]},
      install_requires=['tinydb>=3.15.2', 'colorful', 'requests', 'beautifulsoup4'],
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='dankondr',
      author_email="dankondr@icloud.com",
      url="https://github.com/dankondr/octo-train",
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
      ],
      python_requires='>=3.7'
      )
