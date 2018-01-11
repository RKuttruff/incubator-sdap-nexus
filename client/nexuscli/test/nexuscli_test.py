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

import unittest
from datetime import datetime

from shapely.geometry import box

import nexuscli


class TestCli(unittest.TestCase):
    def test_time_series(self):
        ts = nexuscli.time_series(("AVHRR_OI_L4_GHRSST_NCEI", "MEASURES_SLA_JPL_1603"), box(-150, 45, -120, 60),
                                  datetime(2016, 1, 1), datetime(2016, 12, 31))

        self.assertEqual(2, len(ts))

    def test_list(self):
        ds_list = nexuscli.dataset_list()

        print(ds_list)
        self.assertTrue(len(ds_list) > 0)

    def test_daily_difference_average(self):
        ts = nexuscli.daily_difference_average("AVHRR_OI_L4_GHRSST_NCEI", box(-150, 45, -120, 60),
                                               datetime(2013, 1, 1), datetime(2014, 12, 31))

        self.assertEqual(1, len(ts))