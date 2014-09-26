from distutils.core import setup

setup(
    name='django-databrowse',
    version='1.3',
    packages=['django_databrowse', 'django_databrowse.plugins'],
    package_dir={'django_databrowse': 'django_databrowse'},
    package_data={
        'django_databrowse': [
            'templates/databrowse/*.html',
            'templates/databrowse/include/*.html'
        ]
    },
    provides=['django_databrowse'],
    include_package_data=True,
    url='https://github.com/Alir3z4/django-databrowse',
    license=open('LICENSE').read(),
    author='Alireza Savand',
    author_email='alireza.savand@gmail.com',
    description='Databrowse is a Django application that lets you browse your data.',
    long_description=open('README.rst').read(),
    install_requires=['Django', ],
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
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development'
    ],
)
