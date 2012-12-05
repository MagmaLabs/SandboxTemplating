from ..Node import Node

from functools import partial

class UnaryOperatorNode(Node):
	@classmethod
	def withOperator( cls, operator ):
		return partial( UnaryOperatorNode, operator=operator )
	
	def __init__( self, operand, operator ):
		self.operand = operand
		self.operator = operator
		
	def __json__( self ):
		return {
			'nodeType': 'UnaryOperatorNode',
			'operand': self.operand.__json__( ),
			'operator': self.operator,
		}