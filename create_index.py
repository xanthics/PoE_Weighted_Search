import subprocess
import os

from secrets import user_agent, poe_sessid
from helper_files.trade_mod_slots import update_mods, updateleagues, updatejsonmods


def safe_delete(file):
	if os.path.exists(file):
		os.remove(file)


def update_brython():
	# always run brython update when started
	safe_delete("docs/js/brython.js")
	# start installing brython js
	proc = subprocess.Popen(['brython-cli', 'install'], cwd='docs/js')
	proc.wait()
	# remove demo files that will interfere with make_modules
	for file in ['demo.html', 'index.html', 'README.txt', 'unicode.txt']:
		safe_delete(f"docs/js/{file}")
	# make a brython_modules.js specific to our setup
	proc = subprocess.Popen(['brython-cli', 'make_modules'], cwd='docs')
	proc.communicate(b'Y\n')
	proc.wait()
	# remove stdlib since we no longer need it
	safe_delete("docs/js/brython_stdlib.js")


def main():
	root_dir_g = os.path.dirname(os.path.abspath(__file__))
	g_cookies = {'POESESSID': poe_sessid}
	g_headers = {'User-Agent': user_agent}
	updateleagues(root_dir_g, g_headers, g_cookies)
	updatejsonmods(root_dir_g)
	update_mods('Crucible', root_dir_g, g_headers, g_cookies)
	# generate compact brython.js
	update_brython()


if __name__ == '__main__':
	main()
