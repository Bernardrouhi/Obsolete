import os
import json
from datetime import datetime, timezone

from .envHandler import OB_EXTENSION, is_project_file

PUBLISH_EXTENSION = ".hfpub"
PUBLISH_FILE = f"Asset{PUBLISH_EXTENSION}"

def is_publish_file(filePath=str()):
	"""check the file exists and correct extension.

		Returns: validation of filepath
		Return Type: bool
	"""
	return filePath.lower().endswith(PUBLISH_EXTENSION) and os.path.exists(filePath)

class PublishLogKeys():
	VERSION = "Version"
	VARIANT = "Variant"
	USER = "User"
	WORKFILES = "WorkFiles"
	PUBLISHFILES = "PublishFiles"
	RECORD = "Record"
	APP = "Application"
	DESCRIPTION = "Description"

class PublishFileKeys():
	FILE_VERSION = "HandFree Version"
	VERSION = "Version"
	ASSET_TYPE = "AssetType"
	ASSET_CONTAINER = "AssetContainer"
	ASSET_SPACE = "AssetSpace"
	ASSET_NAME = "AssetName"
	LOGS = "Logs"

class LogObject(object):
	"""Handle Publish Log object"""
	def __init__(self, Version=int(1), Variant=str(), User=str(), WorkFiles=list(), 
				 PublishFiles=list(), Application=str(), Record=float(), Description=str()):
		self._data = self.LOG_METADATA()
		if isinstance(Version, int) and Version : self.set_Version(Version=Version)
		if isinstance(Variant, str) and Variant : self.set_Variant(Variant=Variant)
		if isinstance(User, str) and User : self.set_User(User=User)
		if isinstance(WorkFiles, (list, tuple)) and WorkFiles : self.set_WorkFiles(WorkFiles=WorkFiles)
		if isinstance(PublishFiles, (list, tuple)) and PublishFiles : self.set_PublishFiles(PublishFiles=PublishFiles)
		if isinstance(Application, str) and Application : self.set_Application(Application=Application)
		if isinstance(Record, float) and Record : self.set_Record(Record=Record)
		if isinstance(Description, str) and Description : self.set_Description(Description=Description)

	@staticmethod
	def LOG_METADATA():
		"""Node Metadata structure"""
		return {
			PublishLogKeys.VERSION: int(1),
			PublishLogKeys.VARIANT: str(),
			PublishLogKeys.USER: str(),
			PublishLogKeys.WORKFILES: list(),
			PublishLogKeys.PUBLISHFILES: list(),
			PublishLogKeys.RECORD: str(),
			PublishLogKeys.APP:str(),
			PublishLogKeys.DESCRIPTION:str()
		}.copy()

	def get_Version(self):
		return self._data[PublishLogKeys.VERSION]
	def set_Version(self, Version=int()):
		self._data[PublishLogKeys.VERSION] = Version

	def get_Variant(self):
		return self._data[PublishLogKeys.VARIANT]
	def set_Variant(self, Variant=str()):
		self._data[PublishLogKeys.VARIANT] = Variant

	def get_User(self):
		return self._data[PublishLogKeys.USER]
	def set_User(self, User=str()):
		self._data[PublishLogKeys.USER] = User

	def get_WorkFiles(self):
		return self._data[PublishLogKeys.WORKFILES]
	def set_WorkFiles(self, WorkFiles=list()):
		self._data[PublishLogKeys.WORKFILES] = WorkFiles

	def get_PublishFiles(self):
		return self._data[PublishLogKeys.PUBLISHFILES]
	def set_PublishFiles(self, PublishFiles=list()):
		self._data[PublishLogKeys.PUBLISHFILES] = PublishFiles

	def get_Record(self):
		return self._data[PublishLogKeys.RECORD]
	def set_Record(self, Record=float()):
		self._data[PublishLogKeys.RECORD] = Record

	def get_Application(self):
		return self._data[PublishLogKeys.APP]
	def set_Application(self, Application=str()):
		self._data[PublishLogKeys.APP] = Application

	def get_Description(self):
		return self._data[PublishLogKeys.DESCRIPTION]
	def set_Description(self, Description=str()):
		self._data[PublishLogKeys.DESCRIPTION] = Description

	def toJSON(self):
		"""Serialized the object into dictionary.

			Returns: get a dictionary of LogObject.
			Returns Types: dict
		"""
		return self._data

