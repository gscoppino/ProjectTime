# Project Time

A tool that can be used to keep track of time spent on projects.

[![Build Status](https://app.circleci.com/pipelines/github/gscoppino/ProjectTime?branch=master)](https://app.circleci.com/pipelines/github/gscoppino/ProjectTime)

## Development Environment Setup

1. Install [Miniconda](https://docs.conda.io/miniconda.html).

   Miniconda is the recommended environment for development. Miniconda is a minimal distribution of [Conda](https://docs.conda.io), a cross-platform package management and environment management tool for Python projects.

2. Open a terminal and ensure the conda `base` environment is activated.

3. Install Anaconda Project: `conda install anaconda-project`

   [Anaconda Project](https://anaconda-project.readthedocs.io) is the recommended task runner, and is installable using `conda`. Anaconda Project allows for multiple Conda environments to be defined in a single file, each with their own associated package dependencies. Commands can be associated with specific environments, and can be tailored to different platforms. Anaconda Project also assists with environment setup and cross-platform environment variables, among other things.

## Useful Project Commands

The project is built on the [Django](https://www.djangoproject.com) framework. It is backed by the [PostgreSQL](https://www.postgresql.org) database.

Task                            | Command
--------------------------------|-------------------------------------------
Create a database               | `anaconda-project run pg_ctl initdb`
Start the database              | `anaconda-project run postgres`
Apply Django migrations         | `anaconda-project run manage.py migrate`
Start the web server            | `anaconda-project run manage.py runserver`
Run unit tests                  | `anaconda-project run manage.py test`
Run unit tests w/ code coverage | `anaconda-project run coverage run manage.py test`
Generate coverage report        | `anaconda-project run coverage report`
Generate coverage report (HTML) | `anaconda-project run coverage html`
Run acceptance tests            | `anaconda-project run robot test/`
Start a new Django app          | `anaconda-project run django-admin startapp <app> src`
Create new Django migrations    | `anaconda-project run manage.py makemigrations`
Run a Jupyter notebook          | `anaconda-project run jupyter notebook`

## Extra Development Tips

### Development Tools

By running `anaconda-project prepare --env-spec devtools`, an environment containing useful development tools (such as linters, formatters, and interactive execution environments) will be created in `envs/devtools`.

### Unit Testing

* Pass `--fail-fast` to fail execution immediately as soon as a test fails.
* Pass `--parallel` to run tests in parallel.

### Acceptance Testing

* Pass `-d` to write Robot output files to a directory of your choice.
* Pass `-v` to pass variables to Robot.
  * `-v BROWSER:<browser>` will change the browser Robot uses to test the application. Examples of valid browsers are:
      - `firefox`
      - `headlessfirefox`
      - `chrome`
      - `headlesschrome`
   * `-v DRIVER_SPEED_SECS:<seconds>` will speed up or slow down test execution

### Performance Profiling

The `application-debug` environment adds `django-debug-toolbar` to the
application runtime. To use it, do:
`anaconda-project run --env-spec application-debug manage.py runserver`.

## Packaging

For PyPi: `anaconda-project run setup.py sdist bdist_wheel`
For Conda: `anaconda-project run conda build conda-recipe`
