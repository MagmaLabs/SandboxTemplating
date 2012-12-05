from interfaces import *

class IContextItem(interface):
	def getTemplateValue( self ):
		"""Represents this class as a template-safe type."""
		pass