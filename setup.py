from setuptools import setup

setup(
    name='pyLCM',
    version='0.0.2',
    description='Flow calculation in reinforcement textiles.',
    url='https://github.com/binyang424/pyLCM',
    author='Bin Yang',
    author_email='bin.yang@polymtl.ca',
    license='BSD 2-clause',
    packages=['pyLCM', 'pyLCM.perm', 'pyLCM.resin'],
    install_requires=['numpy>=0.5',             
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
