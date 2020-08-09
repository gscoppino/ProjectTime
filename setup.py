import os
import setuptools
import yaml

project_file = open('anaconda-project.yml', 'r')
readme_file = open('README.md', 'r')

project_spec = yaml.load(project_file, Loader=yaml.Loader)
readme_text = readme_file.read()

setuptools.setup(
    name=project_spec['name'],
    description=project_spec["description"],
    version=os.getenv('PROJECT_TIME_VERSION'),
    python_requires='~=3.8',
    install_requires=[
        'psycopg2~=2.8',
        'sqlparse~=0.3',
        'pytz~=2019.3',
        'django~=3.0',
        'pandas~=1.0',
        'bokeh~=2.1',
        'tabulate~=0.5'
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

project_file.close()
readme_file.close()
