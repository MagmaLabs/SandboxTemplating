from ..Node import Node

from functools import partial

class InfixOperatorNode(Node):
	@classmethod
	def withOperator( cls, operator ):
		return partial( InfixOperatorNode, operator=operator )
	
	def __init__( self, leftOperand, rightOperand, operator ):
		self.leftOperand = leftOperand
		self.rightOperand = rightOperand
		self.operator = operator
	
	def __json__( self ):
		return {
			'nodeType': 'InfixOperatorNode',
			'leftOperand': self.leftOperand.__json__( ),
			'rightOperand': self.rightOperand.__json__( ),
			'operator': self.operator,
		}