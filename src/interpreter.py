# coding=utf-8
# Copyright 2018-2022 EVA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from cmd import Cmd
from contextlib import ExitStack

from src.db_api import connect


class EvaCommandInterpreter(Cmd):
    def __init__(self):
        super().__init__()

    def set_connection(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()

    def emptyline(self):
        print("Enter a valid query.")
        return False

    def do_quit(self, args):
        """Quits the program."""
        return True

    def do_exit(self, args):
        """Quits the program."""
        return True

    def default(self, line):
        """Considers the input as a query"""
        return self.do_query(line)

    def do_query(self, query):
        """Takes in SQL query and generates the output"""

        self.cursor.execute(query)
        print(self.cursor.fetch_all())

        return False


def handle_user_input(connection):
    """
        Reads from stdin in separate thread

        If user inputs 'quit' stops the event loop
        otherwise just echoes user input
    """

    # Start command interpreter
    prompt = EvaCommandInterpreter()
    prompt.prompt = "$ "

    prompt.set_connection(connection)

    prompt.cmdloop("Welcome to EVA Server")


def start_cmd_client(host: str, port: int):
    """
    Starts the command line client
    """

    with ExitStack() as stack:
        connection = connect(host, port)
        handle_user_input(connection)
