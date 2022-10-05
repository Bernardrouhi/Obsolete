import os, sys, json

# add package to path
package_path = os.getcwd()
if package_path not in sys.path:
	sys.path.append(package_path)

import unittest
import Obsolete.envHandler as ObEnv
import Obsolete.projectNode as ObPro

FILE_ADDRESS = "E:/Project/Sample/"

if not os.path.exists(FILE_ADDRESS):
	os.makedirs(FILE_ADDRESS)

def setEnv():
	ObEnv.set_Env(key=ObEnv.BaseENV.PROJECT_FILE, value=FILE_ADDRESS)

class General_TDD(unittest.TestCase):
	def test_CreateProjectFile_01(self):
		# Data
		projectName = "Sample"
		assetType = "Character"
		AssetSpace1 = "Model"
		AssetSpace2 = "Texture"
		PublishDirectory = "E:/Project/SamplePublish"
		ProjectFilePath = os.path.join(os.path.dirname(FILE_ADDRESS), f"{projectName}{ObEnv.OB_EXTENSION}")


		# expected result
		result = {
			ObPro.ProjectKeys.WORK_DIRECTORY: "",
			ObPro.ProjectKeys.PUBLISH_DIRECTORY: PublishDirectory,
			ObPro.ProjectKeys.PROJECT: projectName,
			ObPro.ProjectKeys.ASSET_TYPES:{assetType: [
				{
					ObPro.AssetSpaceKeys.ASSET_SPACE: AssetSpace1,
					ObPro.AssetSpaceKeys.WORKSPACE: ObPro.WorkspaceKeys.MAYA,
				},
				{
					ObPro.AssetSpaceKeys.ASSET_SPACE: AssetSpace2,
					ObPro.AssetSpaceKeys.WORKSPACE: ObPro.WorkspaceKeys.SUBSTANCE_PAINTER,
				},]
			},
			ObPro.ProjectKeys.VERSION:"1.0"
		}

		# ProjectObject
		projectObj = ObPro.ProjectObject()
		projectObj.set_ProjectName(project_name=projectName)

		assetTypelist = []
		assetTypelist.append(ObPro.AssetSpaceObject(AssetSpace=AssetSpace1, Workspace=ObPro.WorkspaceKeys.MAYA))
		assetTypelist.append(ObPro.AssetSpaceObject(AssetSpace=AssetSpace2, Workspace=ObPro.WorkspaceKeys.SUBSTANCE_PAINTER))

		projectObj.set_AssetType(assetType=assetType, assetSpaceList=assetTypelist)
		projectObj.set_PublishDirectory(publish_directory=PublishDirectory)
		projectObj.save(ProjectFile=ProjectFilePath)
		self.assertEqual(result, projectObj.toJSON())

	def test_CreateProjectFile_02(self):
		# Data
		projectName = "Sample_02"
		assetType = "Character"
		AssetSpace = ["Model", "Texture", "Rig", "Animation"]
		WorkSpace = ["Maya", "SubstancePainter", "Maya", "Maya"]
		ProjectFilePath = os.path.join(os.path.dirname(FILE_ADDRESS), f"{projectName}{ObEnv.OB_EXTENSION}")

		# ProjectObject
		projectObj = ObPro.ProjectObject()
		projectObj.set_ProjectName(project_name=projectName)

		assetTypelist = []
		for index in range(len(AssetSpace)):
			assetTypelist.append(ObPro.AssetSpaceObject(AssetSpace=AssetSpace[index], Workspace=WorkSpace[index]))

		projectObj.set_AssetType(assetType=assetType, assetSpaceList=assetTypelist)
		projectObj.save(ProjectFile=ProjectFilePath)
		self.assertTrue(os.path.exists(ProjectFilePath))

	def test_CreateProjectFile_03(self):
		# Data
		projectName = "Sample_03"
		assetType = {"Character": [
			ObPro.AssetSpaceObject(AssetSpace="Model", Workspace="Maya"),
			ObPro.AssetSpaceObject(AssetSpace="Texture", Workspace="SubstancePainter").toJSON(),
			ObPro.AssetSpaceObject(AssetSpace="Rig", Workspace="Maya"),
			ObPro.AssetSpaceObject(AssetSpace="Animation", Workspace="Maya").toJSON()
		]}
		ProjectFilePath = os.path.join(os.path.dirname(FILE_ADDRESS), f"{projectName}{ObEnv.OB_EXTENSION}")


		# ProjectObject
		projectObj = ObPro.ProjectObject(ProjectName=projectName,AssetTypes=assetType)
		projectObj.save(ProjectFile=ProjectFilePath)
		self.assertTrue(os.path.exists(ProjectFilePath))

	def test_CreateProjectFile_04(self):
		# Data
		projectName = "Sample_04"
		assetType = {"Character": [
			ObPro.AssetSpaceObject(AssetSpace="Model", Workspace="Maya"),
			ObPro.AssetSpaceObject(AssetSpace="Texture", Workspace="SubstancePainter").toJSON(),
			ObPro.AssetSpaceObject(AssetSpace="Rig", Workspace="Maya"),
			ObPro.AssetSpaceObject(AssetSpace="Animation", Workspace="Maya").toJSON()
		]}
		# adding extra none existent parameter
		assetType["Character"][1]["Version"] = 20
		ProjectFilePath = os.path.join(os.path.dirname(FILE_ADDRESS), f"{projectName}{ObEnv.OB_EXTENSION}")


		# ProjectObject
		projectObj = ObPro.ProjectObject(ProjectName=projectName,AssetTypes=assetType)
		projectObj.save(ProjectFile=ProjectFilePath)
		self.assertTrue(os.path.exists(ProjectFilePath))

	def test_LoadProjectFile(self):
		# Data
		# Server Start with \\\\ or //
		projectFile = "E:\\Project\\Sample\\Sample.ob".replace("\\", "/")
		project = ObPro.ProjectObject(ProjectFile=projectFile)

		self.assertTrue(os.path.exists(projectFile))

if __name__ == '__main__':
	unittest.main()