import sys
import json

class JSONReader(object):
	
	def __init__(self):
		with open('syncConfig.json', 'r') as f:
			self.config = json.loads(f.read())
	
	def getExcludeFilesAsString(self):
		return ' '.join(self.config["exclude"])
		
	def getLocalSharedFolder(self):
		return self.config["sharedDirs"]["local"]
		
	def getGlobalSharedFolder(self):
		return self.config["sharedDirs"]["global"]
		
	def getPythonFreeze(self):
		return self.config["freezePythonDeps"]
		
#helper = SyncHelper()
#print(helper.config["locationShared"])
#print(helper.getLocalSharedFolder())
#print(helper.getGlobalSharedFolder())
#print(helper.getExcludeFilesAsString())
