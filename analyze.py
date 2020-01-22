## Analyze, stem, and exclude stop words from analysis

def analyze_file(exclude_stop_words=False):
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
				word = word.lower()
				if exclude_stop_words and word not in stop_words and word != '':
					if word not in frequencies:
						frequencies[word] = 0
					frequencies[word] += 1
			line = text_file.readline()
	top_25 = sorted(frequencies.items(), key=lambda item: item[1], reverse=True)[:25]
	return top_25