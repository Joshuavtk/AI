from pprint import pprint
import json
import markovify

# read text from file
f = open('Nescio-de-Uitvreter.txt', 'r')
text = f.read()

# train and print model for n=2
text_model = markovify.Text(text, state_size=2)

val = text_model.chain.model[('Gare', 'du')]
print(val)

# generate some sentences
for _ in range(5):
    sentence = text_model.make_sentence()
    print(sentence)

# train and print model for n=3
text_model = markovify.Text(text, state_size=3)

val = text_model.chain.model[('Japi', 'wist', 'wel')]
print(val)

# generate sentences n=3
for _ in range(5):
    sentence = text_model.make_sentence(tries=9999)
    print(sentence)