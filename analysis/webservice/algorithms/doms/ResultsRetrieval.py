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

import uuid

from . import BaseDomsHandler
from . import ResultsStorage
from webservice.NexusHandler import nexus_handler
from webservice.webmodel import NexusProcessingException
from webservice.algorithms.doms.insitu import query_insitu_schema


insitu_schema = query_insitu_schema()

@nexus_handler
class DomsResultsRetrievalHandler(BaseDomsHandler.BaseDomsQueryCalcHandler):
    name = "DOMS Resultset Retrieval"
    path = "/domsresults"
    description = ""
    params = {}
    singleton = True

    def __init__(self, tile_service_factory, config=None):
        BaseDomsHandler.BaseDomsQueryCalcHandler.__init__(self, tile_service_factory)
        self.config = config

    def calc(self, computeOptions, **args):
        from webservice.algorithms_spark.Matchup import get_insitu_params

        execution_id = computeOptions.get_argument("id", None)

        caml_params = {}

        output_type = computeOptions.get_argument("output", default='JSON')

        if output_type == 'CAML':
            primary = computeOptions.get_argument("camlPrimary")
            if primary is None:
                raise NexusProcessingException(
                    reason="Primary dataset argument is required when outputting in CAML format", code=400)

            secondary = computeOptions.get_argument("camlSecondary")
            if secondary is None:
                raise NexusProcessingException(
                    reason="Secondary dataset argument is required when outputting in CAML format", code=400)

            insitu_params = get_insitu_params(insitu_schema)

            if secondary not in insitu_params:
                raise NexusProcessingException(
                    reason=f"Parameter {secondary} not supported. Must be one of {insitu_params}", code=400)

            CHART_TYPES = [
                'time_series',
                'scatter',
                'histogram_primary',
                'histogram_secondary',
                'trajectory'
            ]

            types_arg = computeOptions.get_argument("camlChartTypes")

            if types_arg is None:
                types = {
                    'time_series': False,
                    'scatter': True,
                    'histogram_primary': True,
                    'histogram_secondary': True,
                    'trajectory': True
                }
            else:
                types_arg = types_arg.split(',')

                types = {
                    'time_series': False,
                    'scatter': False,
                    'histogram_primary': False,
                    'histogram_secondary': False,
                    'trajectory': False
                }

                for t in types_arg:
                    if t not in CHART_TYPES:
                        raise NexusProcessingException(
                            reason=f"Invalid chart type argument: {t}",
                            code=400
                        )

                    types[t] = True

            caml_params['primary'] = primary
            caml_params['secondary'] = secondary
            caml_params['charts'] = types

        try:
            execution_id = uuid.UUID(execution_id)
        except:
            raise NexusProcessingException(reason="'id' argument must be a valid uuid", code=400)

        simple_results = computeOptions.get_boolean_arg("simpleResults", default=False)

        with ResultsStorage.ResultsRetrieval(self.config) as storage:
            params, stats, data = storage.retrieveResults(execution_id, trim_data=simple_results)

        if output_type == 'CAML':
            params['caml_params'] = caml_params

        if output_type == 'CAML':
            raise NexusProcessingException(reason='CAML output for results retrieval is not yet implemented.', code=501)

        return BaseDomsHandler.DomsQueryResults(results=data, args=params, details=stats, bounds=None, count=None,
                                                computeOptions=None, executionId=execution_id)
