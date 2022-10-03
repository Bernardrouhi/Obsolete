import os

OB_EXTENSION = '.ob'

class BaseENV():
	"""Environment Variables"""
	WORK_DIR = 'OB_WORK_DIR'
	PUBLISH_DIR = 'OB_PUBLISH_DIR'
	PROJECT_NAME = 'OB_PROJECT_NAME'
	ASSET_NAME = 'OB_ASSET_NAME'
	ASSET_TYPE = 'OB_ASSET_TYPE'
	ASSET_SPACE = 'OB_ASSET_SPACE'
	ASSET_CONTAINER = 'OB_ASSET_CONTAINER'
	PROJECT_FILE = 'OB_FILE'

def is_Env(key=str):
	"""Check if Key exists in environment variables.

		Parameters:
		key (str) - Name of environment variable.

		Returns: True if exists, otherwise False.
		Return Type: bool
	"""
	return True if key in os.environ else False

def get_Env(key=str):
	"""Get from environment variables.

		Parameters:
		key (str) - Name of the environment variable.

		Returns: Value of the environment variable.
		Return Type: str
	"""
	return os.getenv(key, "")

def set_Env(key=str, value=str):
	"""Register a new key and value into environment variables.

		Parameters:
		key (str) - Name to register in environment variable.
		value (str) - Value to store in the Name.
	"""
	os.environ[key] = value

def del_Env(key=str):
	"""Delete from environment variables.

		Parameters:
		key (str) - Name of environment variable.
	"""
	if is_Env(key):
		del os.environ[key]

def is_project_file(filePath=str()):
	"""check the file exists and correct extension.

		Returns: validation of filepath
		Return Type: bool
	"""
	return filePath.lower().endswith(OB_EXTENSION) and os.path.exists(filePath)

def check_project_file(projectfile=str()):
	_projectfile = str()
	if projectfile:
		_projectfile = os.path.normpath(projectfile)
		if is_project_file(_projectfile):
			set_Env(key=BaseENV.PROJECT_FILE,value=_projectfile)
			message = "Project Loaded from File Path"
			print (f"{message}".center(len(message)+10, "-"))
			return _projectfile
	return ""

def check_project_env():
	result = get_Env(key=BaseENV.PROJECT_FILE)
	if result:
		_projectfile = os.path.normpath(result)
		if is_project_file(_projectfile):
			message = "Project Loaded from Environment Variable"
			print (f"{message}".center(len(message)+10, "-"))
			return _projectfile
	else:
		set_Env(key=BaseENV.PROJECT_FILE, value="")
	return ""