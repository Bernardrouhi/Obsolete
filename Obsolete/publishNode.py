import os
import json

from .envHandler import PUBLISH_FILE, is_publish_file
from .assetNode import AssetObject, AssetKeys
from .logNode import LogObject

class PublishFileKeys():
	VERSION = "Version"
	LOGS = "Logs"

class PublishObject(AssetObject):
	"""Handle Publish file"""
	__version__ = "1.0"
	def __init__(self, PublishFile=str(), **kwargs):
		AssetObject.__init__(self, **kwargs)
		# Load the file
		if is_publish_file(filePath=PublishFile) : self.load(PublishFile=PublishFile)

	@staticmethod
	def ASSET_METADATA():
		"""File Metadata structure"""
		data = AssetObject.ASSET_METADATA()
		data.update({
			PublishFileKeys.VERSION:PublishObject.__version__,
			PublishFileKeys.LOGS:dict()
			})
		return data.copy()

	def get_version(self):
		"""Get PublishObject version

			Returns: version
			Return Type: str
		"""
		return tuple(self._dataVersion.split("."))

	def get_variants(self):
		"""Get list of variants.

			Returns: List of variants.
			Return Type: tuple
		"""
		items = list(self._data[PublishFileKeys.LOGS].keys())
		items.sort()
		return tuple(items)
	def has_variant(self, variant=str):
		"""Check if the variant exists.

			Parameters:
			variant (str) - Name of the variant.

			Returns: True if valid otherwise False.
			Return Type: bool
		"""
		return variant in self._data[PublishFileKeys.LOGS].keys()
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
			self._data[PublishFileKeys.LOGS][variant].append(logNode)
			return True
		return False
	def get_variant_version(self, variant=str):
		"""Get the version of Variant.

			Parameters:
			variant (str) - Name of the variant.
			asObject (bool) - get the return type as LogObjects or JSON.

			Returns: list of logs.
			Return Type: list
		"""
		if self.has_variant(variant=variant):
			return len(self._data[PublishFileKeys.LOGS][variant])
		return 0
	def create_variant(self, variant=str):
		"""Create a new variant.

			Parameters:
			variant (str) - Name of the variant.
		"""
		if variant not in self._data[PublishFileKeys.LOGS]:
			self._data[PublishFileKeys.LOGS][variant] = list()
	def remove_variant(self, variant=str):
		"""Remove an existing variant.

			Parameters:
			variant (str) - Name of the variant.
		"""
		if variant in self._data[PublishFileKeys.LOGS]:
			del self._data[PublishFileKeys.LOGS][variant]
	def get_variant_logs(self, variant=str, asObject=bool(False)):
		"""get variant's logs.

			Parameters:
			variant (str) - Name of the variant.
			asObject (bool) - get the return type as LogObjects or JSON.

			Returns: list of logs.
			Return Type: list
		"""
		if asObject:
			return self._data[PublishFileKeys.LOGS][variant]
		else:
			return [a.toJSON() for a in self._data[PublishFileKeys.LOGS][variant]]
	def set_variant_logs(self, variant=str, logs=list):
		"""Override variant's logs.

			Parameters:
			variant (str) - Name of the variant.
			logs (list) - list of variant logs (support both dict and LogObject).
		"""
		if not self.has_variant(variant=variant) : self.create_variant(variant=variant)

		nLog = []
		for log in logs:
			if isinstance(log, LogObject) : nLog.append(log)
			if isinstance(log, dict) : nLog.append(LogObject(**log))
		
		self._data[PublishFileKeys.LOGS][variant].append(result)

	def get_logs(self, asObject=bool(False)):
		"""Get all logs

			Returns: list of logs
			Return Type: list
		"""
		logs = list()
		for variant in self.get_variants():
			logs.extend(self.get_variant_logs(variant=variant, asObject=asObject))
		return logs
	def set_logs(self, logs=dict()):
		"""Override all logs

			Parameters:
			logs (dict) - dictionary of variants with list of their logs (support both dict and LogObject).
		"""
		for variant in logs.keys():
			self.set_variant_logs(variant=variant, logs=logs[variant])

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
						self._dataVersion = LoadedData[PublishFileKeys.VERSION]
						if LoadedData[PublishFileKeys.VERSION] == self.__version__:
							if AssetKeys.ASSET_TYPE in LoadedData:
								self.set_AssetType(assetType=LoadedData[AssetKeys.ASSET_TYPE])
							if AssetKeys.ASSET_CONTAINER in LoadedData:
								self.set_AssetContainer(assetContainer=LoadedData[AssetKeys.ASSET_CONTAINER])
							if AssetKeys.ASSET_SPACE in LoadedData:
								self.set_AssetSpace(assetSpace=LoadedData[AssetKeys.ASSET_SPACE])
							if AssetKeys.ASSET_NAME in LoadedData:
								self.set_AssetName(assetName=LoadedData[AssetKeys.ASSET_NAME])
							if PublishFileKeys.LOGS in LoadedData:
								self.set_logs(logs=LoadedData[PublishFileKeys.LOGS])

	def toJSON(self):
		"""Serialized the object into dictionary.

			Returns: get a dictionary of PublishObject.
			Returns Types: dict
		"""
		nData = self._data.copy()
		nData[PublishFileKeys.LOGS] = {}
		for variant in self.get_variants():
			nData[PublishFileKeys.LOGS][variant] = self.get_variant_logs(variant=variant, asObject=False)
		return nData