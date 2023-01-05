from pathlib import Path

from setuptools import (find_packages,
                        setup)

import ground

project_base_url = 'https://github.com/lycantropos/ground/'


def read_file(path_string: str) -> str:
    return Path(path_string).read_text(encoding='utf-8')


setup(name=ground.__name__,
      packages=find_packages(exclude=('tests', 'tests.*')),
      version=ground.__version__,
      description=ground.__doc__,
      long_description=read_file('README.md'),
      long_description_content_type='text/markdown',
      author='Azat Ibrakov',
      author_email='azatibrakov@gmail.com',
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
      ],
      license='MIT License',
      url=project_base_url,
      download_url=project_base_url + 'archive/master.zip',
      python_requires='>=3.7',
      install_requires=read_file('requirements.txt'))
