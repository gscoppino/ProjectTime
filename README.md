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
4. Start the tool:

   `anaconda-project run manage.py runserver`

5. Run tests:

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

The `anaconda-project` commands take care of ensuring that the PostgreSQL
database exists and is running at all times, in addition to ensuring the
latest database migrations are applied. All Python is run with deprecation
warnings enabled.

## Testing

There are no specific testing requirements but a recommendation to append

`--parallel --failfast`

switches when running `manage.py test` to speed up running tests and
verifying test behavior.