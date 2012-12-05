from ..Node import Node

class NumericLiteralNode(Node):
	def __init__( self, literal ):
		if '.' in literal:
			self.literal = float(literal)
		else:
			self.literal = int(literal)
	
	def negate( self ):
		self.literal = -self.literal
	
	def __json__( self ):
		return {
			'nodeType': 'NumericLiteralNode',
			'literal': self.literal
		}