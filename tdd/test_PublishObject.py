import os, sys, json
from datetime import datetime, timezone

# add package to path
package_path = os.getcwd()
if package_path not in sys.path:
	sys.path.append(package_path)

import unittest
import Obsolete.envHandler as ObEnv
import Obsolete.publishNode as ObPub

FILE_ADDRESS = "E:/Project/Sample/"

class General_TDD(unittest.TestCase):
	def test_CreatePublishFile_01(self):
		# Data
		assetType = "Characters"
		assetContainer = "Enemies\\Zombie_Bellboy"
		assetSpace = "Rig"
		assetName = "Zombie_Bellboy"

		# expected result
		result = {
			ObPub.PublishFileKeys.VERSION:"1.0",
			ObPub.PublishFileKeys.ASSET_TYPE:assetType,
			ObPub.PublishFileKeys.ASSET_CONTAINER:assetContainer,
			ObPub.PublishFileKeys.ASSET_SPACE:assetSpace,
			ObPub.PublishFileKeys.ASSET_NAME:assetName,
			ObPub.PublishFileKeys.LOGS:dict()
		}

		# PublishObject
		publishObj = ObPub.PublishObject()
		publishObj.set_AssetType(assetType=assetType)
		publishObj.set_AssetContainer(assetContainer=assetContainer)
		publishObj.set_AssetSpace(assetSpace=assetSpace)
		publishObj.set_AssetName(assetName=assetName)
		publishObj.save(PublishFile=FILE_ADDRESS)

		self.assertEqual(result, publishObj.toJSON())

	def test_CreatePublishFile_02(self):
		# Data
		assetType = "Characters"
		assetContainer = "Enemies\\Zombie_Bellboy"
		assetSpace = "Rig"
		assetName = "Zombie_Bellboy"
		variant = "Test"
		user = "User_01"
		application = "TDD"
		record = float(datetime.now(timezone.utc).timestamp())

		# expected result
		result = {
			ObPub.PublishFileKeys.VERSION:"1.0",
			ObPub.PublishFileKeys.ASSET_TYPE:assetType,
			ObPub.PublishFileKeys.ASSET_CONTAINER:assetContainer,
			ObPub.PublishFileKeys.ASSET_SPACE:assetSpace,
			ObPub.PublishFileKeys.ASSET_NAME:assetName,
			ObPub.PublishFileKeys.LOGS:{}
		}

		# PublishObject
		publishObj = ObPub.PublishObject(
			AssetType=assetType, 
			AssetContainer=assetContainer, 
			AssetSpace=assetSpace, 
			AssetName=assetName)
		publishObj.save(PublishFile=FILE_ADDRESS)

		self.assertEqual(result, publishObj.toJSON())

	def test_CreatePublishFile_03(self):
		# Data
		assetType = "Characters"
		assetContainer = "Enemies\\Zombie_Bellboy"
		assetSpace = "Rig"
		assetName = "Zombie_Bellboy"
		variant = "Test"
		user = "User_01"
		application = "TDD"
		record = float(datetime.now(timezone.utc).timestamp())

		# expected result
		result = {
			ObPub.PublishFileKeys.VERSION:"1.0",
			ObPub.PublishFileKeys.ASSET_TYPE:assetType,
			ObPub.PublishFileKeys.ASSET_CONTAINER:assetContainer,
			ObPub.PublishFileKeys.ASSET_SPACE:assetSpace,
			ObPub.PublishFileKeys.ASSET_NAME:assetName,
			ObPub.PublishFileKeys.LOGS:{variant:[
				{
					ObPub.PublishLogKeys.VERSION:1,
					ObPub.PublishLogKeys.VARIANT:variant,
					ObPub.PublishLogKeys.USER:user,
					ObPub.PublishLogKeys.WORKFILES:[],
					ObPub.PublishLogKeys.PUBLISHFILES:[],
					ObPub.PublishLogKeys.RECORD:record,
					ObPub.PublishLogKeys.APP:application,
					ObPub.PublishLogKeys.DESCRIPTION:"",
				}
			]}
		}

		# PublishObject
		publishObj = ObPub.PublishObject(
			AssetType=assetType, 
			AssetContainer=assetContainer, 
			AssetSpace=assetSpace, 
			AssetName=assetName)
		publishObj.add_variant_log(
			variant=variant,
			logNode=ObPub.LogObject(
				Variant=variant, 
				User=user, 
				Application=application, 
				Record=record
			)
		)
		publishObj.save(PublishFile=FILE_ADDRESS)

		self.assertEqual(result, publishObj.toJSON())

if __name__ == '__main__':
	unittest.main()