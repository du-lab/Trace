from setuptools import setup

setup(
    name='Trace Online',
    version='0.0.1',
    long_description=__doc__,
    packages=['trace_online'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask']
)