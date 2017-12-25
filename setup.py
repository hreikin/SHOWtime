from setuptools import setup, find_packages

setup(
    name='odroidshow',
    version='0.0.1',
    description='Interface for displaying text and data on ODROID Show2 LCD display board',
    url='https://github.com/Matoking/SHOWtime.git',
    author='Janne Pulkkinen',
    author_email='jannepulk@gmail.com',
    license='Unlicense',
    packages=['odroidshow'],
    python_requires='>=3',

    install_requires=[
        'argparse',
        'Pillow',

        # Optional for sysinfo tab
        #'psutil',
        #'humanfriendly',

        # Optional for uptime tab
        #'httplib2',

        # Optional for bitcoin tab
        #'python-jsonrpc',
    ],

    entry_points={
        'console_scripts': [
            'odroidshow=odroidshow.showtime',
        ],
    },
)
