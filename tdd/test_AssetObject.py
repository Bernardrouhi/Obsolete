import os, sys, json
from datetime import datetime, timezone

# add package to path
package_path = os.getcwd()
if package_path not in sys.path:
	sys.path.append(package_path)

import unittest
import Obsolete.envHandler as ObEnv
import Obsolete.pipelineNode as ObPip
import Obsolete.assetNode as ObAs
import Obsolete.projectNode as ObPro

class General_TDD(unittest.TestCase):
	def test_CreateAssetPath_01(self):
		# Data
		assetType = "Characters"
		assetContainer = "Enemies\\Zombie_Bellboy"
		assetSpace = "Rig"
		assetName = "Zombie_Bellboy"

		# expected result
		result = os.path.normpath(f"{assetType}/{assetContainer}/{assetSpace}/{assetName}").replace("\\","/")

		# AssetObject
		asset = ObAs.AssetObject(
			AssetType=assetType, 
			AssetContainer=assetContainer, 
			AssetSpace=assetSpace, 
			AssetName=assetName)
		tempPath = ObEnv.generate_Path(keys=[
			ObAs.AssetKeys.ASSET_TYPE, 
			ObAs.AssetKeys.ASSET_CONTAINER,
			ObAs.AssetKeys.ASSET_SPACE,
			ObAs.AssetKeys.ASSET_NAME])
		assetResutl = asset.expand_AssetPath(templatePath=tempPath)

		self.assertEqual(result, assetResutl)

	def test_CreateAssetPath_02(self):
		# Data
		workDir = "E:/project/sample"
		assetType = "Characters"
		assetContainer = "Enemies\\Zombie_Bellboy"
		assetSpace = "Rig"
		assetName = "Zombie_Bellboy"

		# expected result
		# E:/project/sample/Characters/Enemies/Zombie_Bellboy/Rig/Zombie_Bellboy
		result = os.path.normpath(f"{workDir}/{assetType}/{assetContainer}/{assetSpace}/{assetName}").replace("\\","/")

		# AssetObject
		project = ObPro.ProjectObject(WorkDirectory=workDir)
		asset = ObAs.AssetObject(
			AssetType=assetType, 
			AssetContainer=assetContainer, 
			AssetSpace=assetSpace, 
			AssetName=assetName)
		tempPath = ObEnv.generate_Path(keys=[
			ObPro.ProjectKeys.WORK_DIRECTORY,
			ObAs.AssetKeys.ASSET_TYPE, 
			ObAs.AssetKeys.ASSET_CONTAINER,
			ObAs.AssetKeys.ASSET_SPACE,
			ObAs.AssetKeys.ASSET_NAME])
		assetResult = asset.expand_AssetPath(templatePath=tempPath)
		assetResult = project.expand_ProjectPath(templatePath=assetResult)

		self.assertEqual(result, assetResult)

	def test_CreateTemplateWithValidKeys_01(self):
		# Data
		workDir = ObPro.ProjectKeys.WORK_DIRECTORY
		assetType = ObAs.AssetKeys.ASSET_TYPE
		assetContainer = ObAs.AssetKeys.ASSET_CONTAINER
		assetSpace = ObAs.AssetKeys.ASSET_SPACE
		assetName = ObAs.AssetKeys.ASSET_NAME
		special = "Local"

		# expected result
		# E:/project/sample/Characters/Enemies/Zombie_Bellboy/Rig/Zombie_Bellboy
		result = os.path.normpath(f"${workDir}/{special}/${assetType}/${assetContainer}/${assetSpace}/${assetName}").replace("\\","/")

		# AssetObject
		project = ObPro.ProjectObject(WorkDirectory=workDir)
		asset = ObAs.AssetObject(
			AssetType=assetType, 
			AssetContainer=assetContainer, 
			AssetSpace=assetSpace, 
			AssetName=assetName)
		tempPath = ObEnv.generate_Path(keys=[
			ObPro.ProjectKeys.WORK_DIRECTORY,
			special,
			ObAs.AssetKeys.ASSET_TYPE, 
			ObAs.AssetKeys.ASSET_CONTAINER,
			ObAs.AssetKeys.ASSET_SPACE,
			ObAs.AssetKeys.ASSET_NAME], validKeys=ObAs.AssetKeys.validKeys()+ObPro.ProjectKeys.validKeys())

		self.assertEqual(result, tempPath)

if __name__ == '__main__':
	unittest.main()