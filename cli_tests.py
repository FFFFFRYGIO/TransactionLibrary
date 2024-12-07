import subprocess
import unittest

from ddt import data, unpack, ddt as ddt_decorator


@ddt_decorator
class CliTests(unittest.TestCase):

    def setUp(self):
        """Setup for testing file and script path"""
        self.file_name = 'test_file.txt'
        self.script_path = 'cli_runner.py'

    def run_command(self, subparser: str, request: str, result_type: str, expected_output: str) -> None:
        """Helper method to run a command and return its output"""

        command = f'python {self.script_path} {self.file_name} {subparser} {request} '
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        stdout, stderr = result.stdout.strip(), result.stderr.strip()

        if result_type == 'out':
            self.assertEqual(stderr, '', f'unexpected stderr for command: {command}')
            self.assertEqual(stdout, expected_output, f"failed for command: {command}")
        elif result_type == 'err':
            self.assertEqual(stdout, '', f'unexpected stdout for command: {command}')
            self.assertEqual(stderr, expected_output, f"failed for command: {command}")

    @data(
        ('1000 BOB', 'out', 'transaction added successfully'),
        ('X BOB', 'err',
         'usage: cli_runner.py file add [-h] amount currency\n'
         'cli_runner.py file add: error: argument amount: invalid int value: \'X\''),
        ('1000 X', 'out', 'currency not supported'),
        ('X X', 'err',
         'usage: cli_runner.py file add [-h] amount currency\n'
         'cli_runner.py file add: error: argument amount: invalid int value: \'X\''),
        ('1000 BOB X', 'err',
         'usage: cli_runner.py [-h] file {add,a,get,g,change,c} ...\n'
         'cli_runner.py: error: unrecognized arguments: X'),
    )
    @unpack
    def test_add_commands(self, request: str, result_type: str, expected_output: str) -> None:
        """ test cli commands for add subparser """
        self.run_command('add', request, result_type, expected_output)

    @data(
        ('name', 'out', 'Name'),
        ('surname', 'out', 'Surname'),
        ('patronymic', 'out', 'Patronymic'),
        ('address', 'out', '221B Baker Street'),
        ('counter', 'out', 'missing counter parameter'),
        ('counter --counter 000001', 'out', '000001'),
        ('counter --counter X', 'out', 'could not find transaction with counter X'),
        ('amount', 'out', 'missing counter parameter'),
        ('amount --counter 000001', 'out', '54321'),
        ('amount --counter X', 'out', 'could not find transaction with counter X'),
        ('currency', 'out', 'missing counter parameter'),
        ('currency --counter 000001', 'out', 'PLN'),
        ('currency --counter X', 'out', 'could not find transaction with counter X'),
    )
    @unpack
    def test_get_commands(self, request: str, result_type: str, expected_output: str) -> None:
        """ test cli commands for get subparser """
        self.run_command('get', request, result_type, expected_output)

    @data(
        ('name Name', 'out', 'field \'name\' changed to \'Name\' successfully'),
        ('surname Surname', 'out', 'field \'surname\' changed to \'Surname\' successfully'),
        ('patronymic Patronymic', 'out', 'field \'patronymic\' changed to \'Patronymic\' successfully'),
        ('amount 54321', 'out', 'missing counter parameter'),
        ('amount --counter 000001 54321', 'out',
         'field \'amount\' for counter \'000001\' changed to \'54321\' successfully'),
        ('amount --counter X 54321', 'out', 'counter value X not convertable to int'),
        ('currency', 'err',
         'usage: cli_runner.py file change [-h] [--counter COUNTER]\n                                 '
         '{name,surname,patronymic,address,amount,currency}\n                                 value\n'
         'cli_runner.py file change: error: the following arguments are required: value'),
        ('currency --counter 000001 PLN', 'out',
         'field \'currency\' for counter \'000001\' changed to \'PLN\' successfully'),
        ('currency --counter X', 'err',
         'usage: cli_runner.py file change [-h] [--counter COUNTER]\n                                 '
         '{name,surname,patronymic,address,amount,currency}\n                                 value\n'
         'cli_runner.py file change: error: the following arguments are required: value'),
    )
    @unpack
    def test_change_commands(self, request: str, result_type: str, expected_output: str) -> None:
        """ test cli commands for change subparser """
        self.run_command('change', request, result_type, expected_output)
