from ..Node import Node

class StringLiteralNode(Node):
	def __init__( self, literal ):
		self.literal = unicode(literal)
	
	def __json__( self ):
		return {
			'nodeType': 'StringLiteralNode',
			'literal': self.literal
		}