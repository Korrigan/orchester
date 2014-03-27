from setuptools import setup

def readme():
    """Extract contents from README.rst"""
    with open('README.rst') as r:
        return r.read()

def requirements():
    """Fetch requirements from requirements.txt"""
    with open('requirements.txt') as req:
        return req.read().splitlines()

setup(name='orchester',
      version='0.1',
      description='Orchester is a scalable IaaS/PaaS solution.',
      long_description=readme(),
      author='Orchester.io team',
      classifiers=[
          'Development Status :: 1 - Planning',
          'Programming Language :: Python :: 2.7',
      ],
      packages=['orchester'],
      test_suite='orchester.tests',
      install_requires=requirements(),
  )
