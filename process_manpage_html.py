#!/usr/bin/python3

#    Automated VDR repository mirror and wiki page generator
#    Copyright © 2024  Manuel Reimer <manuel.reimer@gmx.de>
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

# Get only the body
body = re.search(r'<body>(.*)</body>', input_str, flags=re.DOTALL).group(1)

# Remove the "head" table
body = re.sub(r'<table class="head">.*?</table>', r'', body, flags=re.DOTALL)

# Remove all links
body = re.sub(r'<a [^>]+>(.+?)</a>', r'\1', body, flags=re.DOTALL)

# Drop all "id" or "class" attributes from all HTML tags
body = re.sub(r'<([a-z0-9]+)(?: (?:id|class)="[^"]+")+>', r'<\1>', body)

# Wrap all <dt> contents into additional <h3> tags
body = re.sub(r'<dt>(.*?)</dt>', r'<dt><h3>\1</h3></dt>', body, flags=re.DOTALL)

# Remove all HTML tags within headers
# Replace series of space characters in headers with a single space character
# Note: Two RegEx stacked with the first using a "positive lookbehind"
body = re.sub(r'(?<=<h[1-3]>)(.+?)(?=</h[1-3]>)',
              lambda match: re.sub(r'(?:\s|&#x00A0;)+', r' ',
                                   re.sub(r'<[^>]+>', r'', match.group(1))),
              body, flags=re.DOTALL)

# Drop "<br/>" within "<pre>...</pre>" (bug in mandoc?)
body = re.sub(r'(?<=<pre>)(.+?)(?=</pre>)',
              lambda match: re.sub(r'<br/>\n?', r'', match.group(1)),
              body, flags=re.DOTALL)

print(crosslink(body))
