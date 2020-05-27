from setuptools import setup

setup(
    name='internet_object',
      version='0.1',
      description='The python internet-object parser',
      long_description='The python internet-object parser',
    #   classifiers=[
    #     'Development Status :: 3 - Alpha',
    #     'License :: OSI Approved :: MIT License',
    #     'Programming Language :: Python :: 2.7',
    #     'Topic :: Text Processing :: Linguistic',
    #   ],
      keywords='internet-object internetobject rest http json',
    #   url='http://github.com/storborg/funniest',
      author='Mohamed Aamir Maniar',
      author_email='aamir@internetobject.org',
      license='ISC',
      packages=['internet_object'],
    #   install_requires=[
    #       'markdown',
    #   ],
      include_package_data=True,
      zip_safe=False,
    #   test_suite='nose.collector',
    #   tests_require=['nose']
      )