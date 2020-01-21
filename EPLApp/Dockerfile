# Copyright (c) 2018 Software AG, Darmstadt, Germany and/or its licensors
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this 
# file except in compliance with the License. You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the
# License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, 
# either express or implied. 
# See the License for the specific language governing permissions and limitations under the License.

ARG APAMA_VERSION=10.5
ARG APAMA_BUILDER=store/softwareag/apama-builder:${APAMA_VERSION}
ARG APAMA_IMAGE=store/softwareag/apama-correlator:${APAMA_VERSION}

# Use the build environment
FROM ${APAMA_BUILDER} as builder


#build steps, tests, and deployment
RUN ant
RUN cd tests && pysys run
RUN engine_deploy
 
#create the working application image
FROM ${APAMA_IMAGE}
COPY --from=builder ${APAMA_WORK}/deployed ${APAMA_WORK}/deployed
 
 
#example startup command
CMD ["correlator", "--config", "deployed"]



