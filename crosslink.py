#!/usr/bin/python3

#    Automated VDR repository mirror and wiki page generator
#    Copyright © 2023  Manuel Reimer <manuel.reimer@gmx.de>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re

def crosslink(content):
    # vdr(1)
    content = re.sub(r'([,>])(?:<strong>)?vdr(?:</strong>)?\(1\)([<,])',
                     r'\1\n[vdr(1)](VDR-command-reference)\2', content)

    # vdr(5)
    content = re.sub(r'([ >])(?:<strong>)?vdr(?:</strong>)?\(5\)([ \),<])',
                     r'\1\n[vdr(5)](VDR-file-formats-and-conventions)\2', content)

    # svdrpsend(1)
    content = re.sub(r'([,])(?:<strong>)?svdrpsend(?:</strong>)?\(1\)([<])',
                     r'\1\n[svdrpsend(1)](svdrpsend-command-reference)\2', content)

    # 'commands.conf'
    content = re.sub(r'([\'])commands.conf([\'])',
                     r'\1\n[commands.conf](VDR-file-formats-and-conventions#commands)\2', content)

    return content
