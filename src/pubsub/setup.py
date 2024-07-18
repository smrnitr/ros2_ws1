from setuptools import find_packages, setup

package_name = 'pubsub'

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
    maintainer='penguine',
    maintainer_email='smritisrivastava2005@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'talker = pubsub.publisher_member_function:main',
            'subscriber = pubsub.subscriber_member_function:main',
            'test_node = pubsub.my_first_node:main',
            'draw_circle = pubsub.draw_circle:main',
            "pose_subscriber = pubsub.pose_subscriber:main",
            "turtle_controller = pubsub.turtle_controller:main",
            "p_controller = pubsub.p_controller:main",
            "goals_score = pubsub.goals_score:main"
        ],
    },
)
