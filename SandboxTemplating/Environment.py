import os

from SandboxTemplating.Template import Template

class Environment(object):
	def __init__( self, basePath, tags=None, blocks=None ):
		self.basePath = basePath
		self.tags = tags or {}
		self.blocks = blocks or []
	
	def loadTemplate( self, templateName ):
		# FIXME: make even more sure this is safe
		assert '..' not in templateName
		
		path = os.path.join( self.basePath, templateName )
		
		data = open( path, 'rb' ).read( )
		
		return Template.fromString( self, data, name=templateName )
		
	def templateFromString( self, data, templateName=None ):
		return Template.fromString( self, data, name=templateName )