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

# Split paragraphs
paragraphs = input_str.split("\n\n")

for index, paragraph in enumerate(paragraphs):
    lines = paragraph.split("\n")

    # Match for headlines (single line with "underline")
    if len(lines) == 2 and re.match(r'^-+$', lines[1]):
        # Do not actually make them headers but bold text
        print("**" + lines[0] + "**\n")

    # Match for headlines (* in front of line)
    elif len(lines) == 1 and lines[0][0] == "*":
        print("## " + lines[0][2:] + "\n")

    # Detect "preformatted tables".
    elif "  " in lines[0].strip() or "       " in paragraph:
        # Add two more space characters for a total of four.
        for line in lines:
            print("  " + line)
        print("")

    # Detect the footnote list
    elif "(1)" in lines[0]:
        for number in range(2,4):
            paragraph = paragraph.replace(f"({number})", f"<br>({number})")
        print(paragraph + "\n")

    # All other paragraphs.
    else:
        # GitHub will misinterpret tildes for "strike-through" if not escaped
        paragraph = paragraph.replace("~", "\\~")
        # Add crosslinking and print paragraph
        print(crosslink(paragraph) + "\n")
