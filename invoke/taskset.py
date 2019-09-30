from invoke import Context
from invoke.tasks import task
from invoke.collection import Collection
from fabric2.connection import Connection
from contextlib import contextmanager
from invoke.config import Config

host = "192.168.8.182"

class CliConnection(Connection):

    def __init__(self, host, user):
        super(CliConnection, self).__init__(host=host, user=user)
        command_user = list()
        self._set(command_user=command_user)

    @contextmanager
    def update_config(self, user):
        # Update username for easier testing of functions demanding root
        # Close connection if it is not closed, or the username will be
        # unchanged
        if self.is_connected == True:
            self.close()
        # Updates user in config
        # Depends on SSH to already have SSH key configured on remote machine
        # SSH connection closes after contextmanager is finished
        self.command_user.append(self.user)
        self.user = user
        try:
            yield
        finally:
            self.command_user.pop()
            self.close() # not sure if this is needed

context = CliConnection(host=host,user="bar")

class Taskset(object):
    """
    NOTE: This should be added to the repo
    """
    def __init__(self, context):
        self.context = context

    def run(self, cmd, echo=True, **kwargs):
        self.context.run(cmd, echo=echo, **kwargs)

class CliTaskset(Taskset):
    @task
    def which_user(self):
        self.run("whoami") # bar
        with self.context.update_config(user="root"):
            self.run("whoami") # root
        with self.context.update_config(user="bar"):
            self.run("whoami") # bar

ns = Collection()
ns.add_collection(Collection.from_class(CliTaskset(context)), name="clitaskset")
