# python3

import os, time, requests, json
from bs4 import BeautifulSoup as BS
from threading import Thread


class Words:

    def __init__(self):
        pass

    def compose_dictionary(self, filename='Words.txt', dir="", threads=20, batch_size=25):

        batch = []
        self.threadies = threads
        self.activity = threads*[0]
        self.progress = 0
        self.words = open(dir + filename, 'r').read().splitlines()

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

        if not os.path.exists('Dictionary/' + self.words[index] + '.w'):
            with open('Dictionary/' + self.words[index] + '.w', 'w') as file:
                file.write(json.dumps({'index': index} | Words.compose(self.words[index])))

        self.activity[thread] -= 1

        return True

    @staticmethod
    def compose(word):
        return {'D': Words.define(word), 'S': Words.synonyms(word), 'A': Words.antonyms(word)}

    @staticmethod
    def define(word):
        # return BS(requests.get('https://www.dictionary.com/browse/{}'.format(word)).content, 'html.parser').find('div', {'class': 'css-1avshm7 e16867sm0'}).find('div', {'class': 'e1q3nk1v2'}).findAll('span', {'class': 'one-click-content'})[-1].text.split(':')[0]
        try: return BS(requests.get('https://www.dictionary.com/browse/{}'.format(word)).content, 'html.parser').find('div', {'class': 'css-1avshm7 e16867sm0'}).find('div', {'class': 'e1q3nk1v2'}).findAll('span', {'class': 'one-click-content'})[-1].text.split(':')[0]
        except: return []

    @staticmethod
    def synonyms(word):
        soup = BS(requests.get('https://www.thesaurus.com/browse/{}'.format(word)).content, 'html.parser')
        # return [span.text for span in soup.find('div', {'id': 'meanings'}).find('ul').findAll('a', {'class': ' '.join(soup.find('div', {'id': 'meanings'}).find('ul').findAll('a', {'class': 'eh475bn0'})[0]['class'])})]
        try: return [span.text for span in soup.find('div', {'id': 'meanings'}).find('ul').findAll('a', {'class': ' '.join(soup.find('div', {'id': 'meanings'}).find('ul').findAll('a', {'class': 'eh475bn0'})[0]['class'])})]
        except: return []

    @staticmethod
    def antonyms(word):
        soup = BS(requests.get('https://www.thesaurus.com/browse/{}'.format(word)).content, 'html.parser')
        # return [span.text for span in soup.find('div', {'id': 'antonyms'}).find('ul').findAll('a', {'class': ' '.join(soup.find('div', {'id': 'antonyms'}).find('ul').findAll('a', {'class': 'eh475bn0'})[0]['class'])})]
        try: return [span.text for span in soup.find('div', {'id': 'antonyms'}).find('ul').findAll('a', {'class': ' '.join(soup.find('div', {'id': 'antonyms'}).find('ul').findAll('a', {'class': 'eh475bn0'})[0]['class'])})]
        except: return []



    #
    #
    # MISC

    def status(self):
        print('\rProgress: ' + str(round(100 * self.progress / len(self.words), 2)) + '%  (' + str(self.progress) + ' of ' + str(len(self.words)) + ')', end="")

