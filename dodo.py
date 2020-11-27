import os

from doit.action import CmdAction
from doit.tools import LongRunning, Interactive
from pathlib import Path

DOIT_CONFIG = {
    'default_tasks': ['build']
}

# Paths

cwd = Path(os.getcwd())
project_file = Path(cwd / 'anaconda-project.yml')

database_env_dir = Path(cwd / 'envs' / 'database')
application_env_dir = Path(cwd / 'envs' / 'application')
unit_test_env_dir = Path(cwd / 'envs' / 'test')
acceptance_test_env_dir = Path(cwd / 'envs' / 'test-acceptance')
lint_env_dir = Path(cwd / 'envs' / 'lint')
source_code_dir = Path(cwd / 'src' / 'ProjectTime')
database_dir = Path(cwd / 'db')
acceptance_tests_dir = Path(cwd / 'test')
acceptance_test_suites_dir = Path(acceptance_tests_dir / 'suites')

database_executable = Path(database_env_dir / 'bin' / 'pg_ctl')
app_executable = Path(application_env_dir / 'bin' / 'python')
unit_test_executable = Path(unit_test_env_dir / 'bin' / 'python')
acceptance_test_executable = Path(acceptance_test_env_dir / 'bin' / 'robot')
lint_executable = Path(lint_env_dir / 'bin' / 'python')

postgres_config_file = Path(database_dir / 'postgresql.conf')
postgres_pid_file = Path(database_dir / 'postmaster.pid')
python_source_files = source_code_dir.glob('**/*.py')
test_fixture_file = Path(acceptance_tests_dir / 'fixtures' / 'admin_user.json')

# Command string builders

prepare_env = ['anaconda-project', 'prepare', '--env-spec']
run_command = ['anaconda-project', 'run']
clean = ['rm', '-r']

def task_prepare_db_env():
    """ Install database dependencies
    """
    return {
        'file_dep': [project_file],
        'actions': [[*prepare_env, 'database']],
        'targets': [database_executable],
        'clean': [[*clean, str(database_env_dir)]]
    }

def task_prepare_app_env():
    """ Install application dependencies
    """
    return {
        'file_dep': [project_file],
        'actions': [[*prepare_env, 'application']],
        'targets': [app_executable],
        'clean': [[*clean, str(application_env_dir)]],
    }

def task_prepare_unit_test_env():
    """ Install test dependencies
    """
    return {
        'file_dep': [project_file],
        'actions': [[*prepare_env, 'test']],
        'targets': [unit_test_executable],
        'clean': [[*clean, str(unit_test_env_dir)]],
    }

def task_prepare_acceptance_test_env():
    """ Install acceptance test dependencies
    """
    return {
        'file_dep': [project_file],
        'actions': [[*prepare_env, 'test-acceptance']],
        'targets': [acceptance_test_executable],
        'clean': [[*clean, str(acceptance_test_env_dir)]],
    }

def task_prepare_lint_env():
    """ Install dependencies for tidying code
    """
    return {
        'file_dep': [project_file],
        'actions': [[*prepare_env, 'lint']],
        'targets': [lint_executable],
        'clean': [[*clean, str(lint_env_dir)]],
    }

def task_initdb():
    """ Create the PostgreSQL database
    """
    return {
        'file_dep': [database_executable],
        'actions': [[*run_command, 'pg_ctl', 'initdb']],
        'targets': [postgres_config_file],
        'clean': [[*clean, str(database_dir)]],
    }

def task_startdb():
    """ Start the PostgreSQL database
    """
    return {
        'file_dep': [postgres_config_file],
        'actions': [LongRunning(' '.join([*run_command, 'pg_ctl', 'start']))],
        'targets': [postgres_pid_file],
    }

def task_migrate():
    """ Prepare the application for execution
    """
    return {
        'file_dep': [
            app_executable,
            postgres_pid_file,
            *python_source_files,
        ],
        'actions': [
            [*run_command, 'manage.py', 'migrate'],
            [*run_command, 'pg_ctl', 'stop'],
        ],
    }

def task_serve():
    """ Execute the app
    """
    return {
        'file_dep': [
            app_executable,
            postgres_pid_file,
        ],
        'actions': [
            [*run_command, 'manage.py', 'migrate'],
            LongRunning(' '.join([*run_command, 'manage.py', 'runserver'])),
            [*run_command, 'pg_ctl', 'stop'],
        ]
    }

def task_testserver():
    """ Execute the app with a test database
    """
    return {
        'file_dep': [
            app_executable,
            postgres_pid_file,
        ],
        'actions': [
            LongRunning(' '.join([
                *run_command,
                'manage.py',
                'testserver',
                '--noinput',
                str(test_fixture_file)
            ])),
            [*run_command, 'pg_ctl', 'stop'],
        ],
    }

def task_test_unit():
    """ Execute the application unit tests
    """
    return {
        'file_dep': [
            unit_test_executable,
            postgres_pid_file,
        ],
        'actions': [
            Interactive(' '.join([*run_command, 'coverage', 'run', 'manage.py', 'test', '--noinput'])),
            [*run_command, 'pg_ctl', 'stop'],
            [*run_command, 'coverage', 'report'],
        ]
    }

def task_test_smoke():
    """ Execute the acceptance smoke tests (start testserver in a separate process first)
    """
    return {
        'file_dep': [
            acceptance_test_executable,
        ],
        'actions': [
            Interactive(' '.join([
                *run_command,
                'robot',
                '-d',
                'test_report_smoke_tests',
                '-v',
                'headlessfirefox',
                str(acceptance_test_suites_dir / 'smoke_tests.robot')
            ])),
        ]
    }

def task_test_workflow():
    """ Execute the acceptance workflow tests (start testserver in a separate process first)
    """
    return {
        'file_dep': [
            acceptance_test_executable,
        ],
        'actions': [
            Interactive(' '.join([
                *run_command,
                'robot',
                '-d',
                'test_report_workflow_tests',
                '-v',
                'headlessfirefox',
                str(acceptance_test_suites_dir / 'workflow_tests.robot')
            ])),
        ]
    }

def task_tidy():
    """ Tidy code
    """
    return {
        'uptodate': [False],
        'file_dep': [
            lint_executable,
            acceptance_test_executable,
        ],
        'actions': [
            [*run_command, 'isort', str(source_code_dir)],
            [*run_command, 'autopep8', '-r', '-i', '--max-line-length', '88', str(source_code_dir)],
            [*run_command, 'robot.tidy', '-r', 'test'],
        ]
    }

def task_check():
    """ Lint code
    """
    return {
        'uptodate': [False],
        'file_dep': [
            lint_executable,
            app_executable
        ],
        'actions': [
            ['python', '-m', 'scripts.dev_install'],
            Interactive(' '.join([
                *run_command,
                'pylint',
                '--fail-under',
                '8',
                str(source_code_dir)
            ])),
            Interactive(' '.join([
                *run_command,
                'manage.py',
                'check'
            ])),
        ]
    }