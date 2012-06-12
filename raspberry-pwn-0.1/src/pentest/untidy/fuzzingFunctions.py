'''
fuzzingFunctions.py

Copyright 2006 Andres Riancho

This file is part of untidy, untidy.sourceforge.net .

untidy is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2 of the License.

untidy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with untidy; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

'''
import re

class fuzzingFunctions:
	'''
	This class has a collection of fuzzing funcions for xml tags, text and attrs.
	
	@author: Andres Riancho ( andres.riancho@gmail.com )
	'''
	def __init__(self):
		self._ffTestList = [ self.ff0 ]
		
	def _getTestFuzzFunctions( self ):
		'''
		@return: A list of fuzzing functions for testing.
		'''
		return self._ffTestList
		
	def _getFuzzFunctions( self ):
		'''
		@return: A list of fuzzing functions.
		'''
		res = []
		i = 0
		try:
			while True:
				# pure python love :P
				res.append( getattr( self, 'ff'+str(i) ) )
				i += 1
		except:
			# I dont care
			pass
			
		return res

###############################################
#																									    #
#				These are the fuzzing functions, the Core.				#
#																						    			#
###############################################

	def ff0( self, xmlItem, repetitions=[] ):
		'''
		Return the item without changes
		'''
		return [xmlItem,]

######################################
#																					#
#				This set of ff's break the XML sintax		#
#																					#
######################################	
	
	def ff1( self, xmlItem, repetitions=[] ):
		'''
		Matches the opening <, replace with '>'*repetitions
		'''
		result = []
		p = re.compile('^<')
		for rep in repetitions:
			if p.match( xmlItem ):
				fuzzedItem = p.sub('>'*rep , xmlItem )
				result.append( fuzzedItem )
		return result
	
	def ff2( self, xmlItem, repetitions=[] ):
		'''
		If repetitions=2 and xmlItem='<foo>'
		this ff returns '<foo><<>>'
		'''
		result = []
		for rep in repetitions:
			fuzzedItem = xmlItem
			for i in range( rep ):
				fuzzedItem += '<'
			for i in range( rep ):
				fuzzedItem += '>'
			result.append( fuzzedItem )
		return result
		
	def ff3( self, xmlItem, repetitions=0 ):
		result = []
		for rep in repetitions:
			fuzzedItem = xmlItem
			fuzzedItem += 'A'*rep
			result.append( fuzzedItem )
		return result

	def ff4( self, xmlItem, repetitions=[] ):
		result = []
		for rep in repetitions:
			result.append(xmlItem*rep)
		return result
		
	def ff5( self, xmlItem, repetitions=0 ):
		return ['',]

######################################
#																								#
#				This set of ff's fuzz the XML ( mostly ) without		#
#									breaking XML sintax								#
#																								#
######################################	

	def _sameType( self, charA, charB ):
		if charA.isalpha() and charB.isalpha():
			return True
		elif charA.isdigit() and charB.isdigit():
			return True		
		else:
			return False
		
	def ff6( self, xmlItem, repetitions=[] ):
		'''
		Lots of fuzzing going on here! :)
		Some of this fuzzed XML's will be valid, some not.
		'''
		result = []
		last = ''
		pointer = 0
		for char in xmlItem:
			if not self._sameType( last, char ):
				for rep in repetitions:
					fuzzedItem = xmlItem[ : pointer ]
					
					# This helps me identify the bugs on the remote side
					if char.isalpha():
						fuzzedItem += 'A'* rep
					elif char.isdigit():
						fuzzedItem += '1'* rep
					else:
						fuzzedItem += char* rep
						
					fuzzedItem += xmlItem[ pointer : ]
					result.append( fuzzedItem )
			pointer += 1
			last = char
			
		return result
		
