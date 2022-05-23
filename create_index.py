import subprocess
import os

from secrets import user_agent, poe_sessid
from helper_files.trade_mod_slots import update_mods, updateleagues, updatejsonmods


def update_brython():
	# proc = subprocess.Popen(['brython-cli', 'install'], cwd='docs/js')
	proc = subprocess.Popen(['brython-cli', '--install'], cwd='docs/js')
	proc.wait()
	for file in ['demo.html', 'index.html', 'README.txt', 'unicode.txt']:
		f_file = f"docs/js/{file}"
		if os.path.exists(f_file):
			os.remove(f_file)
	# proc = subprocess.Popen(['brython-cli', 'make_modules'], cwd='docs')
	proc = subprocess.Popen(['brython-cli', '--modules'], cwd='docs')
	proc.wait()
	f_file = "docs/js/brython_stdlib.js"
	if os.path.exists(f_file):
		os.remove(f_file)


def main():
	root_dir_g = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	g_cookies = {'POESESSID': poe_sessid}
	g_headers = {'User-Agent': user_agent}
	updateleagues(root_dir_g, g_headers, g_cookies)
	updatejsonmods(root_dir_g)
	# update_mods('Sentinel', root_dir_g, g_headers, g_cookies)
	# generate compact brython.js
	update_brython()


if __name__ == '__main__':
	main()
