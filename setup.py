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
    packages=['step_driver_G071_API'],
    url='https://github.com/gelio5/step_driver_G071_API.git',
    license='MIT',
    author='Vladislav Reznik',
    author_email='vlreznik97@gmail.com',
    description='Stepper driver using MODBUS communication protocol API',
    requires=['pyserial~=3.5', 'pymodbus~=3.0.2'],
    zip_safe=True,
    platforms=['Linux', 'Win', 'Mac OS X'],
    install_requires = ['pyserial~=3.5', 'pymodbus~=3.0.2']
)
