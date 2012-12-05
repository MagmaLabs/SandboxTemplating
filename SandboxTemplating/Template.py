from SandboxTemplating.parser.Grammar import Grammar

from SandboxTemplating.parser.renderers.SandboxRenderer import SandboxRenderer
from SandboxTemplating.parser.context.Context import Context

from SandboxTemplating.parser.visitors.TransformBlockTagsVisitor import TransformBlockTagsVisitor
from SandboxTemplating.parser.visitors.TransformExtendsVisitor import TransformExtendsVisitor

from StringIO import StringIO

from parcon import Invalid

class Template(object):
	@classmethod
	def fromString( cls, env, data, name=None ):
		return Template( env, data, name )
	
	def __init__( self, env, data, name ):
		self.env = env
		self.name = name
		
		self.doc = Grammar.parse_string( data, whitespace=Invalid() )
		
		self.doc.accept( TransformBlockTagsVisitor( self.env ) )
		
		self.parent = None
		parenting = self.doc.accept( TransformExtendsVisitor( ) )
		if parenting is not None:
			parentName, childBlocks = parenting
			self.parent = env.loadTemplate( parentName )
			self.childBlocks = childBlocks
	
	def __repr__( self ):
		return '<Template %r>' % self.name
	
	def render( self, contextData ):
		s = StringIO()
		self.renderf( s, contextData )
		return s.getvalue()
	
	def renderf( self, f, contextData ):
		context = Context( contextData )
		self._renderf( f, context )
	
	def _renderf( self, f, context ):
		if self.parent is None:
			# render this template
			renderer = SandboxRenderer( self.env, f, context )
			self.doc.accept( renderer )
		else:
			# render the parent template
			context.setChildBlocks( self.childBlocks, replace=False )
			self.parent._renderf( f, context )
	
	def acceptVisitor( self, visitor ):
		self.doc.accept( visitor )