# Simple class to generate a test query based on what is implemented in gensearchparams.py
# also validates that all mods in goodmod are implemented and all implemented mods are in goodmod
def main():
	from helper_files.goodmod import goodmod
	selections = {'SpellslingerDW', 'Spellslinger', 'BattleMage'}
	dps = set()
	# sort goodmod based on str lens
	goodmod.sort(key=len, reverse=True)

	with open("../gensearchparams.py", "r") as f:
		m_check = False
		for line in f:
			l = line.strip()
			# check if any mods exist in this line (vs all mods), isolate it and determine if it is in goodmod, if so remove it
			if 'modstr =' in line:
				m_check = True
			if 'lookup_bases =' in line:
				m_check = False
			if m_check and ':' in line:
				l_s = l.split(':')[0].strip().strip('\'"')
				if l_s in goodmod:
					del goodmod[goodmod.index(l_s)]
				else:
					print(f"Rogue mod: {repr(l_s)}")
			if 'selection' in l:
				l2 = l
				while '}' in l2:
					st = l2.find('{')
					end = l2.find('}')
					for x in l2[st + 1:end].split(','):
						selections.add(x.strip('\'" '))
					l2 = l2[end+1:]
			if 'dps[' in l:
				l2 = l
				while 'dps[' in l2:
					st = l2.find('dps[')
					end = l2[st:].find(']')
					for x in l2[st + 4:st+end].split(','):
						dps.add(x.strip('\'" '))
					l2 = l2[end + 1:]
	# goodmod should be empty now if all mods are implemented
	if goodmod:
		print(f"Unimplemented good mods: {goodmod}")
	print('=111&'.join(sorted(dps)), '=111&', "Flags=", ','.join(sorted(selections)), sep='')


# sorts goodmod and badmod
def resetmods():
	from helper_files.goodmod import goodmod
	from helper_files.badmod import badmod
	for d, fo in [[goodmod, 'goodmod'], [badmod, 'badmod']]:
		d = list(set(d))
		d.sort()
		with open(f'{fo}.py', 'w') as f:
			f.write(f'{fo} = [\n\t"')
			f.write('",\n\t"'.join(d))
			f.write('"\n]\n')


if __name__ == '__main__':
#	resetmods()
	main()
