# Simple class to generate a test query based on what is implemented in gensearchparams.py

def main():
	selections = {'SpellslingerDW', 'Spellslinger', 'BattleMage'}
	dps = set()

	with open("../gensearchparams.py", "r") as f:
		for line in f:
			l = line.strip()
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

	print('=111&'.join(sorted(dps)), '=111&', "Flags=", ','.join(sorted(selections)), sep='')

if __name__ == '__main__':
	main()