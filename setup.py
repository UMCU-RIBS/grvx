from setuptools import setup


setup(
    name='grvx',
    version='0.1',
    description='',
    long_description='',
    url='https://github.com/gpiantoni/grvx',
    author="Gio Piantoni",
    author_email='grvx@gpiantoni.com',
    license='GPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.7',
        ],
    install_requires=[
        'numpy',
        'scipy',
        'wonambi',
        'nibabel',
        'plotly',
        ],
    entry_points={
        'console_scripts': [
            'grvx=grvx.bin:command',
        ],
    },
    )
