import os
import signal
import subprocess
import sys
from robot.api.deco import keyword


class ProjectTimeLibrary:
    def __init__(self):
        self.path = os.path.join(os.path.dirname(__file__),
                                 '..',
                                 '..',
                                 'src',
                                 'ProjectTime')
        self.test_server_pid = None

    @keyword('Start Test Server On Port "${port}" With Data "${fixtures}"')
    def start_test_server_with_data(self, port=8000, fixtures=''):
        self.test_server_pid = subprocess.Popen(
            [
                sys.executable,
                'manage.py',
                'testserver',
                '--addrport',
                str(port),
                '--noinput',
                ' '.join([
                    '../test/fixtures/' + fixture_name
                    for fixture_name in fixtures.split(' ')
                ])
            ],
            cwd=self.path,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        ).pid

    def stop_test_server(self):
        os.kill(self.test_server_pid, signal.SIGKILL)
