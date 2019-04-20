from setuptools import setup

setup(
   name='AWS-Automate',
   version='0.1',
   author="Pavan", 
   license="GPLv3+",
   package_dir={'./':'snapshot'},
   packages=['snapshot'],
   url="https://github.com/plakkineni/analyzer",
   install_requires=['click', 'boto3'],
   entry_points='''
         [console_scripts]
       	 aws=snapshot.aws:cli
   ''',

)
