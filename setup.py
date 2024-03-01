from setuptools import setup, find_packages

description = '摸鱼办公室 cli 版本，自用'

with open('README.md', 'r', encoding='UTF-8') as f:
    long_description = f.read()

setup(
    name='mofish_cli',
    version='1.1.0',
    description=description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Clustering',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Systems Administration',
    ],
    python_requires='>=3.7',
    author='PY-GZKY',
    author_email='HiNyaasu@outlook.com',
    url='https://github.com/Nyaasu66/Mofish',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    entry_points="""
        [console_scripts]
        moyu=mofish_cli.main:cli
    """,
    install_requires=[
        'click>=6.7',
        'zhdate',
        'blessed',
        'colorama'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
)
