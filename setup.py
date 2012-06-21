from setuptools import setup, find_packages

setup(
    name = "Resty",
    version = "0.1",
    packages = ['resty'],
    include_package_data = True,

    author = "Aaron O'Mullan",
    author_email = "aaron.omullan@gmail.com",
    description = "A tiny but fast async RESTful framework, using gevent.",
    license = "Apache",
    keywords = "python gevent fast tiny rest async",
    url = "https://github.com/AaronO/resty",
    install_requires = ['gevent'],

    classifiers = [
        'Development Status :: 0.2 - Beta Testing',
        'Environment :: Unix-like Systems',
        'Intended Audience :: Developers, Project managers, Sys admins',
        'Programming Language :: Python',
        'Operating System :: Unix-like',
    ],
)