class PublishObject(object):
	"""Handle Publish file"""
	def __init__(self, PublishFile=str(), AssetType=str(), AssetContainer=str(),
				 AssetSpace=str(), AssetName=str(), Logs=dict()):
		self._publish = self.PUBLISH_METADATA()
		if is_publish_file(filePath=PublishFile):
			self.load(PublishFile=PublishFile)
		else:
			if isinstance(AssetType, str) and AssetType : self.set_AssetType(assetType=AssetType)
			if isinstance(AssetContainer, str) and AssetContainer : self.set_AssetContainer(assetContainer=AssetContainer)
			if isinstance(AssetSpace, str) and AssetSpace : self.set_AssetSpace(assetSpace=AssetSpace)
			if isinstance(AssetName, str) and AssetName : self.set_AssetName(assetName=AssetName)
			# if isinstance(Logs, str) and Logs : self.set_AssetSpace(assetSpace=AssetSpace)

	@staticmethod
	def PUBLISH_METADATA():
		"""File Metadata structure"""
		return {
			PublishFileKeys.FILE_VERSION:"2.0",
			PublishFileKeys.VERSION:int(),
			PublishFileKeys.ASSET_TYPE:str(),
			PublishFileKeys.ASSET_CONTAINER:str(),
			PublishFileKeys.ASSET_SPACE:str(),
			PublishFileKeys.ASSET_NAME:str(),
			PublishFileKeys.LOGS:dict()
		}.copy()

	def set_AssetType(self, assetType=str):
		self._publish[PublishFileKeys.ASSET_TYPE] = assetType
	def get_AssetType(self):
		return self._publish[PublishFileKeys.ASSET_TYPE]

	def set_AssetContainer(self, assetContainer=str):
		self._publish[PublishFileKeys.ASSET_CONTAINER] = assetContainer
	def get_AssetContainer(self):
		return self._publish[PublishFileKeys.ASSET_CONTAINER]

	def set_AssetSpace(self, assetSpace=str):
		self._publish[PublishFileKeys.ASSET_SPACE] = assetSpace
	def get_AssetSpace(self):
		return self._publish[PublishFileKeys.ASSET_SPACE]

	def set_AssetName(self, assetName=str):
		self._publish[PublishFileKeys.ASSET_NAME] = assetName
	def get_AssetName(self):
		return self._publish[PublishFileKeys.ASSET_NAME]

	def get_version(self):
		return self._publish[PublishFileKeys.VERSION]

	def set_PublishNode(self, assetType=str, assetContainer=str, assetSpace=str, assetName=str):
		self.set_AssetType(assetType=assetType)
		self.set_AssetContainer(assetContainer=assetContainer)
		self.set_AssetSpace(assetSpace=assetSpace)
		self.set_AssetName(assetName=assetName)

	def create_new_log(self, username=str, variant=str, workfiles=list, publishfiles=list, app=str, description=str):
		newRecord = LogObject.LOG_METADATA()
		# check variant
		self.create_variant(variant=variant)

		nextVersion = self.get_variant_version(variant=variant) + 1
		newRecord[PublishLogKeys.VERSION] = nextVersion
		newRecord[PublishLogKeys.USER] = username
		newRecord[PublishLogKeys.WORKFILES] = workfiles
		newRecord[PublishLogKeys.PUBLISHFILES] = publishfiles
		newRecord[PublishLogKeys.VARIANT] = variant
		newRecord[PublishLogKeys.RECORD] = datetime.now(timezone.utc).timestamp()
		newRecord[PublishLogKeys.APP] = app
		newRecord[PublishLogKeys.DESCRIPTION] = description
		
		self._publish[PublishFileKeys.LOGS][variant].append(newRecord)
		return newRecord

	def get_variants(self):
		items = self._publish[PublishFileKeys.LOGS].keys()
		items.sort()
		return items

	def has_variant(self, variant=str):
		return variant in self._publish[PublishFileKeys.LOGS].keys()

	def get_variant_logs(self, variant=str):
		return self._publish[PublishFileKeys.LOGS][variant]

	def get_variant_version(self, variant=str):
		if self.has_variant(variant=variant):
			return len(self._publish[PublishFileKeys.LOGS][variant])
		return 0

	def create_variant(self, variant=str):
		if variant not in self._publish[PublishFileKeys.LOGS]:
			self._publish[PublishFileKeys.LOGS][variant] = list()

	def get_logs(self):
		logs = list()
		for variant in self._publish[PublishFileKeys.LOGS].keys():
			logs += self._publish[PublishFileKeys.LOGS][variant]
		return logs

	def get_data(self):
		return self._publish.copy()

	def get_date(self, record=float):
		return self.get_record().date()
	def get_time(self, record=float):
		return self.get_record().time()

	def get_record(self):
		return datetime.fromtimestamp(self._publish[PublishLogKeys.RECORD], tz=timezone.utc)

	def save(self, PublishFile=str):
		"""Save Hand Free publish file

			Parameters:
			PublishFile (str) - Path to publish file.
		"""
		if PublishFile:
			if os.path.isfile(PublishFile):
				PublishFile = os.path.dirname(PublishFile)
			PublishFile = os.path.normpath(PublishFile)
			# add extension
			file_path = os.path.join(PublishFile,PUBLISH_FILE)
			# save project file
			with open(file_path, 'w') as outfile:
				json.dump(self._publish, outfile, ensure_ascii=False)

	def load(self, PublishFile=str):
		if PublishFile:
			if os.path.isfile(PublishFile):
				PublishFile = os.path.dirname(PublishFile)
			# add extension
			file_path = os.path.join(PublishFile,PUBLISH_FILE)
			if os.path.exists(file_path):
				with open(file_path, 'r') as outfile:
					LoadedData = json.load(outfile)
					if PublishFileKeys.FILE_VERSION in LoadedData and LoadedData[PublishFileKeys.FILE_VERSION] == "1.0":
						if PublishFileKeys.ASSET_TYPE in LoadedData:
							self.set_AssetType(assetType=LoadedData[PublishFileKeys.ASSET_TYPE])
						if PublishFileKeys.ASSET_CONTAINER in LoadedData:
							self.set_AssetContainer(assetContainer=LoadedData[PublishFileKeys.ASSET_CONTAINER])
						if PublishFileKeys.ASSET_SPACE in LoadedData:
							self.set_AssetSpace(assetSpace=LoadedData[PublishFileKeys.ASSET_SPACE])
						if PublishFileKeys.ASSET_NAME in LoadedData:
							self.set_AssetName(assetName=LoadedData[PublishFileKeys.ASSET_NAME])
						if PublishFileKeys.LOGS in LoadedData:
							self._publish[PublishFileKeys.VERSION] = len(LoadedData[PublishFileKeys.LOGS])
							logs = list()
							for log in LoadedData[PublishFileKeys.LOGS]:
								# adding variant name
								log[PublishLogKeys.VARIANT] = LoadedData[PublishFileKeys.ASSET_NAME]
								logs.append(log)
							self._publish[PublishFileKeys.LOGS][LoadedData[PublishFileKeys.ASSET_NAME]] = logs

					if PublishFileKeys.FILE_VERSION in LoadedData and LoadedData[PublishFileKeys.FILE_VERSION] == "2.0":
						if PublishFileKeys.VERSION in LoadedData:
							self._publish[PublishFileKeys.VERSION] = LoadedData[PublishFileKeys.VERSION]
						if PublishFileKeys.ASSET_TYPE in LoadedData:
							self.set_AssetType(assetType=LoadedData[PublishFileKeys.ASSET_TYPE])
						if PublishFileKeys.ASSET_CONTAINER in LoadedData:
							self.set_AssetContainer(assetContainer=LoadedData[PublishFileKeys.ASSET_CONTAINER])
						if PublishFileKeys.ASSET_SPACE in LoadedData:
							self.set_AssetSpace(assetSpace=LoadedData[PublishFileKeys.ASSET_SPACE])
						if PublishFileKeys.ASSET_NAME in LoadedData:
							self.set_AssetName(assetName=LoadedData[PublishFileKeys.ASSET_NAME])
						if PublishFileKeys.LOGS in LoadedData:
							self._publish[PublishFileKeys.LOGS] = LoadedData[PublishFileKeys.LOGS]

	def toJSON(self):
		return self._publish