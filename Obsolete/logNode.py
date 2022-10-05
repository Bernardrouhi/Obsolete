from datetime import datetime, timezone

class LogKeys():
	VERSION = "Version"
	VARIANT = "Variant"
	USER = "User"
	WORKFILES = "WorkFiles"
	PUBLISHFILES = "PublishFiles"
	RECORD = "Record"
	APP = "Application"
	DESCRIPTION = "Description"

class LogObject(object):
	"""Handle Publish Log object"""
	def __init__(self, Version=int(1), Variant=str(), User=str(), WorkFiles=list(), 
				 PublishFiles=list(), Application=str(), Record=float(), Description=str()):
		self._data = self.LOG_METADATA()
		if isinstance(Version, int) and Version : self.set_Version(Version=Version)
		if isinstance(Variant, str) and Variant : self.set_Variant(Variant=Variant)
		if isinstance(User, str) and User : self.set_User(User=User)
		if isinstance(WorkFiles, (list, tuple)) and WorkFiles : self.set_WorkFiles(WorkFiles=WorkFiles)
		if isinstance(PublishFiles, (list, tuple)) and PublishFiles : self.set_PublishFiles(PublishFiles=PublishFiles)
		if isinstance(Application, str) and Application : self.set_Application(Application=Application)
		if isinstance(Record, float) and Record : self.set_Record(Record=Record)
		if isinstance(Description, str) and Description : self.set_Description(Description=Description)

	@staticmethod
	def LOG_METADATA():
		"""Log default metadata structure"""
		return {
			LogKeys.VERSION: int(1),
			LogKeys.VARIANT: str(),
			LogKeys.USER: str(),
			LogKeys.WORKFILES: list(),
			LogKeys.PUBLISHFILES: list(),
			LogKeys.RECORD: float(datetime.now(timezone.utc).timestamp()),
			LogKeys.APP:str(),
			LogKeys.DESCRIPTION:str()
		}.copy()

	def get_Version(self):
		"""Get the the log version.

			Returns: log version.
			Return Type: str
		"""
		return self._data[LogKeys.VERSION]
	def set_Version(self, Version=int()):
		"""Set the the log version.

			Parameters:
			Version (int) - Version number.
		"""
		self._data[LogKeys.VERSION] = Version

	def get_Variant(self):
		"""Get the name of the variant.

			Returns: Variant name.
			Return Type: str
		"""
		return self._data[LogKeys.VARIANT]
	def set_Variant(self, Variant=str()):
		"""Set the the log variant.

			Parameters:
			Variant (str) - Variant name.
		"""
		self._data[LogKeys.VARIANT] = Variant

	def get_User(self):
		"""Get the name of user that created the log.

			Returns: Name of user.
			Return Type: str
		"""
		return self._data[LogKeys.USER]
	def set_User(self, User=str()):
		"""Set the user name that creating the log.

			Parameters:
			User (str) - User name.
		"""
		self._data[LogKeys.USER] = User

	def get_WorkFiles(self):
		"""Get the list of work files.

			Returns: Work files.
			Return Type: list
		"""
		return self._data[LogKeys.WORKFILES]
	def set_WorkFiles(self, WorkFiles=list()):
		"""Set the list of user's workfiles.

			Parameters:
			WorkFiles (list) - User's workfiles.
		"""
		self._data[LogKeys.WORKFILES] = WorkFiles

	def get_PublishFiles(self):
		"""Get the list of publish files.

			Returns: Published files.
			Return Type: list
		"""
		return self._data[LogKeys.PUBLISHFILES]
	def set_PublishFiles(self, PublishFiles=list()):
		"""Set the list of published files.

			Parameters:
			PublishFiles (list) - published files.
		"""
		self._data[LogKeys.PUBLISHFILES] = PublishFiles

	def get_Record(self, asObject=bool(False)):
		"""Get the recorded log.

			To get the date e.g. get_Record(asObject=True).date()
			To get the Time e.g. get_Record(asObject=True).time()

			Returns: Record date and time in UTC.
			Return Type: float
		"""
		if asObject:
			return datetime.fromtimestamp(self.get_Record(), tz=timezone.utc)
		else:
			return self._data[LogKeys.RECORD]
	def set_Record(self, Record=float()):
		"""Set the log created date and time in UTC.

			e.g. datetime.datetime.now(timezone.utc).timestamp()

			Parameters:
			Record (float) - Date and time timestamp.
		"""
		self._data[LogKeys.RECORD] = Record

	def get_Application(self):
		"""Get the name of the application that created the log.

			Returns: Application name.
			Return Type: str
		"""
		return self._data[LogKeys.APP]
	def set_Application(self, Application=str()):
		"""Set the name of application that creating the log.

			Parameters:
			Application (str) - Name of application.
		"""
		self._data[LogKeys.APP] = Application

	def get_Description(self):
		"""Get log description.

			Returns: description of publish.
			Return Type: str
		"""
		return self._data[LogKeys.DESCRIPTION]
	def set_Description(self, Description=str()):
		"""Set the description of the log.

			Parameters:
			Description (str) - Log's Description.
		"""
		self._data[LogKeys.DESCRIPTION] = Description

	def toJSON(self):
		"""Serialized the object into dictionary.

			Returns: get a dictionary of LogObject.
			Returns Types: dict
		"""
		return self._data
