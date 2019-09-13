# Project Time!

A tool that can be used to keep track of time spent on projects.

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

Development workflow is the typical workflow Django project. Django's
`django-admin` and the project `manage.py` script are aliased as
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

## Testing

There are no specific testing requirements but a recommendation to append

`--parallel --failfast`

switches when running `manage.py test` to speed up running tests and
verifying test behavior.
