from setuptools import find_packages, setup

package_name = 'decision_making_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hhk-laptop',
    maintainer_email='whaihong@g.skku.edu',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'rail_pd_controller_node = decision_making_pkg.rail_pd_controller_node:main',
            'rail_approach_action_server_node = decision_making_pkg.rail_approach_action_server_node:main',
        ],
    },
)
