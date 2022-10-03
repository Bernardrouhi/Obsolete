import os, sys

# add package to path
package_path = os.getcwd()
if package_path not in sys.path:
	sys.path.append(package_path)

import unittest
import Obsolete.envHandler as ObEnv

FILE_ADDRESS = ""
TEST_DIR = "E:/Project/Sample"

def setEnv():
	ObEnv.set_Env(key=ObEnv.BaseENV.PROJECT_FILE, value=FILE_ADDRESS)

class General_TDD(unittest.TestCase):
	def test_ReadProjectFile_env_01(self):
		# check for set and get environment variable
		global FILE_ADDRESS, TEST_DIR
		FILE_ADDRESS = os.path.join(TEST_DIR, "Sample.ob")
		setEnv()
		result = ObEnv.get_Env(key=ObEnv.BaseENV.PROJECT_FILE)
		self.assertEqual(FILE_ADDRESS, result)

	def test_ReadProjectFile_env_02(self):
		# check for del environment variable
		ObEnv.del_Env(key=ObEnv.BaseENV.PROJECT_FILE)
		result = ObEnv.get_Env(key=ObEnv.BaseENV.PROJECT_FILE)
		self.assertFalse(result)

	def test_ReadProjectFile_env_03(self):
		# check for del environment variable
		global FILE_ADDRESS, TEST_DIR
		FILE_ADDRESS = os.path.join(TEST_DIR, "Sample.ob")
		setEnv()
		address = ObEnv.get_Env(key=ObEnv.BaseENV.PROJECT_FILE)
		result = ObEnv.is_project_file(filePath=address)
		self.assertTrue(result)

if __name__ == '__main__':
	unittest.main()