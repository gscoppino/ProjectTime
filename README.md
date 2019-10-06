# Project Time!

A tool that can be used to keep track of time spent on projects.

[![Build Status](https://travis-ci.org/gscoppino/ProjectTime.svg?branch=master)](https://travis-ci.org/gscoppino/ProjectTime)

## Setup Notes

### Recommended

1. Install [MiniConda](https://docs.conda.io/en/latest/miniconda.html).
2. Open a terminal, ensuring the conda `base` environment is activated. If it is
   not activated:

   `conda activate base`

3. Install [Anaconda Project](https://anaconda-project.readthedocs.io/en/latest)
   within the base environment:

   `conda install anaconda-project`

4. Start the database:

    `anaconda-project run postgres start`

5. Start the tool:

   `anaconda-project run manage.py runserver`

6. Run tests:

   `anaconda-project run manage.py test --parallel --failsafe`

### Alternative Setup (Advanced)

The tool can be set up to run manually without a conda environment.

1. Open `anaconda-project.yml` and install the dependencies listed in
   `env_specs` in any choice of environment.
2. Directly run command scripts described in the
   `anaconda-project.yml` `commands` in the environment of choice.

## Development

Run `anaconda-project run prepare --env-spec development` to build a Conda environment
with extra development tools such as a linter, code formatter, and interactive
execution environment. To take advantage of these, configure your editor or IDE
to use the `development` environment in the `envs` folder.

Development workflow is the typical workflow Django project.
Django's `django-admin` and the project `manage.py` script are aliased as
`anaconda-project` commands.

For example, to start the server:

`anaconda-project run manage.py runserver`

Or to make migrations on models:

`anaconda-project run manage.py makemigrations`

And to create a new Django app:

`anaconda-project run django-admin startapp APP_NAME`

In addition, the `postgres` script is aliased as an `anaconda-project` command.

For example, to start the database server:

`anaconda-project run postgres`

The `anaconda-project run postgres` command takes care of ensuring a database
always exists, while the `anaconda-project run manage.py` commands take care of
ensuring that the latest database migrations are always applied before the server
is started. In addition, all Python scripts are run with deprecation warnings enabled.

The `anaconda-project run ipython-kernel-create` command prepares an IPython
kernel that can be loaded into a Jupyter Notebook, allowing for execution of
code in the `development` environment in an interactive notebook. Run
`anaconda-project run jupyter notebook development.ipynb` to load a notebook
that is templated with code to load the Django project.

## Testing

Tests can be run with `anaconda-project run manage.py test`, consistent with how
other management commands are run. A recommendation would be to append the
`--parallel --failfast` switches to speed up running tests and verifying test
behavior.

To measure code coverage when running tests, use `anaconda-project run coverage`.
When running the `coverage` command this way with no command line arguments, it
defaults to `coverage run` on the command `manage.py test`, with some extra switches
to include/omit files relevant to coverage, measure branch coverage, and passing
extra flag(s) to `manage.py test` to bail early if an error occurs). To
generate a code coverage report afterwards, run `anaconda-project run coverage report`.
An HTML report can be generated using `anaconda-project run coverage html`
