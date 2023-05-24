# python3

import os, time, requests, json, numpy as np
from bs4 import BeautifulSoup as BS
from threading import Thread


class Words:

    def __init__(self):
        pass

    def compose_dictionary(self, filename='Words.txt', dir='Word Lists/', threads=20, batch_size=25):

        batch = []
        self.threadies = threads
        self.activity = threads*[0]
        self.progress = 0
        self.words = Words.open_array(filename, dir)

        print('\nCreating Dictionary...')
        self.status()

        for i in range(0, threads):
            batch.append(Thread(target=self.compose_words, args=[i*batch_size, batch_size, threads, i]))
            batch[-1].start()

        while self.threadies > 0:
            time.sleep(1)

        self.words.clear()
        self.activity.clear()
        del self.progress
        del self.threadies

        print('\nDictionary Complete!\n\n')

        return True

    def compose_words(self, index, batch_size, threads, thread):

        if index > len(self.words):
            self.threadies -= 1
            return True

        batch = []

        for i in range(index, min(index + batch_size, len(self.words))):
            batch.append(Thread(target=self.compose_word, args=[i, thread]))
            batch[-1].start()

        while(self.activity[thread] > 0):
            time.sleep(0.1)

        self.progress = min(len(self.words), self.progress + batch_size)

        self.status()

        return self.compose_words(index + batch_size*threads, batch_size, threads, thread)

    def compose_word(self, index, thread):

        self.activity[thread] += 1

        if not Words.known(self.words[index], '../Dictionary/'):
            Words.save_json({'index': index} | Words.compose(self.words[index]), self.words[index] + '.w', 'Dictionary/')

        self.activity[thread] -= 1

        return True

    @staticmethod
    def compose(word):
        return {'D': Words.define(word), 'S': Words.synonyms(word), 'A': Words.antonyms(word)}

    @staticmethod
    def known(word, dir='Dictionary/'):
        return os.path.exists(dir + word + '.w')

    @staticmethod
    def collect(word, dir='Dictionary/'):
        if Words.known(word, dir):
            return Words.open_json(word + '.w', dir)
        return {}



    def filter_top_words(self, filenames, dir='Word Lists/'):

        top = []

        for word_list in filenames:
            wordies = Words.open_array(word_list, dir)

            for word in wordies:
                if Words.known(word, '../Dictionary/'):
                    top.append(word)

        Words.save_array(top, 'Top.txt', dir)

        return True



    def compose_synonym_matrix(self, filename='Words.txt', dir='Word Lists/'):

        words = Words.open_array(filename, dir)
        indices = dict(zip(words, range(len(words))))
        sm = np.zeros(len(words)**2).reshape(len(words), len(words))

        for i in range(len(sm)):
            composition = Words.collect(words[i])
            if composition and 'S' in composition:
                for synonym in composition['S']:
                    synonym = Words.clean(synonym)
                    if synonym in indices:
                        sm[i][indices[synonym]] = 1

        print(sm)
        return Words.save_numpy(sm, 'Synonyms_Matrix', 'etc/')




    @staticmethod
    def define(word):
        # return BS(requests.get('https://www.dictionary.com/browse/{}'.format(word)).content, 'html.parser').find('div', {'class': 'css-1avshm7 e16867sm0'}).find('div', {'class': 'e1q3nk1v2'}).findAll('span', {'class': 'one-click-content'})[-1].text.split(':')[0]
        try: return BS(requests.get('https://www.dictionary.com/browse/{}'.format(word)).content, 'html.parser').find('div', {'class': 'css-1avshm7 e16867sm0'}).find('div', {'class': 'e1q3nk1v2'}).findAll('span', {'class': 'one-click-content'})[-1].text.split(':')[0]
        except: return []

    @staticmethod
    def synonyms(word):
        soup = BS(requests.get('https://www.thesaurus.com/browse/{}'.format(word)).content, 'html.parser')
        # return [span.text for span in soup.find('div', {'id': 'meanings'}).find('ul').findAll('a', {'class': ' '.join(soup.find('div', {'id': 'meanings'}).find('ul').findAll('a', {'class': 'eh475bn0'})[0]['class'])})]
        try: return [Words.clean(span.text) for span in soup.find('div', {'id': 'meanings'}).find('ul').findAll('a', {'class': ' '.join(soup.find('div', {'id': 'meanings'}).find('ul').findAll('a', {'class': 'eh475bn0'})[0]['class'])})]
        except: return []

    @staticmethod
    def antonyms(word):
        soup = BS(requests.get('https://www.thesaurus.com/browse/{}'.format(word)).content, 'html.parser')
        # return [span.text for span in soup.find('div', {'id': 'antonyms'}).find('ul').findAll('a', {'class': ' '.join(soup.find('div', {'id': 'antonyms'}).find('ul').findAll('a', {'class': 'eh475bn0'})[0]['class'])})]
        try: return [Words.clean(span.text) for span in soup.find('div', {'id': 'antonyms'}).find('ul').findAll('a', {'class': ' '.join(soup.find('div', {'id': 'antonyms'}).find('ul').findAll('a', {'class': 'eh475bn0'})[0]['class'])})]
        except: return []



    #
    #
    # etc

    @staticmethod
    def clean(word):
        return word.strip()

    @staticmethod
    def open_array(filename, dir=""):
        if os.path.exists(dir + filename):
            with open(dir + filename, 'r') as file:
                a = file.read().splitlines()
            return a

        raise Exception('File not found: ' + dir + filename)

    @staticmethod
    def open_json(filename, dir=""):
        if os.path.exists(dir + filename):
            with open(dir + filename, 'r') as file:
                d = json.load(file)
            return d

        raise Exception('File not found: ' + dir + filename)

    @staticmethod
    def open_numpy(filename, dir=""):
        if os.path.exists(dir + filename):
            with open(dir + filename, 'r') as file:
                n = np.load(file)
            return n

        raise Exception('File not found: ' + dir + filename)

    @staticmethod
    def save_array(a, filename, dir=""):
        with open(dir + filename, 'w') as file:
            file.write('\n'.join(a))
        return True


    @staticmethod
    def save_json(d, filename, dir=""):
        with open(dir + filename, 'w') as file:
            file.write(json.dumps(d))
        return True

    @staticmethod
    def save_numpy(n, filename, dir=""):
        return np.save(dir + filename, n)

    def status(self):
        print('\rProgress: ' + str(round(100 * self.progress / len(self.words), 2)) + '%  (' + str(self.progress) + ' of ' + str(len(self.words)) + ')', end="")

