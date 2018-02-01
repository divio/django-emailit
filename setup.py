from setuptools import setup, find_packages

from emailit import __version__


setup(
    name="django-emailit",
    version=__version__,
    url='http://github.com/divio/django-emailit',
    license='BSD',
    platforms=['OS Independent'],
    description="Make sending html emails easy.",
    long_description=open('README.rst').read(),
    author='Stefan Foulis',
    author_email='stefan@foulis.ch',
    packages=find_packages(),
    install_requires=(
        'Django>=1.6,<2.0',  # TODO: 2.0 may work here but it's not tested.
        'premailer>=1.12',
        'django-absolute',
    ),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
