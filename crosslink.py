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
                     r'\1<a href="VDR-command-reference">vdr(1)</a>\2', content)

    # vdr(5)
    content = re.sub(r'([ >])(?:<strong>)?vdr(?:</strong>)?\(5\)([ \),<])',
                     r'\1<a href="VDR-file-formats-and-conventions">vdr(5)</a>\2', content)

    # svdrpsend(1)
    content = re.sub(r'([,])(?:<strong>)?svdrpsend(?:</strong>)?\(1\)([<])',
                     r'\1<a href="svdrpsend-command-reference">svdrpsend(1)</a>\2', content)

    # 'commands.conf'
    content = re.sub(r'([\'])commands.conf([\'])',
                     r'\1<a href="VDR-file-formats-and-conventions#commands">commands.conf</a>\2', content)

    return content
