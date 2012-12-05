from ..Node import Node

class MarkupNode(Node):
	def __init__( self, data ):
		self.markup = unicode( u''.join( data ) )
		
	def __json__( self ):
		return {
			'nodeType': 'MarkupNode',
			'markup': self.markup,
		}