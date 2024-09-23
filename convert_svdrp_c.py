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

import sys
import re
from crosslink import crosslink

input_str = sys.stdin.read()

# GitHub treats all angle brackets as HTML, so escape them
input_str = input_str.replace("<", "&lt;").replace(">", "&gt;")

# Get the actual help pages from the source file
helppages = re.search(r'const char \*HelpPages\[\] = {\n(.*?)};', input_str, flags=re.DOTALL).group(1)

# Sub headline
print("## SVDRP commands")

# Run over each individual command
for command in helppages.split(',\n')[:-1]:
    lines = command.split("\n")
    lines = list(map(lambda a: a.strip(' "').replace("\\n", ""), lines))
    print("### " + lines.pop(0))
    print()
    print(crosslink(" ".join(lines)))
    print()

# Get the SVDRP reply codes
returncodes = re.search(r'/\* SVDRP Reply Codes:\n(.*?)\*/', input_str, flags=re.DOTALL).group(1)

# Sub headline
print("## SVDRP reply codes")

print(returncodes.replace("\n ", "\n    "))

# Whereever this is documented, let's drop it in here.
print("""
Answers are in the format:

    <reply code><-|space><text>\\n

In the last line, returned as an answer to a command, the "-" will be replaced by a space character.
""")
