import setuptools

readme_file = open('README.md', 'r')
readme_text = readme_file.read()

setuptools.setup(
    name='ProjectTime',
    description='A tool that can be used to keep track of time spent on projects.',
    version='1.0.0',
    python_requires='~=3.8',
    install_requires=[
        'psycopg2~=2.8',
        'sqlparse~=0.4',
        'pytz~=2019.3',
        'django~=3.2',
        'django-filter~=2.4',
        'django-tables2~=2.4',
        'pandas~=1.2',
        'bokeh~=2.3',
        'django-heroku',
        'gunicorn',
    ],
    author='Giuseppe Scoppino',
    author_email='scoppino.giuseppe@gmail.com',
    url='https://github.com/gscoppino/ProjectTime',
    long_description=readme_text,
    long_description_content_type='text/markdown',
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src'),
    data_files=[('.', ['anaconda-project.yml'])],
    entry_points={
        'console_scripts': ['project-time = ProjectTime.manage:main']
    }
)

readme_file.close()
