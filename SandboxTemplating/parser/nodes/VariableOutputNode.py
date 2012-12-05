from ..Node import Node

class VariableOutputNode(Node):
	def __init__( self, expression ):
		self.expression = expression
		
	def __json__( self ):
		return {
			'nodeType': 'VariableOutputNode',
			'expression': self.expression.__json__( ),
		}