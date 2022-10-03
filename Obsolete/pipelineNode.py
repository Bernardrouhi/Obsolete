import importlib
from . import envHandler
importlib.reload(envHandler)

from .envHandler import BaseENV, get_Env, set_Env
class Pipeline(object):
	def __init__(self):
		object.__init__(self)

	def get_ProjectName(self):
		'''Get the project name from environment variables.

			Returns: Name of project.
			Return Type: str
		'''
		return get_Env(BaseENV.PROJECT_NAME)
	def set_ProjectName(self, project_name=str):
		'''Set the project name in environment variables.

			Parameters:
			project_name (str) - Name of the project.
		'''
		set_Env(key=BaseENV.PROJECT_NAME, value=project_name)
		return

	def get_AssetType(self):
		'''Get the asset type from environment variables.

			Returns: Name of Asset Type.
			Return Type: str
		'''
		return get_Env(BaseENV.ASSET_TYPE)
	def set_AssetType(self, asset_type=str):
		'''Set the asset type in environment variables.

			Parameters:
			asset_type (str) - Name of the Asse Type.
		'''
		set_Env(key=BaseENV.ASSET_TYPE, value=asset_type)

	def get_AssetName(self):
		'''Get the asset name from environment variables.

			Returns: Name of the Asset.
			Return Type: str
		'''
		return get_Env(BaseENV.ASSET_NAME)
	def set_AssetName(self, asset_name=str):
		'''Set the asset name in environment variables.

			Parameters:
			asset_name (str) - Name of the Asset.
		'''
		set_Env(key=BaseENV.ASSET_NAME, value=asset_name)

	def get_AssetSpace(self):
		'''Get the asset space from environment variables.

			Returns: Name of the AssetSpace.
			Return Type: str
		'''
		return get_Env(BaseENV.ASSET_SPACE)
	def set_AssetSpace(self, asset_space=str):
		'''Set the asset space in environment variables.

			Parameters:
			asset_space (str) - Name of the AssetSpace.
		'''
		set_Env(key=BaseENV.ASSET_SPACE, value=asset_space)

	def get_AssetContainer(self):
		'''Get the asset container from environment variables.

			Returns: Name of the AssetContainer.
			Return Type: str
		'''
		return get_Env(BaseENV.ASSET_CONTAINER)
	def set_AssetContainer(self, asset_container=str):
		'''Set the asset container in environment variables.

			Parameters:
			asset_container (str) - Name of the AssetContainer.
		'''
		set_Env(key=BaseENV.ASSET_CONTAINER, value=asset_container)

	def get_WorkDirectory(self):
		'''Get the work directory from environment variables.

			Returns: Path to work directory.
			Return Type: str
		'''
		return get_Env(BaseENV.WORK_DIR)
	def set_WorkDirectory(self, directory=str):
		'''Set the work directory in environment variables.

			Parameters:
			directory (str) - Path to work directory.
		'''
		set_Env(key=BaseENV.WORK_DIR, value=directory)

	def get_PublishDirectory(self):
		'''Get the publish directory from environment variables.

			Returns: Path to publish directory.
			Return Type: str
		'''
		return get_Env(BaseENV.PUBLISH_DIR)
	def set_PublishDirectory(self, directory=str):
		'''Set the publish directory in environment variables.

			Parameters:
			directory (str) - Path to publish directory.
		'''
		set_Env(key=BaseENV.PUBLISH_DIR, value=directory)
