import os, sys, json
from datetime import datetime, timezone

# add package to path
package_path = os.getcwd()
if package_path not in sys.path:
	sys.path.append(package_path)

import unittest
import Obsolete.envHandler as ObEnv
import Obsolete.publishNode as ObPub
import Obsolete.assetNode as ObAs
import Obsolete.logNode as ObLog

FILE_ADDRESS = "E:/Project/Sample/"

if not os.path.exists(FILE_ADDRESS):
	os.makedirs(FILE_ADDRESS)

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
			ObAs.AssetKeys.ASSET_TYPE:assetType,
			ObAs.AssetKeys.ASSET_CONTAINER:assetContainer,
			ObAs.AssetKeys.ASSET_SPACE:assetSpace,
			ObAs.AssetKeys.ASSET_NAME:assetName,
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

		# expected result
		result = {
			ObPub.PublishFileKeys.VERSION:ObPub.PublishObject.__version__,
			ObAs.AssetKeys.ASSET_TYPE:assetType,
			ObAs.AssetKeys.ASSET_CONTAINER:assetContainer,
			ObAs.AssetKeys.ASSET_SPACE:assetSpace,
			ObAs.AssetKeys.ASSET_NAME:assetName,
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
		# expected result
		result = {
			ObPub.PublishFileKeys.VERSION:"1.0",
			ObAs.AssetKeys.ASSET_TYPE:"",
			ObAs.AssetKeys.ASSET_CONTAINER:"",
			ObAs.AssetKeys.ASSET_SPACE:"",
			ObAs.AssetKeys.ASSET_NAME:"",
			ObPub.PublishFileKeys.LOGS:{}
		}

		# PublishObject
		publishObj = ObPub.PublishObject()
		publishObj.save(PublishFile=FILE_ADDRESS)

		self.assertEqual(result, publishObj.toJSON())

	def test_CreatePublishFile_04(self):
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
			ObAs.AssetKeys.ASSET_TYPE:assetType,
			ObAs.AssetKeys.ASSET_CONTAINER:assetContainer,
			ObAs.AssetKeys.ASSET_SPACE:assetSpace,
			ObAs.AssetKeys.ASSET_NAME:assetName,
			ObPub.PublishFileKeys.LOGS:{variant:[
				{
					ObLog.LogKeys.VERSION:1,
					ObLog.LogKeys.VARIANT:variant,
					ObLog.LogKeys.USER:user,
					ObLog.LogKeys.WORKFILES:[],
					ObLog.LogKeys.PUBLISHFILES:[],
					ObLog.LogKeys.RECORD:record,
					ObLog.LogKeys.APP:application,
					ObLog.LogKeys.DESCRIPTION:"",
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