from ..Node import Node

class NoneLiteralNode(Node):
	def __init__( self, nothing ):
		pass
	
	def __json__( self ):
		return {
			'nodeType': 'NoneLiteralNode',
		}