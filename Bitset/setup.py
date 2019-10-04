from setuptools   import setup

setup(name = 'Bitset',
      version='0.0.1',
      description='Bitset Class',
      author='Jon Pajaud',
      author_email='jpajaud2@gmail.com',
      packages = ['bitset'],
      package_data={'bitset':['DocStrings/*.txt']}
)

# run python setup.py bdist_egg
# resulting egg in in ./dist/ directory
