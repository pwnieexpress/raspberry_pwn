'''
This file is part of VoIPER.

VoIPER is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

VoIPER is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with VoIPER.  If not, see <http://www.gnu.org/licenses/>.

Copyright 2008, http://www.unprotectedhex.com
Contact: nnp@unprotectedhex.com
'''

from replay import *

if __name__ == '__main__':

    # test Parser.extract_packet() with <allOneline> and <hex> expansion
    test_file = open('test_files/test_extract_packet', 'r')
    test_contents = test_file.read()
    test_file.close()
    parser = Parser('test_files')
    ret = parser._Parser__extract_packet(open('rfc4475_tests/unreason.valid', 'r'))

    assert(ret == test_contents)

    # test Parser.extract_packet() with <repeat>
    test_file = open('test_files/test_extract_packet_repeat', 'r')
    test_contents = test_file.read()
    test_file.close()
    parser = Parser('test_files')
    ret = parser._Parser__extract_packet(open('rfc4475_tests/scalar02.invalid', 'r'))

    assert(ret == test_contents)

    # test Parser.parse()
    dictionary = parser.parse()

    test_file = open('test_files/test_extract_packet', 'r')
    test_contents = test_file.read()
    test_file.close()
    
    assert(len(dictionary['valid']) == 1)
    assert(dictionary['valid'][0].name == 'unreason.valid')
    assert(dictionary['valid'][0].data == test_contents)

    test_file = open('test_files/test_extract_packet_repeat', 'r')
    test_contents = test_file.read()
    test_file.close()
    
    assert(len(dictionary['invalid']) == 1)
    assert(dictionary['invalid'][0].name == 'scalar02.invalid')
    assert(dictionary['invalid'][0].data == test_contents)

    '''
    # test Parser.__extract_invite_details
    test_file = open('test_files/wsinv_test', 'r')
    msg = test_file.read()
    
    print parser._Parser__extract_invite_details(msg)
    '''
