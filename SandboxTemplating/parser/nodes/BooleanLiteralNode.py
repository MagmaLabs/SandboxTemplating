from ..Node import Node

class BooleanLiteralNode(Node):
	def __init__( self, which ):
		self.value = bool( which.lower() == 'true' )
	
	def __json__( self ):
		return {
			'nodeType': 'BooleanLiteralNode',
			'value': self.value,
		}