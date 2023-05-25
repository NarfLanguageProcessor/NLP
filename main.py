# python3

from src.Words import Words

word = 'tenacious'
w = Words()

# print(w.define(word))
# print(w.synonyms(word))
# print(w.antonyms(word))

print(w.known('von'))
# print(w.compose('von'))

w.compose_dictionary()

# w.filter_top_words(['Top10k-Short.txt', 'Top10k-Medium.txt', 'Top10k-Long.txt'])

# w.compose_synonym_matrix('Top.txt', 'Word Lists/')



