from .ContextSafety import ContextSafety

class Context(object):
	def __init__( self, data=None ):
		self.stack = []
		self.push( data )
		
		self.childBlocks = {}
	
	def setChildBlocks( self, childBlocks, replace=False ):
		if replace:
			self.childBlocks.update( childBlocks )
		else:
			for k,v in childBlocks.iteritems( ):
				if k not in self.childBlocks:
					self.childBlocks[k] = v
	
	def push( self, data=None ):
		if data is None:
			data = {}
		assert isinstance(data, dict), "Can only push items of type 'dict' on the context stack"
		self.stack.append( data )
	
	def pop( self ):
		self.stack.pop( )
	
	def get( self, name, *args ):
		for data in reversed( self.stack ):
			if name in data:
				value = data[name]
				if not isinstance(value, ContextSafety):
					return ContextSafety( value )
				else:
					return value
		if len(args) > 0:
			return args[0] # default
		raise KeyError
	
	def set( self, name, value ):
		self.stack[-1][name] = value