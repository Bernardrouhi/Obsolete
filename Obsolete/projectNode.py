import os
import json
from string import Template

from .envHandler import OB_EXTENSION, is_project_file
from .pipelineNode import Pipeline

class ProjectKeys():
	WORK_DIRECTORY = "Work_directory"
	PUBLISH_DIRECTORY = "Publish_directory"
	PROJECT = "Project"
	VERSION = "Version"
	ASSET_TYPES = "AssetTypes"

	@staticmethod
	def validKeys():
		"""Get the list of valid keys for expanding the path

			Returns: Valid keys.
			Return Type: list
		"""
		return [ProjectKeys.WORK_DIRECTORY, ProjectKeys.PUBLISH_DIRECTORY, ProjectKeys.PROJECT]

class AssetSpaceKeys():
	ASSET_SPACE = "AssetSpace"
	WORKSPACE = "Workspace"

class WorkspaceKeys():
	MAYA = "Maya"
	SUBSTANCE_PAINTER = "SubstancePainter"
	EMPTY = "Empty"

class AssetSpaceObject(object):
	"""Handle AssetSpace object."""
	def __init__(self, AssetSpace=str(), Workspace=str(), **kwargs):
		self._data = self.ASSETSPACE_METADATA()
		if isinstance(AssetSpace, str) and AssetSpace : self.set_AssetSpace(assetSpace=AssetSpace)
		if isinstance(Workspace, str) and Workspace : self.set_WorkSpace(workSpace=Workspace)

	@staticmethod
	def ASSETSPACE_METADATA():
		"""AssetSpace default Metadata structure"""
		return {
            AssetSpaceKeys.ASSET_SPACE:"", 
            AssetSpaceKeys.WORKSPACE:""
            }.copy()

	def get_AssetSpace(self):
		"""get the AssetSpace name.

			Returns: AssetApace name.
			Return Type: str
		"""
		return self._data[AssetSpaceKeys.ASSET_SPACE]
	def set_AssetSpace(self, assetSpace=str()):
		"""set the AssetSpace name.

			Parameters:
			assetSpace (str) - Name of AssetSpace.
		"""
		self._data[AssetSpaceKeys.ASSET_SPACE] = assetSpace

	def get_WorkSpace(self):
		"""get the AssetSpace workspace.

			Returns: AssetSpace workspace.
			Return Type: str
		"""
		self._data[AssetSpaceKeys.WORKSPACE] = workSpace
	def set_WorkSpace(self, workSpace=str()):
		"""set the AssetSpace workspace.

			Parameters:
			workSpace (str) - Name of related application.
		"""
		self._data[AssetSpaceKeys.WORKSPACE] = workSpace

	def toJSON(self):
		"""Serialized the object into dictionary.

			Returns: get a dictionary of AssetSpaceObject.
			Returns Types: dict
		"""
		return self._data

