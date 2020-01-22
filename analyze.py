## Analyze, stem, and exclude stop words from analysis

def analyze_file(exclude_stop_words):
	stop_words = set()
	if exclude_stop_words:
		with open('files/stop-words.txt') as stop_words_file:
			stop_words = set(word.replace('\n', '') for word in stop_words_file.readlines())
	frequencies = dict()
	with open('example.txt') as text_file:
		line = text_file.readline()
		while line:
			words = line.replace('\n', '').split(' ')
			for word in words:
				word = stem_word(word).lower()
				if word not in stop_words and word != '':
					if word not in frequencies:
						frequencies[word] = 0
					frequencies[word] += 1
			line = text_file.readline()
	top_25 = sorted(frequencies.items(), key=lambda item: item[1], reverse=True)[:25]
	return top_25

def stem_word(word):
	#cover cases of talk, play, pass, and copy
	if word[-3:] == 'ing':
		return word[:-3]

	if word[-2:] in ['ed', 'es']:
		new_stem = word[:-2]
		if new_stem[-1] == 'i': #"change the y to an i and add 'es'/'ed'"
			new_stem = new_stem[:-1] + 'y'
		return new_stem

	if word[-1] == 's':
		return word[:-1]

	return word


## Test suite for stem_word()

regular_stems = {
	'talk' : ["talks", "talking", "talked"],
	'play' : ['plays', 'playing', 'played'],
	'pass' : ['passes', 'passing', 'passed'],
	'copy' : ['copies', 'copying', 'copied'],
	'real' : ['real'] #should just return the word
}

def test_word_stem(word, stem):
	assert stem_word(word) == stem

for stem, word_list in regular_stems.items():
	for word in word_list:
		test_word_stem(word, stem)














