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

VDR_REPO = git://git.tvdr.de/vdr.git
MIRROR_REPO = git@github.com:vdr-projects/vdr.git
WIKI_REPO = git@github.com:vdr-projects/vdr.wiki.git

MD_FILES = vdr.wiki/VDR-command-reference.md\
           vdr.wiki/VDR-file-formats-and-conventions.md\
           vdr.wiki/svdrpsend-command-reference.md\
           vdr.wiki/VDR-manual.md\
           vdr.wiki/SVDRP-help.md\
           vdr.wiki/The-VDR-Plugin-System.md

.PHONY: all
all: vdr.git vdr.wiki $(MD_FILES) wiki-push mirror-push

#
# Prepares a bare repo local mirror of the VDR upstream repo
#

vdr.git:
#	Cleanup
	rm -rf vdr.git
#	Clone our GitHub mirror, first.
#	Then replace the origin URL with the upstream URL and fetch changes.
#	Doing it this way heavily reduces load on the upstream server.
	git clone --mirror $(MIRROR_REPO)
	git -C vdr.git remote set-url origin $(VDR_REPO)
	git -C vdr.git remote update
	git -C vdr.git remote prune origin

#
# Checks out a local working copy of VDR. We use our previously created
# bare repo for this.
#

# Require vdr.wiki to exist before checking out the VDR source code.
# This is to ensure that all Wiki files are recreated.
vdr: vdr.git vdr.wiki
	rm -rf vdr
	git clone vdr.git

vdr/vdr.1: vdr
vdr/vdr.5: vdr
vdr/svdrpsend.1: vdr
vdr/MANUAL: vdr
vdr/svdrp.c: vdr
vdr/PLUGINS.html: vdr

#
# Checks out our Wiki
#

vdr.wiki:
	git clone $(WIKI_REPO)

#
# man page convertings
#

define MAN_TO_MD =
mandoc -T html $(1) | python3 ./process_manpage_html.py > $(2)
endef

vdr.wiki/VDR-command-reference.md: vdr/vdr.1
	$(call MAN_TO_MD, $<, $@)

vdr.wiki/VDR-file-formats-and-conventions.md: vdr/vdr.5
	$(call MAN_TO_MD, $<, $@)

vdr.wiki/svdrpsend-command-reference.md: vdr/svdrpsend.1
	$(call MAN_TO_MD, $<, $@)

#
# MANUAL
#

vdr.wiki/VDR-manual.md: vdr/MANUAL
	python3 convert_vdr_manual.py < $< > $@

#
# SVDRP documentation
#

vdr.wiki/SVDRP-help.md: vdr/svdrp.c
	python3 convert_svdrp_c.py < $< > $@

#
# PLUGINS.html
#

vdr.wiki/The-VDR-Plugin-System.md: vdr/PLUGINS.html vdr.wiki
	python3 convert_plugins_html.py < $< > $@

#
# Pushes the wiki pages to GitHub.
# This target also creates a commit if changes where made.
#

.PHONY: wiki-push
wiki-push: $(MD_FILES)
	git -C vdr.wiki diff --quiet || git -C vdr.wiki commit -am 'Auto-Update wiki pages'
	git -C vdr.wiki push

#
# Pushes the VDR GIT mirror to GitHub.
#

# Require the Wiki files to be created before pushing the mirror.
# This is an added security. If something fails when creating the Wiki files
# then an admin should check the automated job.
.PHONY: mirror-push
mirror-push: $(MD_FILES)
#	Make sure our mirror is set as the origin URL. Then push a mirror.
	git -C vdr.git remote set-url origin $(MIRROR_REPO)
	git -C vdr.git push --mirror

#
# Cleanup
#

.PHONY: clean
clean:
	rm -rf vdr.git vdr vdr.wiki __pycache__
