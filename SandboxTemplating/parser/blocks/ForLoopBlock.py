from ..Block import Block

from ..nodes.NodeListNode import NodeListNode
from ..nodes.InfixOperatorNode import InfixOperatorNode
from ..nodes.ContextVariableNode import ContextVariableNode

class ForLoopBlock(Block):
	startTagNames = [ 'for' ]
	
	@classmethod
	def parseBlock( cls, startTag, parseUntil ):
		# this is a hack
		arguments = startTag.arguments
		assert len(arguments) == 1
		argument = arguments[0]
		assert isinstance(argument, InfixOperatorNode)
		assert argument.operator == 'in'
		needle = argument.leftOperand
		haystack = argument.rightOperand
		
		assert isinstance(needle, ContextVariableNode)
		needle = needle.variableName
		
		# get the contents of the loop
		loopNodes = list( parseUntil( ['empty', 'endfor'] ) )
		
		loopNodes, endFor = loopNodes[:-1], loopNodes[-1]
		
		if endFor.name == 'empty':
			emptyNodes = list( parseUntil( ['endfor'] ) )

			emptyNodes, endFor = emptyNodes[:-1], emptyNodes[-1]
		else:
			emptyNodes = []
		
		assert endFor.name == 'endfor'
		
		return ForLoopBlock( needle, haystack, loopNodes, emptyNodes )
	
	def __init__( self, needle, haystack, loopNodes, emptyNodes ):
		self.needle = needle
		self.haystack = haystack
		self.loopNodes = NodeListNode( loopNodes )
		self.emptyNodes = NodeListNode( emptyNodes )
	
	def __json__( self ):
		return {
			'nodeType': 'ForLoopBlock',
			'needle': self.needle,
			'haystack': self.haystack.__json__( ),
			'loopNodes': self.loopNodes.__json__( ),
			'emptyNodes': self.emptyNodes.__json__( ),
		}