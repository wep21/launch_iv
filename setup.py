from setuptools import find_packages
from setuptools import setup

package_name = 'launch_iv'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/' + package_name, ['package.xml']),
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
    ],
    install_requires=[
        'setuptools',
        'launch',
        'launch_ros',
        'pyyaml',
    ],
    zip_safe=True,
    author='Daisuke Nishimatsu',
    author_email='daisuke.nishimatsu@tier4.jp',
    maintainer='Daisuke Nishimatsu',
    maintainer_email='daisuke.nishimatsu@tier4.jp',
    keywords=['ROS'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='Autoware.iv specific extensions to `launch`.',
    long_description=(
        'This package provides autoware.iv specific extensions to the launch package.'
    ),
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'launch.frontend.launch_extension': [
            'launch_iv = launch_iv',
        ],
    }
)
