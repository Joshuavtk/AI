import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews

# Naive Bayes explained: https://www.youtube.com/watch?v=O2L2Uv9pdDA

def extract_features(word_list):
    return dict([(word, True) for word in word_list])

# load positive and negative reviews (# 1000 pos, 1000 neg)
positive_fileids = movie_reviews.fileids('pos')
negative_fileids = movie_reviews.fileids('neg')

# go through all 'positive files', extract the words and put them in a dict
# example: [({'films': True, 'adapted': True, 'from': True, 'comic': True, 'books': True, 'have': True}, 'Positive')]
# list of tuples, where each tuple has form (dict, 'Positive')
features_positive = [(extract_features(movie_reviews.words(fileids=[f])),'Positive') for f in positive_fileids]
features_negative = [(extract_features(movie_reviews.words(fileids=[f])),'Negative') for f in negative_fileids]

#print(features_positive[1])

print("Number of words seen as positive: ", len(features_positive))
print("Number of words seen as negative: ", len(features_negative))

# split the data into train and test (80/20)
threshold_factor = 0.8
threshold_positive = int(threshold_factor * len(features_positive))
threshold_negative = int(threshold_factor * len(features_negative))

features_train = features_positive[:threshold_positive]+features_negative[:threshold_negative]
features_test = features_positive[threshold_positive:]+features_negative[threshold_negative:]

print("Number of training datapoints: ", len(features_train))
print("Number of test datapoints: ", len(features_test)) 

# train the NaiveBayesClassifier
# print accuracy of classifier
# show the 20 most informative features

# sample input reviews
input_reviews = [
    "Started off as the greatest series of all time, but had the worst ending of all time.",
    "Exquisite. 'Big Little Lies' takes us to an incredible journey with its emotional and intriguing storyline.",
    "I love Brooklyn 99 so much. It has the best crew ever!!",
    "The Big Bang Theory and to me it's one of the best written sitcoms currently on network TV.",
    "'Friends' is simply the best series ever aired. The acting is amazing.",
    "SUITS is smart, sassy, clever, sophisticated, timely and immensely entertaining!",
    "Cumberbatch is a fantastic choice for Sherlock Holmes-he is physically right (he fits the traditional reading of the character) and he is a damn good actor",
    "What sounds like a typical agent hunting serial killer, surprises with great characters, surprising turning points and amazing cast."
    "This is one of the most magical things I have ever had the fortune of viewing.",
    "I don't recommend watching this at all!"
]

print("Predictions: ")

for review in input_reviews:
    # print pos or negative, together with the probability
