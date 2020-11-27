# Project Time

A tool that can be used to keep track of time spent on projects.

[![gscoppino](https://circleci.com/gh/gscoppino/ProjectTime.svg?style=svg)](https://circleci.com/gh/gscoppino/ProjectTime/tree/master)

## Development Environment Setup

1. Install [Miniconda](https://docs.conda.io/miniconda.html).

   Miniconda is the recommended environment for development. Miniconda is a minimal distribution of [Conda](https://docs.conda.io), a cross-platform package management and environment management tool for Python projects.

2. Open a terminal and ensure the conda `base` environment is activated.

3. Install Anaconda Project and DoIt: `conda install anaconda-project doit`

   [Anaconda Project](https://anaconda-project.readthedocs.io) is a basic task runner for Conda projects. Anaconda Project allows for multiple Conda environments to be defined in a single file, each with their own associated package dependencies. Tasks can be associated with specific environments, and can be tailored to different platforms. Anaconda Project also assists with environment setup and cross-platform environment variables, among other things.

   [DoIt](https://pydoit.org) is a more advanced task runner that is used as a wrapper around Anaconda Project. It can handle orchestration of tasks and their dependencies, and avoid unnecessary rework for tasks that have been previously completed.

4. (Optional) Prepare the default environment: `doit prepare`

   The default environment contains all development, debug, and testing dependencies, in addition to useful development tools (such as linters, formatters, and Jupyter Notebook).

## Useful Project Commands

The project is built on the [Django](https://www.djangoproject.com) framework. It is backed by the [PostgreSQL](https://www.postgresql.org) database.

Run `doit list` to get a list of high-level tasks that can be run via `doit <task>`. DoIt tasks represent the most common use cases for day-to-day development. For more advanced usage, `anaconda-project` tasks can be used directly, as they provide direct interfaces to the development tools (Use `anaconda-project list-commands` to see available commands). Anaconda Project tasks and DoIt tasks can be mixed and matched as needed.

A list of useful lower level `anaconda-project` commands is provided for convenience.

Task                            | Command
--------------------------------|----------------------------------------------------------------------------
Create a database               | `anaconda-project run pg_ctl initdb`
Start the database              | `anaconda-project run postgres`
Apply Django migrations         | `anaconda-project run manage.py migrate`
Start the web server            | `anaconda-project run manage.py runserver`
Start a test server             | `anaconda-project run manage.py testserver <absolute/path/to/fixture>`
Run unit tests                  | `anaconda-project run manage.py test`
Run unit tests w/ code coverage | `anaconda-project run coverage run manage.py test`
Generate coverage report        | `anaconda-project run coverage report`
Generate coverage report (HTML) | `anaconda-project run coverage html`
Run acceptance tests            | `anaconda-project run robot test/`
Format Python code              | `anaconda-project run autopep8 -r -i --max-line-length 88 src/ProjectTime`
Sort imports in Python files    | `anaconda-project run isort src/ProjectTime`
Lint Python files               | `anaconda-project run pylint src/ProjectTime`
Start a new Django app          | `anaconda-project run django-admin startapp <app> src/ProjectTime`
Create new Django migrations    | `anaconda-project run manage.py makemigrations`
Run a Jupyter notebook          | `anaconda-project run jupyter notebook`

## Extra Development Tips

### Database

* Pass `-E` to `postgres` to run with verbose logging, where every database query will be printed.

### Unit Testing

* Pass `--fail-fast` to fail execution immediately as soon as a test fails.
* Pass `--parallel` to run tests in parallel.

### Acceptance Testing

When starting the test server, a few useful flags:
* Pass `--noinput` to wipe the test database without a user prompt
* Pass `--addrport` to use a different port e.g. running the dev and test server side by side

For running robot:

* Pass `-d` to write Robot output files to a directory of your choice.
* Pass `-v` to pass variables to Robot.
  * `-v BROWSER:<browser>` will change the browser Robot uses to test the application. Examples of valid browsers are:
      - `firefox`
      - `headlessfirefox`
      - `chrome`
      - `headlesschrome`
   * `-v DRIVER_SPEED_SECS:<seconds>` will speed up or slow down test execution
   * `-v SERVER_PORT:<port>` to change the port Robot uses to access the application. Useful if running a dev and test server side-by-side.

### Performance Profiling

The `application-debug` environment adds `django-debug-toolbar` to the application runtime. To use it, set the `DJANGO_SETTINGS_MODULE` environment variable to `ProjectTime.config.settings-debug`, then run the following command:

```
anaconda-project run --env-spec application-debug manage.py runserver
```

## Packaging

* For PyPi: `anaconda-project run setup.py sdist bdist_wheel`
* For Conda: `anaconda-project run conda build conda-recipe`
