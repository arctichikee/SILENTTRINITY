import asyncio
import logging
from terminaltables import SingleTable
from core.client.utils import command, register_cli_commands

@register_cli_commands
class Listeners:
    name = 'listeners'
    description = 'Listeners menu'

    _remote = True

    def __init__(self):
        self.prompt = None
        self._selected = None
    
    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, data):
        self.prompt = f"(<ansired>{data['name']}</ansired>)"
        self._selected = data

    @command
    def use(self, name: str, response):
        """
        Select the specified listener

        Usage: use <name> [-h]

        Arguments:
            name  filter by listener name
        """

        self.selected = response.result

    @command
    def list(self, name: str, running: bool, available: bool, response):
        """
        Get running/available listeners

        Usage: list [-h] [(--running | --available)] [<name>]

        Arguments:
            name  filter by listener name

        Options:
            -h, --help       Show dis
            -r, --running    List running listeners  [default: True]
            -a, --available  List available listeners
        """

        listeners = response.result
        if available:
            table_title = "Available"
            table_data = [["Name", "Description"]]

            for name,fields in listeners.items():
                table_data.append([name, fields["description"]])

        else:
            table_title = 'Running'
            table_data = [["Name", "URL"]]
            for name,lst in listeners.items():
                table_data.append([
                    lst['options']['Name']['Value'],
                    f"{name}://{lst['options']['BindIP']['Value']}:{lst['options']['Port']['Value']}"
                ])

        table = SingleTable(table_data)
        table.title = table_title
        table.inner_row_border = True
        print(table.table)

    @command
    def options(self, response):
        """
        Show selected listeners options

        Usage: options [-h]
        """

        table_data = [
            ["Option Name", "Required", "Value", "Description"]
        ]

        for k, v in response.result.items():
            table_data.append([k, v["Required"], v["Value"], v["Description"]])

        table = SingleTable(table_data, title="Listener Options")
        table.inner_row_border = True
        print(table.table)

    @command
    def start(self, response):
       """
       Start the selected listener

       Usage: start [-h]
       """
    
    @command
    def stop(self, response):
        """
        Stop the selected listener

        Usage: stop <name> [-h]
        """

    @command
    def set(self, name: str, value: str, response):
        """
        Set options on the selected listener

        Usage: set <name> <value> [-h]

        Arguments:
            name   option name
            value  option value
        """

    @command
    def reload(self, response):
        """
        Reload all listeners

        Usage: reload [-h]
        """
