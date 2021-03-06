from . import six
from . import Font
from . import Fill
from . import Format

class Style(object):
	_DEFAULT_FORMAT = Format.Format()
	_DEFAULT_FILL = Fill.Fill()
	_DEFAULT_FONT = Font.Font()
	def __init__(self):
		self._font = None
		self._fill = None
		self._format = None

	@property
	def is_default(self):
		return not (self._font or self._fill or self._format)

	@property
	def format(self):
		# don't use default because default should be const
		return self._lazy_get('_format', Format.Format())
	
	@format.setter
	def format(self, value):
		self._lazy_set('_format', Style._DEFAULT_FORMAT, value)
	
	@property
	def font(self):
		return self._lazy_get('_font', Font.Font())
	
	@font.setter
	def font(self, value):
		self._lazy_set('_font', Style._DEFAULT_FONT, value)
	
	@property
	def fill(self):
		return self._lazy_get('_fill', Fill.Fill())
	
	@fill.setter
	def fill(self, value):
		self._lazy_set('_fill', Style._DEFAULT_FILL, value)
	
	def get_xml_string(self):
		# Precondition: Workbook._align_styles has been run.
		# Be careful when using this function as id's may be inaccurate if precondition not met.
		tag = []
		if not self.format.is_default:
			tag.append("numFmtId=\"%d\"" % self.format.id)
		if not self.font.is_default:
			tag.append("applyFont=\"1\" fontId=\"%d\"" % (self.font.id))
		if not self.fill.is_default:
			tag.append("applyFill=\"1\" fillId=\"%d\"" % (self.fill.id + 1))
		return "<xf xfId=\"0\" borderId=\"0\" %s/>" % (" ".join(tag))
		
	def __hash__(self):
		return hash((hash(self._font), hash(self._fill), hash(self._format)))
	
	def __eq__(self, other):
		if other is None:
			return self.is_default
		else:
			return self._to_tuple() == other._to_tuple()
	
	def _to_tuple(self):
		return (self._font, self._fill, self._format)
	
	def _lazy_get(self, attribute, default):
		value = getattr(self, attribute)
		if not value:
			setattr(self, attribute, default)
			return default
		else:
			return value
			
	def _lazy_set(self, attribute, default, value):
		if value == default:
			setattr(self, attribute, None)
		else:
			setattr(self, attribute, value)
			
	def __str__(self):
		return "%s %s %s" % (self.font, self.fill, self.format)
		
	def __repr__(self):
		return "<%s>" % self.__str__()