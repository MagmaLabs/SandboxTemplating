from ..Visitor import Visitor
from ..nodes import *

from ..blocks.BlockBlock import BlockBlock

class TransformExtendsVisitor(Visitor):
	def visitTemplateNode( self, node ):
		resultName = None
		resultBlocks = {}
		
		for child in node.nodes:
			if isinstance(child, TagNode) and child.name == 'extends':
				assert len(child.arguments) == 1
				parentName = child.arguments[0]
				assert isinstance(parentName, StringLiteralNode)
				parentName = parentName.literal
				
				resultName = parentName
			elif isinstance(child, BlockBlock):
				resultBlocks[child.name] = child
		
		if resultName is not None:
			return resultName, resultBlocks