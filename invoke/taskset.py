from invoke import Context
from invoke.tasks import task
from invoke.collection import Collection
from fabric2.connection import Connection
from contextlib import contextmanager
from invoke.config import Config

host = "192.168.8.182"
user = "bar"

class CliConnection(Connection):
    """
    Class used for establising SSH Connection. Inherits fabric2s'
    Connection class.
    """

    def __init__(self, host, user):
        super(CliConnection, self).__init__(host=host, user=user)

        command_user = list()
        self._set(command_user=command_user)

    @contextmanager
    def update_config(self, user):
        """
        Updates username in current config.
        """
        # Close connection if it is not closed, or the username will remain
        # unchanged
        if self.is_connected == True:
            self.close()

        self.command_user.append(self.user)
        self.user = user

        try:
            yield
        finally:
            self.command_user.pop()
            self.close() # is this needed?

# create SSH connection
context = CliConnection(host=host,user=user)

class Taskset(object):
    """
    NOTE: This should be added to the repo
    """
    def __init__(self, context):
        self.context = context

    def run(self, cmd, echo=True, **kwargs):
        self.context.run(cmd, echo=echo, **kwargs)

class CliTaskset(Taskset):
    """
    Example usage of Taskset.
    """
    @task
    def which_user(self): # example usage of update_config()
        self.run("whoami")
        with self.context.update_config(user="root"):
            self.run("whoami")
        with self.context.update_config(user="bar"):
            self.run("whoami")

ns = Collection()
ns.add_collection(Collection.from_class(CliTaskset(context)), name="clitaskset")
