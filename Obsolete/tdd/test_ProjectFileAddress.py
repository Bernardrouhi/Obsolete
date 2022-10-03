import os, sys

# add package to path
package_path = os.getcwd()
if package_path not in sys.path:
	sys.path.append(package_path)

import unittest
import Obsolete.envHandler as ObEnv


class General_TDD(unittest.TestCase):
	def test_ReadProjectFile_address_01(self):
		# forward slash
		address = "E:/Project/Sample/Sample.ob"
		result = ObEnv.is_project_file(filePath=address)
		self.assertTrue(result)

	def test_ReadProjectFile_address_02(self):
		# backward slash
		address = "E:\\Project\\Sample\\Sample.ob"
		result = ObEnv.is_project_file(filePath=address)
		self.assertTrue(result)

	def test_ReadProjectFile_address_03(self):
		# mix of forward and backward slash
		address = "E:\\Project\\Sample/Sample.ob"
		result = ObEnv.is_project_file(filePath=address)
		self.assertTrue(result)

	def test_ReadProjectFile_address_04(self):
		# No Extension
		address = "E:\\Project\\Sample/Sample"
		result = ObEnv.is_project_file(filePath=address)
		# Only files with ObEnv.OB_EXTENSION are valid 
		self.assertFalse(result)

if __name__ == '__main__':
	unittest.main()