import os, sys, json

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
			ObPub.PublishFileKeys.FILE_VERSION:"2.0",
			ObPub.PublishFileKeys.VERSION:int(),
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

if __name__ == '__main__':
	unittest.main()