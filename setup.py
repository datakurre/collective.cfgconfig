from setuptools import setup, find_packages

setup(
    name='collective.cfgconfig',
    version='1.0.0',
    description='Experiment for configuring with *.cfg instead of *.zcml',
    long_description=(open('README.txt').read() + '\n' +
                      open('CHANGES.txt').read()),
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Programming Language :: Python',
    ],
    keywords='',
    author='Asko Soukka',
    author_email='asko.soukka@iki.fi',
    url='https://github.com/datakurre/collective.cfgconfig/',
    license='GPL',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    namespace_packages=['collective'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'zope.configuration',
    ],
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """
)
