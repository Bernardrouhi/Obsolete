import os
from string import Template

class AssetKeys():
	ASSET_TYPE = "AssetType"
	ASSET_CONTAINER = "AssetContainer"
	ASSET_SPACE = "AssetSpace"
	ASSET_NAME = "AssetName"

	@staticmethod
	def validKeys():
		"""Get the list of valid keys for expanding the path

			Returns: Valid keys.
			Return Type: list
		"""
		return [AssetKeys.ASSET_TYPE, AssetKeys.ASSET_CONTAINER, AssetKeys.ASSET_SPACE, AssetKeys.ASSET_NAME]

class AssetObject(object):
	"""Handle Asset object"""
	def __init__(self, AssetType=str(), AssetContainer=str(), AssetSpace=str(), AssetName=str()):
		self._data = self.ASSET_METADATA()
		if isinstance(AssetType, str) and AssetType : self.set_AssetType(assetType=AssetType)
		if isinstance(AssetContainer, str) and AssetContainer : self.set_AssetContainer(assetContainer=AssetContainer)
		if isinstance(AssetSpace, str) and AssetSpace : self.set_AssetSpace(assetSpace=AssetSpace)
		if isinstance(AssetName, str) and AssetName : self.set_AssetName(assetName=AssetName)

	@staticmethod
	def ASSET_METADATA():
		"""Asset Metadata structure"""
		return {
			AssetKeys.ASSET_TYPE:str(),
			AssetKeys.ASSET_CONTAINER:str(),
			AssetKeys.ASSET_SPACE:str(),
			AssetKeys.ASSET_NAME:str()
		}.copy()

	def reset(self):
		"""Reset the node"""
		self._data = self.ASSET_METADATA()

	def get_AssetType(self):
		"""Get the AssetType

			Returns: Asset type
			Return Type: str
		"""
		return self._data[AssetKeys.ASSET_TYPE]
	def set_AssetType(self, assetType=str):
		"""Set the AssetType

			Parameters:
			assetType (str) - Asset type.
		"""
		self._data[AssetKeys.ASSET_TYPE] = assetType

	def get_AssetContainer(self):
		"""Get the AssetContainer

			Returns: Asset container
			Return Type: str
		"""
		return self._data[AssetKeys.ASSET_CONTAINER]
	def set_AssetContainer(self, assetContainer=str):
		"""Set the AssetContainer

			Parameters:
			assetContainer (str) - Asset container.
		"""
		self._data[AssetKeys.ASSET_CONTAINER] = assetContainer

	def get_AssetSpace(self):
		"""Get the AssetSpace

			Returns: Asset space
			Return Type: str
		"""
		return self._data[AssetKeys.ASSET_SPACE]
	def set_AssetSpace(self, assetSpace=str):
		"""Set the AssetSpace

			Parameters:
			assetSpace (str) - Asset space.
		"""
		self._data[AssetKeys.ASSET_SPACE] = assetSpace

	def get_AssetName(self):
		"""Get the AssetName

			Returns: Asset name
			Return Type: str
		"""
		return self._data[AssetKeys.ASSET_NAME]
	def set_AssetName(self, assetName=str):
		"""Set the AssetName

			Parameters:
			assetName (str) - Asset name.
		"""
		self._data[AssetKeys.ASSET_NAME] = assetName

	def toJSON(self):
		"""Serialized the object into dictionary.

			Returns: get a dictionary of AssetObject.
			Returns Types: dict
		"""
		return self._data.copy()

	def expand_AssetPath(self, templatePath=str):
		"""expand the asset Path from give template path.

			Parameters:
			templatePath (str) - template path.

			Returns: expanded the asset path
			Return Type: str
		"""
		nPath = Template(templatePath).safe_substitute(self.toJSON())
		nPath = os.path.normpath(nPath).replace("\\","/")
		return nPath
