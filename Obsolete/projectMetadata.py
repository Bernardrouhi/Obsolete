import os
import json

from .envHandler import OB_EXTENSION, is_project_file
from .pipelineHandler import Pipeline

class ProjectKeys():
	WorkDirectory = "Work_directory"
	PublishDirectory = "Publish_directory"
	Project = "Project"
	Version = "Version"
	AssetTypes = "AssetTypes"
	AssetSpace = "AssetSpace"
	WorkSpace = "Workspace"

class AssetSpaceKeys():
	Maya = "Maya"
	SusbtancePainter = "SubstancePainter"
	Empty = "Empty"

class AssetSpaceObject(object):
	"""Handle AssetSpace object."""
	def __init__(self, AssetSpace=str(), Workspace=str(), **kwargs):
		self._data = self.ASSETSPACE_METADATA()
		if AssetSpace:
			self.set_AssetSpace(assetSpace=AssetSpace)
		if Workspace:
			self.set_WorkSpace(workSpace=Workspace)

	@staticmethod
	def ASSETSPACE_METADATA():
		"""AssetSpace default Metadata structure"""
		return {
            ProjectKeys.AssetSpace:"", 
            ProjectKeys.WorkSpace:""
            }.copy()

	def set_AssetSpace(self, assetSpace=str()):
		"""set the AssetSpace name.

			Parameters:
			assetSpace (str) - Name of AssetSpace.
		"""
		self._data[ProjectKeys.AssetSpace] = assetSpace

	def set_WorkSpace(self, workSpace=str()):
		"""set the AssetSpace workspace.

			Parameters:
			workSpace (str) - Name of related application.
		"""
		self._data[ProjectKeys.WorkSpace] = workSpace

	def toJSON(self):
		"""Serialized the object into dictionary.

			Returns: get a dictionary of AssetSpaceObject.
			Returns Types: dict
		"""
		return self._data

class ProjectObject(object):
	"""Handle Project file."""
	def __init__(self, ProjectFile=str(), WorkDirectory=str(), PublishDirectory=str(), ProjectName=str(), AssetTypes=dict()):
		self._data = self.PROJECT_METADATA()
		self._path = str(os.path.expanduser('~'))
		self._version = self.PROJECT_METADATA()[ProjectKeys.Version]
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
		"""Project default Metadata structure."""
		return {
			ProjectKeys.WorkDirectory:"",
			ProjectKeys.PublishDirectory:"",
			ProjectKeys.Project:"",
			ProjectKeys.AssetTypes:{},
			ProjectKeys.Version:"1.0"
		    }.copy()

	def setDefault(self):
		"""Set the prject default, load or set ProjectName and WorkDirectory."""
		# Project Name
		if self._pm.get_ProjectName():
			self.ProjectName = self._pm.get_ProjectName()
		else:
			self._pm.set_ProjectName(self._data[ProjectKeys.Project])


		# Work Directory
		if self._pm.get_WorkDirectory():
			self.WorkDirectory = self._pm.get_WorkDirectory()
		else:
			self._pm.set_WorkDirectory(self._data[ProjectKeys.WorkDirectory])

	def get_Version(self):
		"""Get last opened directory.

			Returns: version of the file (Major,Bug)
			Return Type: tuple
		"""
		return tuple(self._version.split("."))

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
		self._data[ProjectKeys.Project] = project_name
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
		self._data[ProjectKeys.WorkDirectory] = work_directory
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
		self._data[ProjectKeys.PublishDirectory] = publish_directory
		self._pm.set_PublishDirectory(publish_directory)

	def get_AssetTypesName(self):
		"""Get list of all the project AssetTypes"""
		return self._data[ProjectKeys.AssetTypes].keys()
	def get_AssetTypes(self, asObject=bool(False)):
		"""get the Project assetTypes.

			Returns: get a dictionary of AssetType with serialized AssetSpace .
			Returns Types: dict
		"""
		data = {}
		if asObject:
			data = self._data[ProjectKeys.AssetTypes]
		else:
			for assetTypeName in self._data[ProjectKeys.AssetTypes]:
				data[assetTypeName] = []
				for assetObj in self._data[ProjectKeys.AssetTypes][assetTypeName]:
					raw = assetObj.toJSON()
					data[assetTypeName].append(raw)
		return data
	def add_AssetType(self, assetType=str):
		"""Add the Project assetType.

			Parameters:
			assetType (str) - Name of AssetType.
		"""
		if assetType not in self._data[ProjectKeys.AssetTypes]:
			self._data[ProjectKeys.AssetTypes][assetType] = list()
	def set_AssetType(self, assetType=str, assetSpaceList=list):
		"""Override the Project assetType.

			Parameters:
			assetType (str) - Name of AssetType.
			assetSpaceList (list) - List of AssetSpaces.
		"""
		self._data[ProjectKeys.AssetTypes][assetType] = []
		for assetSpace in assetSpaceList:
			if isinstance(assetSpace, AssetSpaceObject):
				self.add_AssetSpace(assetType=assetType, assetTypeObject=assetSpace)
			elif isinstance(assetSpace, dict):
				self.add_AssetSpace(assetType=assetType, assetTypeObject=AssetSpaceObject(**assetSpace))

	def get_AssetSpaces(self, assetType=str(), asObject=bool(False)):
		"""get the AssetType AssetSpaces.

			Returns: List of AssetSpace .
			Returns Types: list
		"""
		assetSpaces = list()
		if assetType in self._data[ProjectKeys.AssetTypes]:
			if asObject:
				assetSpaces = self._data[ProjectKeys.AssetTypes][assetType]
			else:
				for assetSpace in self._data[ProjectKeys.AssetTypes][assetType]:
					assetSpaces.append(assetSpace.toJSON())
		return assetSpaces
	def add_AssetSpace(self, assetType=str, assetTypeObject=AssetSpaceObject):
		"""Add an AssetTypeObject to AssetType.

			Parameters:
			assetType (str) - Name of AssetType.
			assetTypeObject (AssetSpaceObject) - AssetSpace object reference.
		"""
		if assetType not in self._data[ProjectKeys.AssetTypes]:
			self.add_AssetType(assetType=assetType)
		self._data[ProjectKeys.AssetTypes][assetType].append(assetTypeObject)

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
					if ProjectKeys.Version in LoadedData:
						self._version = LoadedData[ProjectKeys.Version]
						if LoadedData[ProjectKeys.Version] == "1.0":
							if ProjectKeys.Project in LoadedData:
								self.set_ProjectName(project_name=LoadedData[ProjectKeys.Project])
							if ProjectKeys.WorkDirectory in LoadedData:
								self.set_WorkDirectory(work_directory=LoadedData[ProjectKeys.WorkDirectory])
							if ProjectKeys.AssetTypes in LoadedData:
								for assetType in LoadedData[ProjectKeys.AssetTypes]:
									self.set_AssetType(assetType=assetType, assetSpaceList=LoadedData[ProjectKeys.AssetTypes][assetType])
							if ProjectKeys.PublishDirectory in LoadedData:
								self.set_PublishDirectory(publish_directory=LoadedData[ProjectKeys.PublishDirectory])

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

	def toJSON(self):
		"""Serialized the object into dictionary."""
		nData = self._data.copy()
		nData[ProjectKeys.WorkDirectory] = str()
		nData[ProjectKeys.AssetTypes] = self.get_AssetTypes()
		return nData