class ProjectObject(object):
	"""Handle Project file."""
	__version__ = "1.0"
	def __init__(self, ProjectFile=str(), WorkDirectory=str(), PublishDirectory=str(), ProjectName=str(), AssetTypes=dict()):
		self._data = self.PROJECT_METADATA()
		self._path = str(os.path.expanduser('~'))
		self._pm = Pipeline()
		self.setDefault()
		if is_project_file(filePath=ProjectFile):
			self.load(ProjectFile=ProjectFile)
		else:
			self.set_ProjectName(project_name=ProjectName)
			self.set_PublishDirectory(publish_directory=PublishDirectory)
			self.set_WorkDirectory(work_directory=WorkDirectory)
			if isinstance(AssetTypes, dict):
				for key in AssetTypes.keys():
					if isinstance(AssetTypes[key], (list, tuple)):
						self.set_AssetType(assetType=key,assetSpaceList=AssetTypes[key])
					else:
						self.add_AssetType(assetType=key)

	@staticmethod
	def PROJECT_METADATA():
		"""Project default metadata structure."""
		return {
			ProjectKeys.WORK_DIRECTORY:"",
			ProjectKeys.PUBLISH_DIRECTORY:"",
			ProjectKeys.PROJECT:"",
			ProjectKeys.ASSET_TYPES:{},
			ProjectKeys.VERSION:ProjectObject.__version__
		    }.copy()

	def setDefault(self):
		"""Set the prject default, load or set ProjectName and WorkDirectory."""
		# Project Name
		if self._pm.get_ProjectName():
			self.ProjectName = self._pm.get_ProjectName()
		else:
			self._pm.set_ProjectName(self._data[ProjectKeys.PROJECT])


		# Work Directory
		if self._pm.get_WorkDirectory():
			self.WorkDirectory = self._pm.get_WorkDirectory()
		else:
			self._pm.set_WorkDirectory(self._data[ProjectKeys.WORK_DIRECTORY])

	def get_Version(self):
		"""Get last opened directory.

			Returns: version of the file (Major,Bug)
			Return Type: tuple
		"""
		return tuple(self._dataVersion.split("."))

	def get_LastPath(self):
		"""Get last opened directory.

			Returns: directory path.
			Returns Types: str
		"""
		return self._path
	def set_LastPath(self, directory=str):
		"""Set last opened directory.

			Returns: directory path.
			Returns Types: str
		"""
		self._path = directory

	def get_ProjectName(self):
		"""Get the name of project.

			Returns: Name of the Project
			Returns Types: str
		"""
		return self._pm.get_ProjectName()
	def set_ProjectName(self, project_name=str):
		"""Update the project name.

			Parameters:
			project_name (str) - Name of the Project.
		"""
		self._data[ProjectKeys.PROJECT] = project_name
		self._pm.set_ProjectName(project_name)

	def get_WorkDirectory(self):
		"""Get the WorkDirectory.

			Returns: Path to project work directory.
			Returns Types: str
		"""
		return self._pm.get_WorkDirectory()
	def set_WorkDirectory(self, work_directory=str):
		"""update the Work Directory.

			Parameters:
			work_directory (str) - Path to project work directory.
		"""
		self._data[ProjectKeys.WORK_DIRECTORY] = work_directory
		self._pm.set_WorkDirectory(work_directory)

	def get_PublishDirectory(self):
		"""Get the Publish_directory.

			Returns: Path to project work directory.
			Returns Types: str
		"""
		return self._pm.get_PublishDirectory()
	def set_PublishDirectory(self, publish_directory=str):
		"""update the Work Directory.

			Parameters:
			publish_directory (str) - Path to project work directory.
		"""
		self._data[ProjectKeys.PUBLISH_DIRECTORY] = publish_directory
		self._pm.set_PublishDirectory(publish_directory)

	def get_AssetTypesName(self):
		"""Get list of all the project AssetTypes"""
		return self._data[ProjectKeys.ASSET_TYPES].keys()
	def get_AssetTypes(self, asObject=bool(False)):
		"""get the Project assetTypes.

			Parameters:
			asObject (bool) - get the return type as AssetSpaceObject or JSON.

			Returns: get a dictionary of AssetType with serialized AssetSpace.
			Returns Types: dict
		"""
		data = {}
		if asObject:
			data = self._data[ProjectKeys.ASSET_TYPES]
		else:
			for assetTypeName in self._data[ProjectKeys.ASSET_TYPES]:
				data[assetTypeName] = []
				for assetObj in self._data[ProjectKeys.ASSET_TYPES][assetTypeName]:
					raw = assetObj.toJSON()
					data[assetTypeName].append(raw)
		return data
	def add_AssetType(self, assetType=str):
		"""Add the Project assetType.

			Parameters:
			assetType (str) - Name of AssetType.
		"""
		if assetType not in self._data[ProjectKeys.ASSET_TYPES]:
			self._data[ProjectKeys.ASSET_TYPES][assetType] = list()
	def set_AssetType(self, assetType=str, assetSpaceList=list):
		"""Override the Project assetType.

			Parameters:
			assetType (str) - Name of AssetType.
			assetSpaceList (list) - List of AssetSpaces.
		"""
		self._data[ProjectKeys.ASSET_TYPES][assetType] = []
		for assetSpace in assetSpaceList:
			if isinstance(assetSpace, AssetSpaceObject):
				self.add_AssetSpace(assetType=assetType, assetTypeObject=assetSpace)
			elif isinstance(assetSpace, dict):
				self.add_AssetSpace(assetType=assetType, assetTypeObject=AssetSpaceObject(**assetSpace))

	def get_AssetSpaces(self, assetType=str(), asObject=bool(False)):
		"""get the AssetType AssetSpaces.

			Parameters:
			assetType (str) - Name of AssetType.
			asObject (bool) - get the return type as AssetSpaceObject or JSON.

			Returns: List of AssetSpace.
			Returns Types: list
		"""
		assetSpaces = list()
		if assetType in self._data[ProjectKeys.ASSET_TYPES]:
			if asObject:
				assetSpaces = self._data[ProjectKeys.ASSET_TYPES][assetType]
			else:
				for assetSpace in self._data[ProjectKeys.ASSET_TYPES][assetType]:
					assetSpaces.append(assetSpace.toJSON())
		return assetSpaces
	def add_AssetSpace(self, assetType=str, assetTypeObject=AssetSpaceObject):
		"""Add an AssetTypeObject to AssetType.

			Parameters:
			assetType (str) - Name of AssetType.
			assetTypeObject (AssetSpaceObject) - AssetSpace object reference.
		"""
		if assetType not in self._data[ProjectKeys.ASSET_TYPES]:
			self.add_AssetType(assetType=assetType)
		self._data[ProjectKeys.ASSET_TYPES][assetType].append(assetTypeObject)

	def update_settings(self, project_name=str, work_directory=str):
		"""update all the settings.

			Parameters:
			project_name (str) - Name of the Project.
			work_directory (str) - Path to project work directory.
		"""
		self.set_ProjectName(project_name)
		self.set_WorkDirectory(work_directory)

	def load(self, ProjectFile=str):
		"""Load  Projet file.

			Parameters:
			ProjectFile (str) - Path to project file.
		"""
		if ProjectFile and ProjectFile.lower().endswith(OB_EXTENSION):
			# update the latest path
			self._path = os.path.dirname(ProjectFile)
			with open(ProjectFile, 'r') as outfile:
				# Load project file
				if outfile:
					LoadedData = json.load(outfile)
					if ProjectKeys.VERSION in LoadedData:
						self._dataVersion= LoadedData[ProjectKeys.VERSION]
						if LoadedData[ProjectKeys.VERSION] == __version__:
							if ProjectKeys.PROJECT in LoadedData:
								self.set_ProjectName(project_name=LoadedData[ProjectKeys.PROJECT])
							if ProjectKeys.WORK_DIRECTORY in LoadedData:
								self.set_WorkDirectory(work_directory=LoadedData[ProjectKeys.WORK_DIRECTORY])
							if ProjectKeys.ASSET_TYPES in LoadedData:
								for assetType in LoadedData[ProjectKeys.ASSET_TYPES]:
									self.set_AssetType(assetType=assetType, assetSpaceList=LoadedData[ProjectKeys.ASSET_TYPES][assetType])
							if ProjectKeys.PUBLISH_DIRECTORY in LoadedData:
								self.set_PublishDirectory(publish_directory=LoadedData[ProjectKeys.PUBLISH_DIRECTORY])

	def save(self, ProjectFile=str):
		"""Save Projet file.

			Parameters:
			ProjectFile (str) - Path to project file.
		"""
		if ProjectFile:
			# add extension
			file_path = ProjectFile.split('.')[0]
			file_path = f"{file_path}{OB_EXTENSION}"
			# update the latest path
			self._path = os.path.dirname(ProjectFile)
			# save project file
			with open(file_path, 'w') as outfile:
				json.dump(self.toJSON(), outfile, ensure_ascii=False, indent=4)

	def toJSON(self, clean=bool(True)):
		"""Serialized the object into dictionary.

			Parameters:
			clean (bool) - clean the local work directory.

			Returns: get a dictionary of ProjectObject.
			Returns Types: dict
		"""
		nData = self._data.copy()
		if clean : nData[ProjectKeys.WORK_DIRECTORY] = str()
		nData[ProjectKeys.ASSET_TYPES] = self.get_AssetTypes()
		return nData

	def expand_ProjectPath(self, templatePath=str):
		"""expand the project Path from give template path.

			Parameters:
			templatePath (str) - template path.

			Returns: expanded the project path
			Return Type: str
		"""
		nPath = Template(templatePath).safe_substitute(self.toJSON(clean=False))
		nPath = os.path.normpath(nPath).replace("\\","/")
		return nPath