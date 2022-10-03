import os, sys, json

# add package to path
package_path = os.getcwd()
if package_path not in sys.path:
	sys.path.append(package_path)

import unittest
import Obsolete.envHandler as ObEnv
import Obsolete.projectMetadata as ObPM

FILE_ADDRESS = "E:/Project/Sample/"

def setEnv():
	ObEnv.set_Env(key=ObEnv.BaseENV.PROJECT_FILE, value=FILE_ADDRESS)

class General_TDD(unittest.TestCase):
	def test_CreateProjectFile_01(self):
		# Data
		projectName = "Sample"
		assetType = "Character"
		AssetSpace1 = "Model"
		WorkSpace1 = "Maya"
		AssetSpace2 = "Texture"
		WorkSpace2 = "SubstancePainter"
		PublishDirectory = "E:/Project/SamplePublish"
		ProjectFilePath = os.path.join(os.path.dirname(FILE_ADDRESS), f"{projectName}{ObEnv.OB_EXTENSION}")


		# expected result
		result = {
			ObPM.ProjectKeys.WorkDirectory: "",
			ObPM.ProjectKeys.PublishDirectory: PublishDirectory,
			ObPM.ProjectKeys.Project: projectName,
			ObPM.ProjectKeys.AssetTypes:{assetType: [
				{
					ObPM.ProjectKeys.AssetSpace: AssetSpace1,
					ObPM.ProjectKeys.WorkSpace: WorkSpace1,
				},
				{
					ObPM.ProjectKeys.AssetSpace: AssetSpace2,
					ObPM.ProjectKeys.WorkSpace: WorkSpace2,
				},]
			},
			ObPM.ProjectKeys.Version:"1.0"
		}

		# ProjectObject
		projectObj = ObPM.ProjectObject()
		projectObj.set_ProjectName(project_name=projectName)

		assetTypelist = []
		assetTypelist.append(ObPM.AssetSpaceObject(AssetSpace=AssetSpace1, Workspace=WorkSpace1))
		assetTypelist.append(ObPM.AssetSpaceObject(AssetSpace=AssetSpace2, Workspace=WorkSpace2))

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
		projectObj = ObPM.ProjectObject()
		projectObj.set_ProjectName(project_name=projectName)

		assetTypelist = []
		for index in range(len(AssetSpace)):
			assetTypelist.append(ObPM.AssetSpaceObject(AssetSpace=AssetSpace[index], Workspace=WorkSpace[index]))

		projectObj.set_AssetType(assetType=assetType, assetSpaceList=assetTypelist)
		projectObj.save(ProjectFile=ProjectFilePath)
		self.assertTrue(os.path.exists(ProjectFilePath))

	def test_CreateProjectFile_03(self):
		# Data
		projectName = "Sample_03"
		assetType = {"Character": [
			ObPM.AssetSpaceObject(AssetSpace="Model", Workspace="Maya"),
			ObPM.AssetSpaceObject(AssetSpace="Texture", Workspace="SubstancePainter").toJSON(),
			ObPM.AssetSpaceObject(AssetSpace="Rig", Workspace="Maya"),
			ObPM.AssetSpaceObject(AssetSpace="Animation", Workspace="Maya").toJSON()
		]}
		ProjectFilePath = os.path.join(os.path.dirname(FILE_ADDRESS), f"{projectName}{ObEnv.OB_EXTENSION}")


		# ProjectObject
		projectObj = ObPM.ProjectObject(ProjectName=projectName,AssetTypes=assetType)
		projectObj.save(ProjectFile=ProjectFilePath)
		self.assertTrue(os.path.exists(ProjectFilePath))

	def test_CreateProjectFile_04(self):
		# Data
		projectName = "Sample_04"
		assetType = {"Character": [
			ObPM.AssetSpaceObject(AssetSpace="Model", Workspace="Maya"),
			ObPM.AssetSpaceObject(AssetSpace="Texture", Workspace="SubstancePainter").toJSON(),
			ObPM.AssetSpaceObject(AssetSpace="Rig", Workspace="Maya"),
			ObPM.AssetSpaceObject(AssetSpace="Animation", Workspace="Maya").toJSON()
		]}
		# adding extra none existent parameter
		assetType["Character"][1]["Version"] = 20
		ProjectFilePath = os.path.join(os.path.dirname(FILE_ADDRESS), f"{projectName}{ObEnv.OB_EXTENSION}")


		# ProjectObject
		projectObj = ObPM.ProjectObject(ProjectName=projectName,AssetTypes=assetType)
		projectObj.save(ProjectFile=ProjectFilePath)
		self.assertTrue(os.path.exists(ProjectFilePath))


if __name__ == '__main__':
	unittest.main()