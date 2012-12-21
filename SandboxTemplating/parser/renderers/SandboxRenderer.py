import operator

from ..Visitor import Visitor

from markupsafe import Markup, escape

class SandboxRenderer(Visitor):
	automaticallyVisitChildren = False
	
	def __init__( self, env, writer, context ):
		self.env = env
		self.writer = writer
		self.context = context
	
	def _contextUnwrap( self, value ):
		if value is None:
			return None
		elif isinstance(value, (basestring, float, int, dict, list)):
			return value
		else:
			return value.__context_get__( self.context )
	
	def _deepContextUnwrap( self, value ):
		if value is None:
			return None
		elif isinstance(value, (basestring, float, int)):
			return value
		elif isinstance(value, list):
			return [self._deepContextUnwrap(i) for i in value]
		elif isinstance(value, dict):
			return dict((k, self._deepContextUnwrap(v)) for k,v in dict.iteritems())
		else:
			return self._deepContextUnwrap( value.__context_get__( self.context ) )
	
	def visitMarkupNode( self, node ):
		self.writer.write( node.markup )
	
	def visitStringLiteralNode( self, node ):
		return node.literal
	
	def visitNumericLiteralNode( self, node ):
		return node.literal
		
	def visitListLiteralNode( self, node ):
		return [x.accept(self) for x in node.literal]
		
	def visitDictLiteralNode( self, node ):
		items = [(self._contextUnwrap(a.accept(self)), b.accept(self)) for a,b in node.literal]
		for k, v in items:
			assert isinstance(k, basestring)
		
		return dict(items)
	
	def visitBooleanLiteralNode( self, node ):
		return node.value
	
	def visitContextVariableNode( self, node ):
		return self.context.get( node.variableName, None )
	
	def visitGetKeyNode( self, node ):
		term = node.term
		keyExpression = node.keyExpression

		key = self._contextUnwrap( keyExpression.accept( self ) )
		lhs = self._contextUnwrap( term.accept( self ) )
		
		if lhs is None:
			return None
		elif isinstance(lhs, list):
			assert isinstance(key, int), 'List index lookup must be int, not %s.' % (key.__class__.__name__,)
			return lhs[key]
		elif isinstance(lhs, dict):
			assert isinstance(key, basestring), 'Key in dictionary lookup must be string, not %s.' % (key.__class__.__name__,)
			return lhs.get( key, None )
		else:
			assert False, 'Expected dict or list. Cannot get item from %s.' % (lhs.__class__.__name__,)
		
	def visitGetAttributeNode( self, node ):
		term = node.term
		attribute = node.attributeName
		
		assert isinstance(attribute, basestring)
		
		lhs = self._contextUnwrap( term.accept( self ) )
		
		assert isinstance(lhs, dict), 'Getting attribute from type %s, expected dict.' % (lhs.__class__.__name__,)
		
		return lhs.get( attribute, None )
	
	def visitVariableOutputNode( self, node ):
		expression = node.expression
		
		result = self._contextUnwrap( expression.accept( self ) )
		
		self.writer.write( escape( result ) ) # FIXME: only escape if not safe?
	
	def visitUnaryOperatorNode( self, node ):
		operand = self._contextUnwrap( node.operand.accept( self ) )
		if node.operator == 'not':
			return not operand
		elif node.operator == '-':
			return -operand
		elif node.operator == '+':
			return operand
	
	def visitInfixOperatorNode( self, node ):	 
		lhs = self._contextUnwrap( node.leftOperand.accept( self ) )
		rhs = self._contextUnwrap( node.rightOperand.accept( self ) )
		
		if node.operator == 'and':
			return bool(lhs) and bool(rhs)
		elif node.operator == 'or':
			return bool(lhs) or bool(rhs)
		elif node.operator == 'in':
			# TODO: deep unwrap
			return operator.contains( self._deepContextUnwrap(rhs),
			                          self._deepContextUnwrap(lhs) )
		else:
			func = {
				'|': operator.or_,
				'&': operator.and_,
				'^': operator.xor,
				'+': operator.add,
				'-': operator.sub,
				'*': operator.mul,
				'/': operator.div,
				'%': operator.mod,
				'<': operator.lt,
				'>': operator.gt,
				'<=': operator.le,
				'>=': operator.ge,
				'==': operator.eq,
				'!=': operator.ne,
				'<<': operator.lshift,
				'>>': operator.rshift,
			}[node.operator]
			return func( lhs, rhs )
	
	def visitNode( self, node ):
		if hasattr(node, 'render'):
			return node.render( self )
		
		#print '(miss)', node.__class__
		
		# visit children manually in any node we don't explicitly understand
		node.childrenAccept( self )
	
	def visitTagNode( self, node ):
		if node.name in self.env.tags:
			args = [ self._contextUnwrap( a.accept( self ) ) for a in node.arguments ]
			kwargs = dict( (k,self._contextUnwrap( v.accept( self ) )) for k, v in node.keywordArguments.iteritems() )
			
			self.env.tags[node.name]( self.writer, self.context, *args, **kwargs )
			return
		
		self.writer.write( Markup('Unexpected tag \'%s\'') % (escape(node.name),) )
	
	def visitIfBlock( self, node ):
		condition = self._contextUnwrap( node.condition.accept( self ) )
		
		if condition:
			node.ifNodes.accept( self )
		else:
			node.elseNodes.accept( self )
	
	def visitForLoopBlock( self, node ):
		haystack = self._contextUnwrap( node.haystack.accept( self ) )
		assert isinstance(haystack, list)
		
		if not haystack:
			node.emptyNodes.accept( self )
			return
		
		self.context.push( )
		for needle in haystack:
			self.context.set( node.needle, needle )
			node.loopNodes.accept( self )
		self.context.pop( )
	
	def visitBlockBlock( self, node ):
		if node.name in self.context.childBlocks:
			replacement = self.context.childBlocks[node.name]
			replacement.nodes.accept( self )
		else:
			node.nodes.accept( self )