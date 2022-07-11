# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from nexustiles.dao.ZarrProxy import ZarrProxy
from nexustiles.nexustiles import NexusTileService

import configparser
import io

import boto3
from moto import mock_s3

import pytest

def setup():
    pass


if __name__ == '__main__':
    cfg = """
    [s3]
    bucket=s3://mur-sst/zarr
    region=us-west-2
    """

    buf = io.StringIO(cfg)
    config = configparser.ConfigParser()
    config.read_file(buf)

    proxy = ZarrProxy(config)



