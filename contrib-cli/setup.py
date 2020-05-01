from setuptools import find_packages, setup


setup(
    name='garcon-contrib-cli',
    version='0.0.1',
    packages=find_packages(),
    setup_requires=['pytest-runner'],
    install_requires=[
        'boto>=2.34.0',
        'garcon'],
    entry_points=dict(console_scripts=[
        'garcon-activity-local = garcon.contrib.local_activity_cli:main']),
    tests_require=[
        'pytest'])
