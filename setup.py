from setuptools import setup
import os


version = '0.03'

try:  # this block doesn't work under tox
  here = os.path.abspath(os.path.dirname(__file__))
  README = open(os.path.join(here, 'README.md')).read()
  HISTORY = open(os.path.join(here, 'HISTORY.md')).read()
except:
  pass


setup(name='pytest-random',
      version=version,
      description='py.test plugin to randomize tests',
      author='Leah Klearman',
      author_email='lklrmn@gmail.com',
      url='https://github.com/klrmn/pytest-random',
      install_requires=['pytest>=2.2.3', 'pytest-cache'],
      py_modules=['random_plugin'],
      entry_points={'pytest11': ['pytest_random = random_plugin']},
      license='Mozilla Public License 2.0 (MPL 2.0)',
      keywords='py.test pytest qa',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'])
