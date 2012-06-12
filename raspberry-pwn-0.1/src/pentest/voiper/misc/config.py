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

def parse_config(f_name):
    in_file = open(f_name, 'r')
    res_dict = {}

    for num, line in enumerate(in_file):
        line = line.strip()
        if line.startswith('#') or len(line) == 0: continue
        if line.find('=') == -1: return (None, num)
        parts = line.split('=')
        if len(parts) != 2: return (None, num)
        part0 = parts[0].strip()
        part1 = parts[1].strip()
        
        if part1.lower() == 'false':
            part1 = False
        elif part1.lower() == 'true':
            part1 = True

        res_dict[part0] = part1

    in_file.close()

    return (res_dict, 0)
