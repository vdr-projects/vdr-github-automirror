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

input_str = sys.stdin.read()

# Get only the body
body = re.search(r'<body>(.*)</body>', input_str, flags=re.DOTALL).group(1)

# Code is wrapped inside a table which results in ugly display on GitHub
body = re.sub(r'<p><table><tr><td class="code"><pre>(.*?)</pre></td></tr></table></?p>', r'<pre>\1</pre>', body, flags=re.DOTALL)

# Drop all "id" or "class" attributes from all HTML tabs
body = re.sub(r'<([a-z0-9]+)(?: (?:id|class)=".*?")+>', r'<\1>', body)

# Remove border attribute from table
body = re.sub(r'<table border=.*?>', '<table>', body)

# Drop all anchors. GitHub creates their own anchors and ours will conflict
body = re.sub(r'<a name="[^"]+">(.*?)</a>', r'\1', body)

# Now refactor the TOC links to point to the GitHub created anchors
body = re.sub(r'<a href="#([^"]+)">', lambda a: '<a href="#' + a.group(1).lower().replace(" ", "-") + '">', body)

print(body)
