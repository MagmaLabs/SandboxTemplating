class PeekIter(object):
	"""Wraps an interable, safely allowing peeking at the next element."""
	
	def __init__( self, iterable ):
		self._iterable = iter(iterable)
		self._next_item = None
	
	def __iter__( self ):
		return self
	
	def __next__( self ):
		return self.next( )
	
	def next( self ):
		"""Consumes and returns the next item in the iterable.
		
		Raises StopIteration when the iterable is exhausted."""
		
		if self._next_item is not None:
			tmp = self._next_item
			self._next_item = None
			return tmp
		else:
			data = self._iterable.next( )
			return data
	
	def peek( self ):
		"""Returns the next item in the iterable, but does not consume it.
		That is, a subsequent call to .next( ) will return the same item.
		
		Raises StopIteration when the iterable is exhausted."""
		
		if self._next_item is not None:
			return self._next_item
		next = self.next( )
		self._next_item = next # save item for next call
		return next
	
	def whileMatches( self, matches ):
		"""Consumes and returns items as long as the precondition matches.
		
		The delegate is called for each item, and should return a bool."""
		
		while True:
			try:
				token = self.peek( )
			except StopIteration:
				return # run out of data, bail gracefully
			
			if matches( token ):
				yield self.next( ) # eat the token
			else:
				return # different token, bail
	
	def untilMatches( self, matches ):
		"""Consumes and returns items as long as the precondition does't match.
		
		The delegate is called for each item, and should return a bool."""
		
		return self.whileMatches( lambda x: not matches( x ) )