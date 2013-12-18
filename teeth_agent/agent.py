"""
Copyright 2013 Rackspace, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from collections import OrderedDict
import time

import pkg_resources
from teeth_rest import encoding
from werkzeug import serving

from teeth_agent import api


class TeethAgentOperationModes(object):
    DECOM = 'DECOM'
    STANDBY = 'STANDBY'

    @classmethod
    def validate_mode(cls, mode):
        if not hasattr(cls, mode) or getattr(cls, mode) != mode:
            raise RuntimeError('Invalid mode: {}'.format(mode))


class TeethAgentStatus(encoding.Serializable):
    def __init__(self, mode, started_at, version):
        self.mode = mode
        self.started_at = started_at
        self.version = version

    def serialize(self, view):
        """
        Turn the status into a dict.
        """
        return OrderedDict([
            ('mode', self.mode),
            ('started_at', self.started_at),
            ('version', self.version),
        ])


class TeethAgent(object):
    def __init__(self, listen_host, listen_port, mode):
        TeethAgentOperationModes.validate_mode(mode)
        self.listen_host = listen_host
        self.listen_port = listen_port
        self.started_at = None
        self.mode = mode
        self.api = api.TeethAgentAPIServer(self)

    def get_status(self):
        """
        Retrieve a serializable status.
        """
        return TeethAgentStatus(
            mode=self.mode,
            started_at=self.started_at,
            version=pkg_resources.get_distribution('teeth-agent').version
        )

    def execute_command(self, command):
        """
        Execute an agent command.
        """
        pass

    def run(self):
        """
        Run the Teeth Agent.
        """
        if self.started_at:
            raise RuntimeError('Agent was already started')

        self.started_at = time.time()
        serving.run_simple(self.listen_host, self.listen_port, self.api)
