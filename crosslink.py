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
    content = re.sub(r'([,>])(?:<b>)?vdr(?:</b>)?\(1\)([<,])',
                     r'\1<a href="VDR-Command-Reference">vdr(1)</a>\2', content)

    # vdr(5)
    content = re.sub(r'([ >])(?:<b>)?vdr(?:</b>)?\(5\)([ \),<])',
                     r'\1<a href="VDR-File-Formats-and-Conventions">vdr(5)</a>\2', content)

    # svdrpsend(1)
    content = re.sub(r'([,])(?:<b>)?svdrpsend(?:</b>)?\(1\)([<])',
                     r'\1<a href="Svdrpsend-Command-Reference">svdrpsend(1)</a>\2', content)

    # commands.conf
    content = re.sub(r'([\'])commands.conf([\'])',
                     r'\1<a href="VDR-File-Formats-and-Conventions#commands">commands.conf</a>\2', content)

    # keymacros.conf
    content = re.sub(r'([\'])keymacros.conf([\'])',
                     r'\1<a href="VDR-File-Formats-and-Conventions#key-macros">keymacros.conf</a>\2', content)

    # channels.conf
    content = re.sub(r'([\'])channels.conf([\'])',
                     r'\1<a href="VDR-File-Formats-and-Conventions#channels">channels.conf</a>\2', content)

    # reccmds.conf
    content = re.sub(r'([\'])reccmds.conf([\'])',
                     r'\1<a href="VDR-File-Formats-and-Conventions#recording-commands">reccmds.conf</a>\2', content)

    # folders.conf
    content = re.sub(r'([\'])folders.conf([\'])',
                     r'\1<a href="VDR-File-Formats-and-Conventions#folders">folders.conf</a>\2', content)

    # epg.data
    content = re.sub(r'([\'])epg.data([\'])',
                     r'\1<a href="VDR-File-Formats-and-Conventions#epg-data">epg.data</a>\2', content)

    return content
