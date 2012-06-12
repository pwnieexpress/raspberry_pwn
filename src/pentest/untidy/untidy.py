'''
untidy.py

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

DEBUG = False

import fuzzingFunctions
import re

class xmlFuzzer:
	'''
	This class fuzzes an xml string.
	
	@author: Andres Riancho ( andres.riancho@gmail.com )
	'''
	def __init__(self):
		self._stopfuzz = False
		self._output = ''
		self._current = 0
		self._startFrom = []
		
		#self._repetitions = [ 2, 3, 7, 8, 9, 15, 16, 17, 31, 32, 33, 63, 64, 65,
		#127, 128, 129, 254, 255, 256, 511, 512, 513, 1023, 1024, 1025, 2047,
		#2048, 2049, 4095, 4096, 4097, 10000, 10000 ]
		self._repetitions = [ 30, 34 ]
		
		self._ff = fuzzingFunctions.fuzzingFunctions()
	
	def setRepetitions( self , rep ):
		self._repetitions = rep
	
	def _toList( self, xmlString ):
		'''
		This method separates an xml in a "line by line" form.
		
		Example:
		xmlString: "<xml a="b">f00</xml>"
		result: [ '<xml a="b">' , 'f00', '</xml>']
		
		REX/Python
		
		Based on Robert D. Cameron's REX/Perl 1.0.
		
		Original copyright notice follows:
		
		REX/Perl 1.0
		
		Robert D. Cameron "REX: XML Shallow Parsing with Regular Expressions",
		Technical Report TR 1998-17, School of Computing Science, Simon Fraser
		University, November, 1998.
		Copyright (c) 1998, Robert D. Cameron.
		The following code may be freely used and distributed provided that
		this copyright and citation notice remains intact and that modifications
		or additions are clearly identified.
	
		@parameter xmlString: A string representation of the xml
		@return: A list of strings.
		'''
		TextSE = "[^<]+"
		UntilHyphen = "[^-]*-"
		Until2Hyphens = UntilHyphen + "(?:[^-]" + UntilHyphen + ")*-"
		CommentCE = Until2Hyphens + ">?"
		UntilRSBs = "[^\\]]*](?:[^\\]]+])*]+"
		CDATA_CE = UntilRSBs + "(?:[^\\]>]" + UntilRSBs + ")*>"
		S = "[ \\n\\t\\r]+"
		NameStrt = "[A-Za-z_:]|[^\\x00-\\x7F]"
		NameChar = "[A-Za-z0-9_:.-]|[^\\x00-\\x7F]"
		Name = "(?:" + NameStrt + ")(?:" + NameChar + ")*"
		QuoteSE = "\"[^\"]*\"|'[^']*'"
		DT_IdentSE = S + Name + "(?:" + S + "(?:" + Name + "|" + QuoteSE +"))*"
		MarkupDeclCE = "(?:[^\\]\"'><]+|" + QuoteSE + ")*>"
		S1 = "[\\n\\r\\t ]"
		UntilQMs = "[^?]*\\?+"
		PI_Tail = "\\?>|" + S1 + UntilQMs + "(?:[^>?]" + UntilQMs + ")*>"
		DT_ItemSE = "<(?:!(?:--" + Until2Hyphens + ">|[^-]" + MarkupDeclCE + ")|\\?" + Name + "(?:" + PI_Tail + "))|%" + Name + ";|" + S
		DocTypeCE = DT_IdentSE + "(?:" + S + ")?(?:\\[(?:" + DT_ItemSE + ")*](?:" + S + ")?)?>?"
		DeclCE = "--(?:" + CommentCE + ")?|\\[CDATA\\[(?:" + CDATA_CE + ")?|DOCTYPE(?:" + DocTypeCE + ")?"
		PI_CE = Name + "(?:" + PI_Tail + ")?"
		EndTagCE = Name + "(?:" + S + ")?>?"
		AttValSE = "\"[^<\"]*\"|'[^<']*'"
		ElemTagCE = Name + "(?:" + S + Name + "(?:" + S + ")?=(?:" + S + ")?(?:" + AttValSE + "))*(?:" + S + ")?/?>?"
		MarkupSPE = "<(?:!(?:" + DeclCE + ")?|\\?(?:" + PI_CE + ")?|/(?:" + EndTagCE + ")?|(?:" + ElemTagCE + ")?)"
		XML_SPE = TextSE + "|" + MarkupSPE		
		
		res = re.findall(XML_SPE, xmlString)
		res = [ x for x in res if x !='\n' ]
		
		return res
		
	def _getFuzzFunctions( self ):
		'''
		@return: A list of fuzzing functions.
		'''
		if DEBUG:
			self._repetitions = [ 5, 28 ]
			return self._ff._getTestFuzzFunctions()
		else:
			return self._ff._getFuzzFunctions()
	
	def _generateIterator( self, fuzzedItems ):	
		'''
		@return: This method generates and iterator object that returns a string 
		representation of a fuzzed xml on every call to next()
		'''
		class iterator:
			def __init__( self, fuzzedItems ):
				self._fi = fuzzedItems
				
				# Init the counter
				self._counter = []
				for f00 in range( len(self._fi) ):
					self._counter.append( 1 )
					
				# This fixes the first call to next()
				self._counter[ len( self._fi ) -1 ] = 0
				
				self._stopIteration = False
				
			def next( self ):
				if self._stopIteration:
					raise StopIteration
				else:
					# First we increment the counter
					self._incrementCounter()
					
					# Now we fetch the data from the self._fi based on the counter
					itemList = self._fetchData()
					
					# Finally the items are joined into a string and returned
					xmlStr = ''.join( itemList )
					return xmlStr
				
			def _fetchData( self ):
				itemList = []
				# Believe it or not, this for loop worked the first time I wrote it.
				for pos in range( len( self._counter ) ):
					itemList.append( self._fi[ pos ][ self._counter[pos] -1 ] )
				# I dont care if you dont believe me :P
				
				return itemList
				
			def _incrementCounter( self ):
				# this is ugly !
				# It is basically an abacus implementation in python
				self._counter[ len(self._counter) -1 ] += 1
				
				rpositions = range( len(self._counter) )
				rpositions.reverse()
				for position in rpositions:
					if self._counter[ position ] > len( self._fi[ position ] ):
						# I count from 1, still a human.
						self._counter[ position ] = 1
						self._counter[ position - 1 ] += 1
					
				# If all counters are full, then set a flag that indicates that
				# the iterator has no more items inside.
				eq = True
				for c in range( len( self._counter ) ):
					if self._counter[ c ] != len( self._fi[ c ] ):
						eq = False
				
				if eq:
					self._stopIteration = True
					
			def __iter__( self ):
				# Not sure if this is ok, it works... but... is it ok ?
				return self
				
		it = iterator( fuzzedItems )
		return it
	
	def fuzz( self, xmlString ):
		'''
		This method does all the work
		
		@parameter xmlString: A string representation of the xml to fuzz
		@return: An iterator object that returns a fuzzed xml on every call to next()
		'''
		xmlList = self._toList( xmlString )
		
		fuzzedXmlItems = []
		for xmlItem in xmlList:
			fuzzedItems = []
			for f in self._getFuzzFunctions():
				# The repetitions indicate how many times the ff will repeat the pattern
				# it is configured to repeat.
				fuzzedItem = apply( f, (xmlItem, self._repetitions ) )
				if fuzzedItem != None:
					fuzzedItems.extend( fuzzedItem  )
				
			fuzzedXmlItems.append ( fuzzedItems )
			
		iter = self._generateIterator( fuzzedXmlItems )
		return iter

		
if __name__ ==  '__main__' :

	xmlString = '<xml attr1="a"><a>f00!</a></xml>'

	xf = xmlFuzzer()
	xf.setRepetitions( [3,30,60] )
	iter = xf.fuzz( xmlString )

	for i in iter:
		print i
