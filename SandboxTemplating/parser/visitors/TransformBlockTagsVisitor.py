from ..Visitor import Visitor
from ..nodes import *

from ...utils.PeekIter import PeekIter

from ..blocks.ForLoopBlock import ForLoopBlock
from ..blocks.IfBlock import IfBlock
from ..blocks.BlockBlock import BlockBlock

class TransformBlockTagsVisitor(Visitor):
	def __init__( self, env ):
		self.env = env
	
	def getBlocks( self ):
		return [ForLoopBlock, IfBlock, BlockBlock] + self.env.blocks
	
	def visitNodeListNode( self, node ):
		self.nodes = PeekIter( node.nodes )
		
		newNodes = list( self.transformUntil( [] ) )
		
		node.nodes = newNodes
	
	def transformUntil( self, endTagNames ):
		for child in self.nodes:
			matched = False
			if isinstance(child, TagNode):
				if child.name in endTagNames:
					yield child
					return
				for block in self.getBlocks( ):
					if child.name in block.startTagNames:
						matched = True
						yield block.parseBlock( child, self.transformUntil )
			if not matched:
				yield child
			