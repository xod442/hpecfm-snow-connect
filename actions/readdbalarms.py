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
import json
from lib.actions import HpecfmAlarmsBaseAction


class readDb(HpecfmAlarmsBaseAction):
    def run(self):

        mydb = self.client["app_db"]
        process = mydb["processalarms"]
        known = mydb['knownalarms']

        # read all the records from process alarms
        alarms = process.find()

        alarms_out = []
        # make a new dict to remove ObjectID from mongo records (process dict)
        pd = {}

        for alarm in alarms:
            pd['u_eventType'] = alarm['u_eventType']
            pd['u_typex'] = alarm['u_typex']
            pd['u_uuid'] = alarm['u_uuid']
            pd['u_sev'] = alarm['u_sev']
            pd['u_desc'] = alarm['u_desc']

            # convert pd dict to a string for servicenow action
            item = json.dumps(pd)
            alarms_out.append(item)

            # Update records to have the snowack set to yes
            myquery = {"u_snowack" : "no"}
            newvalues = { "$set" : { "u_snowack": "yes"} }

            known.update_one(myquery, newvalues)

        # Clean out the process alarms collection
        process.drop()

        return (alarms_out)
