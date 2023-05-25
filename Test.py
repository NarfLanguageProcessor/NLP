import os, json, numpy as np
from src.Words import Words

word = 'arms'

# print(Words.known(word))
# print(os.path.exists('Dictionary/' + word + '.w'))

# Words.save_array([word], 'Custom.txt', 'Word Lists')
#
# Words().compose_dictionary('Custom.txt')

# print(Words.compose('arms'))

if Words.collect('vonxdd'):
    print('yes')
else:
    print('no')


