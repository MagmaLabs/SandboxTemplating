from ..exceptions import ObjectNotAvailable

from .IContextItem import IContextItem

def isiterable(obj):
	try:
		iterator = iter(obj)
	except TypeError:
		return False
	else:
		return True

class ContextSafety(object):
	def __init__( self, value ):
		self._value = value
	
	def __context_get__( self, context ):
		value = self._value
		
		if IContextItem.isImplementedBy( value ):
			value = value.getTemplateValue( )
		
		if isinstance(value, (basestring, int, float, bool)) or value is None:
			return value
		elif isinstance(value, dict):
			safe = {}
			for k,v in value.iteritems( ):
				safe[unicode(k)] = ContextSafety(v)
			return safe
		elif isiterable(value):
			return list( ContextSafety(v) for v in value )
		else:
			raise ObjectNotAvailable
