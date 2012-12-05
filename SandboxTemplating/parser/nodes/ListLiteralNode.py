from ..Node import Node

class ListLiteralNode(Node):
	def __init__( self, literal=None ):
		if literal:
			self.literal = [literal]
		else:
			self.literal = []
	
	def add( self, other ):
		self.literal += other.literal
		return self
	
	def __json__( self ):
		return {
			'nodeType': 'ListLiteralNode',
			'literal': [x.__json__() for x in self.literal]
		}