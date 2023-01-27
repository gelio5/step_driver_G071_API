"""
Installs pymodbus using distutils
Run:
    python setup.py install
to install the package from the source archive.
"""
from setuptools import setup

setup(
    name='step_driver_g071_api',
    version='0.6',
    packages=['step_driver_g071_api'],
    url='https://github.com/gelio5/step_driver_G071_API.git',
    license='MIT',
    author='Vladislav Reznik',
    author_email='vlreznik97@gmail.com',
    description='Stepper driver using MODBUS communication protocol API',
    long_description='''
    Step driver aims to be fully implemented API for managing stepper driver via MODBUS RTU, which
    was realized in STM32G071 microcontroller.
    ''',

    requires=['pyserial', 'pymodbus'],
    zip_safe=True,
    platforms=['Linux', 'Win', 'Mac OS X'],
    install_requires = ['pyserial~=3.5', 'pymodbus~=3.0.2']
)
