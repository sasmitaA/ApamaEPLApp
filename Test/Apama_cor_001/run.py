# Sample PySys testcase
# Copyright (c) 2015-2016, 2018-2019 Software AG, Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA, and/or its subsidiaries and/or its affiliates and/or their licensors. 
# Use, reproduction, transfer, publication or disclosure is prohibited except as specifically provided for in your License Agreement with Software AG 

from pysys.constants import *
from apama.basetest import ApamaBaseTest
from apama.correlator import CorrelatorHelper

class PySysTest(ApamaBaseTest):

	def execute(self):
		# create the correlator helper, start the correlator and attach an 
		# engine_receive process listening to a test channel. The helper will 
		# automatically get an available port that will be used for all 
		# operations against it
		correlator = CorrelatorHelper(self, name='testcorrelator')
		self.project.APAMA_WORK = self.input+'/../../../EPLApp'
		correlator.start(logfile='testcorrelator.log',config=[os.path.join(self.project.APAMA_WORK,'initialization.yaml')])
		receiveProcess = correlator.receive(filename='receive.evt', channels=['EchoChannel'], logChannels=True)
		correlator.applicationEventLogging(enable=True)
		
		# not strictly necessary in this testcase, but a useful example of waiting 
		# for a log message
		self.waitForSignal('testcorrelator.log', expr="Done processing external event: Pressure\(\"S003\",700\), qlen = 1", 
			process=correlator.process, errorExpr=[' (ERROR|FATAL) .*'])
		
			
		# wait for all events to be processed
		correlator.flush()

		
	def validate(self):
		# look for log statements in the correlator log file
		self.assertGrep('testcorrelator.log', expr=' (ERROR|FATAL) .*', contains=False)
		
		
		# check the received events against the reference
		self.assertDiff('testcorrelator.out', 'ref_testcorrelator.out')
		