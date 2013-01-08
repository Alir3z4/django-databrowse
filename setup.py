from distutils.core import setup

MY_NAME = 'Alireza Savand'
MY_EMAIL = 'alireza.savand@gmail.com'

setup(
    name='django-databrowse',
    version='1.0',
    packages=['django_databrowse', 'django_databrowse.plugins'],
    package_dir={'django_databrowse': 'django_databrowse'},
    package_data={'django_databrowse': ['templates/databrowse/*']},
    provides=['django_databrowse'],
    include_package_data=True,
    url='http://pypi.python.org/pypi/django-databrowse',
    license=open('LICENSE').read(),
    author=MY_NAME,
    author_email=MY_EMAIL,
    maintainer=MY_NAME,
    maintainer_email=MY_EMAIL,
    description='Databrowse is a Django application that lets you browse your data.',
    long_description=open('README.rst').read(),
    install_requires=['django',],
    keywords=[
        'django',
        'web',
        'databrowse',
        'data'
    ],
    platforms='OS Independent',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Framework :: Django',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development'
    ],
)
