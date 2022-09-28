import os

OB_EXTENSION = '.ob'

class BaseENV():
	WORK_DIR = 'OB_WORK_DIR'
	PUBLISH_DIR = 'OB_PUBLISH_DIR'
	PROJECT_NAME = 'OB_PROJECT_NAME'
	ASSET_NAME = 'OB_ASSET_NAME'
	ASSET_TYPE = 'OB_ASSET_TYPE'
	ASSET_SPACE = 'OB_ASSET_SPACE'
	ASSET_CONTAINER = 'OB_ASSET_CONTAINER'
	PROJECT_FILE = 'OB_FILE'

def is_Env(key=str):
	'''Check if Key exists in environment variables.

		Args:
			key (str): Name of environment variable.

		Return:
			(boolean): True if exists, otherwise False.
	'''
	return True if key in os.environ else False

def get_Env(key_name=str):
	'''Get from environment variables.

		Args:
			key_name (str): Name of the environment variable.

		Return:
			(str): Value of the environment variable.
	'''
	return os.getenv(key_name, "")

def set_Env(key_name=str, value_name=str):
	'''Register a new key and value into environment variables.

		Args:
			key_name (str): Name to register in environment variable.
			value_name (str): Value to store in the Name.
		
		Return: None
	'''
	os.environ[key_name] = value_name

def del_Env(key_name=str):
	'''Delete from environment variables.

		Args:
			key_name (str): Name of environment variable.

		Return: None
	'''
	if is_Env(key_name):
		del os.environ[key_name]

def check_project_file(projectfile=str()):
	_projectfile = str()
	if projectfile:
		_projectfile = os.path.normpath(projectfile)
		if os.path.isfile(_projectfile) and _projectfile.lower().endswith(OB_EXTENSION):
			set_Env(key_name=BaseENV.PROJECT_FILE,value_name=_projectfile)
			message = "Project Loaded from File Path"
			print (f"{message}".center(len(message)+10, "-"))
			return _projectfile
	return ""

def check_project_env():
	result = get_Env(key_name=BaseENV.PROJECT_FILE)
	if result:
		_projectfile = os.path.normpath(result)
		if os.path.isfile(_projectfile) and _projectfile.lower().endswith(OB_EXTENSION):
			_projectfile = os.path.normpath(result)
			message = "Project Loaded from Environment Variable"
			print (f"{message}".center(len(message)+10, "-"))
			return _projectfile
	else:
		set_Env(key_name=BaseENV.PROJECT_FILE, value_name="")
	return ""