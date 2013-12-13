from setuptools import setup

def readme():
    """Extract contents from README.rst"""
    with open('README.rst') as r:
        return r.read()


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
      install_required=[
          'flask',
      ],
  )
