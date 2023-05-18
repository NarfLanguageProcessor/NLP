a = {'a': 1, 'b': 2, 'c': 3}
b = {'d': 1, 'e': 2, 'f': 3}
c = a | b
print(c)
print(1, end="\r", flush=True)
print(2, end="\r", flush=True)
print(3, end="", flush=True)
print(1, end="\r", flush=True)
print(2, end="\r", flush=True)
print('\r' + str(3), end="\n", flush=True)
print(round(4.333333, 2))

from threading import Thread

def oink(x):
    print(x)

Thread(target=oink, args=['pig']).run()
