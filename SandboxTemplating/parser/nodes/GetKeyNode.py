from ..Node import Node

from functools import partial

class GetKeyNode(Node):
	@classmethod
	def withFutureTerm( cls ):
		return partial( GetKeyNode, None )
	
	def __init__( self, term, keyExpression ):
		self.term = term
		self.keyExpression = keyExpression
	
	def setLeftOperand( self, operand ):
		self.term = operand

	def __json__( self ):
		return {
			'nodeType': 'GetKeyNode',
			'term': self.term.__json__( ) if not isinstance(self.term, basestring) else self.term,
			'keyExpression': self.keyExpression.__json__( ),
		}