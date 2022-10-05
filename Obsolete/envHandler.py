import os

OB_EXTENSION = '.ob'
PUBLISH_EXTENSION = ".obp"
PUBLISH_FILE = f"Asset{PUBLISH_EXTENSION}"

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

def is_file_valid(filePath=str(), extension=str()):
	"""check file exists with correct extension.

		Parameters:
		filePath (str) - absolute path of file.
		extension (str) - extension of the file.

		Returns: validation of filepath
		Return Type: bool
	"""
	return filePath.lower().endswith(extension.lower()) and os.path.exists(filePath)

def is_project_file(filePath=str()):
	"""check if file exists with correct Obsolete project extension.

		Parameters:
		filePath (str) - absolute path of Obsolete project file.

		Returns: validation of filepath
		Return Type: bool
	"""
	return is_file_valid(filePath=filePath, extension=OB_EXTENSION)

def is_publish_file(filePath=str()):
	"""check if file exists with correct Obsolete publish extension.

		Parameters:
		filePath (str) - absolute path of Obsolete publish file.

		Returns: validation of filepath
		Return Type: bool
	"""
	return is_file_valid(filePath=filePath, extension=PUBLISH_EXTENSION)

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

def generate_Path(keys=[], validKeys=[]):
	if validKeys:
		return "/".join([a if a not in validKeys else f"${a}" for a in keys])
	else:
		return "/".join([f"${a}" for a in keys])

def expand_path(path=str()):
	return os.path.expandvars(path)