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
import subprocess

repo = sys.argv[1]

# Get list of tags (unsorted)
taglist = subprocess.check_output([
    "git", "-C", repo, "tag",
    "--format", "%(refname:short) %(creatordate:short)"
]).decode("utf-8").splitlines()

# Split the two fields for all entries
taglist = [line.split(" ") for line in taglist]

# Sort handler
def versionkey(A):
    part1, part2, part3 = A[0].split(".")

    sort_for = [int(part1), int(part2)]

    if part3.isnumeric():
        sort_for.extend((int(part3), 0))
    elif "-" in part3:
        rev, patch = part3.split("-")
        sort_for.extend((int(rev), int(patch)))
    elif "pre" in part3:
        rev, pre = part3.split("pre")
        sort_for.extend((int(rev), -10 + int(pre)))

    return sort_for

# Try to sort the list
try:
    taglist.sort(key=versionkey)
except Exception as e:
    print(e, file=sys.stderr)

# Get the API version, build entries
entries = []
for tag, date in taglist:

    config_h = subprocess.check_output([
        "git", "-C", repo, "show",
        f"{tag}:config.h"
    ]).decode("utf-8")

    match = re.search(
        r'^#define\s+APIVERSION\s+"([^"]+)',
        config_h, flags=re.MULTILINE
    )

    apiversion = match.group(1) if match else "--"

    entries.append((tag, date, apiversion))

# Create Markdown output
print("| Version | Release Date | API Version |")
print("|---------|--------------|-------------|")
for version, date, apiversion in entries:
    print(f"| {version} | {date} | {apiversion} |")
