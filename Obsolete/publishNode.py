import os
import json
from datetime import datetime, timezone

from .envHandler import PUBLISH_FILE, is_publish_file

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
		"""Log default metadata structure"""
		return {
			PublishLogKeys.VERSION: int(1),
			PublishLogKeys.VARIANT: str(),
			PublishLogKeys.USER: str(),
			PublishLogKeys.WORKFILES: list(),
			PublishLogKeys.PUBLISHFILES: list(),
			PublishLogKeys.RECORD: float(datetime.now(timezone.utc).timestamp()),
			PublishLogKeys.APP:str(),
			PublishLogKeys.DESCRIPTION:str()
		}.copy()

	def get_Version(self):
		"""Get the the log version.

			Returns: log version.
			Return Type: str
		"""
		return self._data[PublishLogKeys.VERSION]
	def set_Version(self, Version=int()):
		"""Set the the log version.

			Parameters:
			Version (int) - Version number.
		"""
		self._data[PublishLogKeys.VERSION] = Version

	def get_Variant(self):
		"""Get the name of the variant.

			Returns: Variant name.
			Return Type: str
		"""
		return self._data[PublishLogKeys.VARIANT]
	def set_Variant(self, Variant=str()):
		"""Set the the log variant.

			Parameters:
			Variant (str) - Variant name.
		"""
		self._data[PublishLogKeys.VARIANT] = Variant

	def get_User(self):
		"""Get the name of user that created the log.

			Returns: Name of user.
			Return Type: str
		"""
		return self._data[PublishLogKeys.USER]
	def set_User(self, User=str()):
		"""Set the user name that creating the log.

			Parameters:
			User (str) - User name.
		"""
		self._data[PublishLogKeys.USER] = User

	def get_WorkFiles(self):
		"""Get the list of work files.

			Returns: Work files.
			Return Type: list
		"""
		return self._data[PublishLogKeys.WORKFILES]
	def set_WorkFiles(self, WorkFiles=list()):
		"""Set the list of user's workfiles.

			Parameters:
			WorkFiles (list) - User's workfiles.
		"""
		self._data[PublishLogKeys.WORKFILES] = WorkFiles

	def get_PublishFiles(self):
		"""Get the list of publish files.

			Returns: Published files.
			Return Type: list
		"""
		return self._data[PublishLogKeys.PUBLISHFILES]
	def set_PublishFiles(self, PublishFiles=list()):
		"""Set the list of published files.

			Parameters:
			PublishFiles (list) - published files.
		"""
		self._data[PublishLogKeys.PUBLISHFILES] = PublishFiles

	def get_Record(self, asObject=bool(False)):
		"""Get the recorded log.

			To get the date e.g. get_Record(asObject=True).date()
			To get the Time e.g. get_Record(asObject=True).time()

			Returns: Record date and time in UTC.
			Return Type: float
		"""
		if asObject:
			return datetime.fromtimestamp(self.get_Record(), tz=timezone.utc)
		else:
			return self._data[PublishLogKeys.RECORD]
	def set_Record(self, Record=float()):
		"""Set the log created date and time in UTC.

			e.g. datetime.datetime.now(timezone.utc).timestamp()

			Parameters:
			Record (float) - Date and time timestamp.
		"""
		self._data[PublishLogKeys.RECORD] = Record

	def get_Application(self):
		"""Get the name of the application that created the log.

			Returns: Application name.
			Return Type: str
		"""
		return self._data[PublishLogKeys.APP]
	def set_Application(self, Application=str()):
		"""Set the name of application that creating the log.

			Parameters:
			Application (str) - Name of application.
		"""
		self._data[PublishLogKeys.APP] = Application

	def get_Description(self):
		"""Get log description.

			Returns: description of publish.
			Return Type: str
		"""
		return self._data[PublishLogKeys.DESCRIPTION]
	def set_Description(self, Description=str()):
		"""Set the description of the log.

			Parameters:
			Description (str) - Log's Description.
		"""
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
				 AssetSpace=str(), AssetName=str()):
		self._publish = self.PUBLISH_METADATA()
		self._version = self._publish[PublishFileKeys.VERSION]
		if is_publish_file(filePath=PublishFile):
			self.load(PublishFile=PublishFile)
		else:
			if isinstance(AssetType, str) and AssetType : self.set_AssetType(assetType=AssetType)
			if isinstance(AssetContainer, str) and AssetContainer : self.set_AssetContainer(assetContainer=AssetContainer)
			if isinstance(AssetSpace, str) and AssetSpace : self.set_AssetSpace(assetSpace=AssetSpace)
			if isinstance(AssetName, str) and AssetName : self.set_AssetName(assetName=AssetName)

	@staticmethod
	def PUBLISH_METADATA():
		"""File Metadata structure"""
		return {
			PublishFileKeys.VERSION:"1.0",
			PublishFileKeys.ASSET_TYPE:str(),
			PublishFileKeys.ASSET_CONTAINER:str(),
			PublishFileKeys.ASSET_SPACE:str(),
			PublishFileKeys.ASSET_NAME:str(),
			PublishFileKeys.LOGS:dict()
		}.copy()

	def get_AssetType(self):
		"""Get the AssetType

			Returns: Asset type
			Return Type: str
		"""
		return self._publish[PublishFileKeys.ASSET_TYPE]
	def set_AssetType(self, assetType=str):
		"""Set the AssetType

			Parameters:
			assetType (str) - Asset type.
		"""
		self._publish[PublishFileKeys.ASSET_TYPE] = assetType

	def get_AssetContainer(self):
		"""Get the AssetContainer

			Returns: Asset container
			Return Type: str
		"""
		return self._publish[PublishFileKeys.ASSET_CONTAINER]
	def set_AssetContainer(self, assetContainer=str):
		"""Set the AssetContainer

			Parameters:
			assetContainer (str) - Asset container.
		"""
		self._publish[PublishFileKeys.ASSET_CONTAINER] = assetContainer

	def get_AssetSpace(self):
		"""Get the AssetSpace

			Returns: Asset space
			Return Type: str
		"""
		return self._publish[PublishFileKeys.ASSET_SPACE]
	def set_AssetSpace(self, assetSpace=str):
		"""Set the AssetSpace

			Parameters:
			assetSpace (str) - Asset space.
		"""
		self._publish[PublishFileKeys.ASSET_SPACE] = assetSpace

	def get_AssetName(self):
		"""Get the AssetName

			Returns: Asset name
			Return Type: str
		"""
		return self._publish[PublishFileKeys.ASSET_NAME]
	def set_AssetName(self, assetName=str):
		"""Set the AssetName

			Parameters:
			assetName (str) - Asset name.
		"""
		self._publish[PublishFileKeys.ASSET_NAME] = assetName

	def get_version(self):
		"""Get PublishObject version

			Returns: version
			Return Type: str
		"""
		return tuple(self._version.split("."))

	def get_variants(self):
		"""Get list of variants.

			Returns: List of variants.
			Return Type: tuple
		"""
		items = list(self._publish[PublishFileKeys.LOGS].keys())
		items.sort()
		return tuple(items)
	def has_variant(self, variant=str):
		"""Check if the variant exists.

			Parameters:
			variant (str) - Name of the variant.

			Returns: True if valid otherwise False.
			Return Type: bool
		"""
		return variant in self._publish[PublishFileKeys.LOGS].keys()
	def add_variant_log(self, variant=str, logNode=LogObject):
		"""Add a new log to variant

			Parameters:
			variant (str) - Name of the variant.
			logNode (LogObject) - LogObject node.

			Returns: True if it was successful otherwise False
			Return Type: bool
		"""
		if isinstance(logNode, LogObject):
			self.create_variant(variant=variant)
			nextVersion = self.get_variant_version(variant=variant) + 1
			logNode.set_Version(Version=nextVersion)
			self._publish[PublishFileKeys.LOGS][variant].append(logNode)
			return True
		return False
	def get_variant_logs(self, variant=str, asObject=bool(False)):
		"""Check if the variant exists.

			Parameters:
			variant (str) - Name of the variant.
			asObject (bool) - get the return type as LogObjects or JSON.

			Returns: list of logs.
			Return Type: list
		"""
		if asObject:
			return self._publish[PublishFileKeys.LOGS][variant]
		else:
			return [a.toJSON() for a in self._publish[PublishFileKeys.LOGS][variant]]
	def get_variant_version(self, variant=str):
		"""Get the version of Variant.

			Parameters:
			variant (str) - Name of the variant.
			asObject (bool) - get the return type as LogObjects or JSON.

			Returns: list of logs.
			Return Type: list
		"""
		if self.has_variant(variant=variant):
			return len(self._publish[PublishFileKeys.LOGS][variant])
		return 0
	def create_variant(self, variant=str):
		"""Create a new variant.

			Parameters:
			variant (str) - Name of the variant.
		"""
		if variant not in self._publish[PublishFileKeys.LOGS]:
			self._publish[PublishFileKeys.LOGS][variant] = list()
	def remove_variant(self, variant=str):
		"""Remove an existing variant.

			Parameters:
			variant (str) - Name of the variant.
		"""
		if variant in self._publish[PublishFileKeys.LOGS]:
			del self._publish[PublishFileKeys.LOGS][variant]

	def get_logs(self, asObject=bool(False)):
		"""Get all logs

			Returns: list of logs
			Return Type: list
		"""
		logs = list()
		for variant in self.get_variants():
			logs.extend(self.get_variant_logs(variant=variant, asObject=asObject))
		return logs

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
				json.dump(self.toJSON(), outfile, ensure_ascii=False, indent=4)

	def load(self, PublishFile=str):
		"""Load publish file.

			Parameters:
			PublishFile (str) - Path to publish file.
		"""
		if PublishFile:
			if os.path.isfile(PublishFile):
				PublishFile = os.path.dirname(PublishFile)
			# add extension
			file_path = os.path.join(PublishFile,PUBLISH_FILE)
			if os.path.exists(file_path):
				with open(file_path, 'r') as outfile:
					LoadedData = json.load(outfile)
					if PublishFileKeys.VERSION in LoadedData:
						self._version = LoadedData[PublishFileKeys.VERSION]
						if LoadedData[PublishFileKeys.VERSION] == "1.0":
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
		"""Serialized the object into dictionary.

			Returns: get a dictionary of PublishObject.
			Returns Types: dict
		"""
		nData = self._publish.copy()
		nData[PublishFileKeys.LOGS] = {}
		for variant in self.get_variants():
			nData[PublishFileKeys.LOGS][variant] = self.get_variant_logs(variant=variant, asObject=False)
		return nData