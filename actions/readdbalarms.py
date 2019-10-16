# (C) Copyright 2019 Hewlett Packard Enterprise Development LP.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#  http://www.apache.org/licenses/LICENSE-2.0.

# Unless required by applicable law. or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# __author__ = "@netwookie"
# __credits__ = ["Rick Kauffman"]
# __license__ = "Apache2.0"
# __maintainer__ = "Rick Kauffman"
# __email__ = "rick.a.kauffman@hpe.com"

# A python script for getting a dictionary of switches

import pymongo
from lib.actions import HpecfmAlarmsBaseAction


class readDb(HpecfmAlarmsBaseAction):
    def run(self, alarms):

        mydb = self.client["app_db"]
        process = mydb["processalarms"]

        # read all the records from process alarms
        alarms = process.find()

        alarms_out = []

        for alarm in alarms:
            alarms_out.append(alarm)

        # Clean out the process alarms collection
        process.drop()
        
        return (alarms_out)
