#
# Copyright 2024 BetterWithData
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
#

from __future__ import absolute_import

from jupyter_server import serverapp as server_app
from notebook import notebookapp as notebook_app


import urllib
import json
import os
import ipykernel
import pathlib


def get_current_dir() -> str:
    """Returns the current working directory in jupyter server
    NOTE: works only when the security is token-based or there is also no password
    """
    try:
        connection_file = os.path.basename(ipykernel.get_connection_file())  # type: ignore
        if not connection_file:
            return os.getcwd()

        kernel_id = connection_file.split('-', 1)[1].split('.')[0]

        # Try server_app first (Jupyter Server)
        for srv in server_app.list_running_servers():  # type: ignore
            try:
                if srv['token'] == '' and not srv['password']:  # No token and no password
                    req = urllib.request.urlopen(srv['url']+'api/sessions')
                else:
                    req = urllib.request.urlopen(srv['url']+'api/sessions?token='+srv['token'])

                sessions = json.load(req)
                for sess in sessions:
                    if sess['kernel']['id'] == kernel_id:
                        notebook_path = pathlib.Path(sess['notebook']['path'])
                        return str(notebook_path.parents[0])
            except Exception:
                continue  # Try next server or fall through to notebook_app

        # Fall back to notebook_app (Jupyter Notebook)
        for srv in notebook_app.list_running_servers():  # type: ignore
            try:
                if srv['token'] == '' and not srv['password']:  # No token and no password
                    req = urllib.request.urlopen(srv['url']+'api/sessions')
                else:
                    req = urllib.request.urlopen(srv['url']+'api/sessions?token='+srv['token'])

                sessions = json.load(req)
                for sess in sessions:
                    if sess['kernel']['id'] == kernel_id:
                        notebook_path = pathlib.Path(sess['notebook']['path'])
                        return str(notebook_path.parents[0])
            except Exception:
                continue  # Try next server

    except Exception:
        pass  # Fall through to returning current directory

    return os.getcwd()
