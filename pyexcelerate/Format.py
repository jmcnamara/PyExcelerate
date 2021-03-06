from . import six

class Format(object):
	def __init__(self, format=None):
		self._id = 0 # autopopulated by workbook.py
		self.format = format
		
	def __eq__(self, other):
		if other is None:
			return self.is_default
		else:
			return self.format == other.format
	
	def __hash__(self):
		return hash(self.format)
	
	@property
	def is_default(self):
		return self == Format()

	@property
	def id(self):
		return self._id
	
	@id.setter
	def id(self, value):
		self._id = value + 1000
		
	def get_xml_string(self):
		return "<numFmt numFmtId=\"%d\" formatCode=\"%s\"/>" % (self.id, self.format)
		
	def __str__(self):
		return "Format: %s" % self.format