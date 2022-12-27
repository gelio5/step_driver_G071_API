"""
Installs pymodbus using distutils
Run:
    python setup.py install
to install the package from the source archive.
"""
from setuptools import setup

setup(
    name='step_driver_G071_API',
    version='0.1',
    packages=['step_driver'],
    url='https://github.com/gelio5/step_driver_G071_API.git',
    license='',
    author='Vladislav Reznik',
    author_email='vlreznik97@gmail.com',
    description='',
    requires=['pyserial~=3.5', 'pymodbus~=3.0.2']

)
