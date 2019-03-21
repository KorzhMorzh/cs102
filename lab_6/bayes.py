import numpy as np
import csv
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer


class NaiveBayesClassifier:

    def __init__(self, alpha=0.05):
        self.alpha = alpha
        self.freq_table = {}
        self.labels = []
        self.likelihood_table = {}
        self.labels_prob = []

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        self.labels = [i for i in set(y)]
        labels_count = {}
        for label in self.labels:
            labels_count.update({label: 0})
        for i, content in enumerate(zip(X, y)):
            for word in content[0].split(" "):
                if not self.freq_table.get(word.lower()):
                    self.freq_table.update({word.lower(): [0 for _i in self.labels]})
                    self.freq_table[word.lower()][self.labels.index(content[1])] += 1
                else:
                    self.freq_table[word.lower()][self.labels.index(content[1])] += 1
                labels_count[content[1]] += 1
        d = len(self.freq_table)
        for i in self.labels:
            self.labels_prob.append(y.count(i) / len(y))
        for word in self.freq_table:
            self.likelihood_table.update({word: [0 for _i in self.labels]})
            for i in range(len(self.labels)):
                self.likelihood_table[word][i] = (self.alpha +
                                                  self.freq_table[word][i]) / \
                                                 (self.alpha * d +
                                                  labels_count[self.labels[i]])

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        y = []
        predict = [0 for _i in range(len(self.labels))]
        for title in X:
            for i in range(len(self.labels)):
                logs_sum = np.log(self.labels_prob[i])
                for word in title.split(" "):
                    if self.freq_table.get(word.lower()):
                        logs_sum += np.log(self.likelihood_table[word.lower()][i])
                predict[i] = logs_sum
            y.append(self.labels[predict.index(max(predict))])
        return y

    '''y.append(self.labels[predict.index(max(predict))])
        return y'''

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        part = 0
        y = self.predict(X_test)
        for i in range(len(y_test)):
            if y[i] == y_test[i]:
                part += 1
        part /= len(X_test)
        return part


if __name__ == "__main__":
    with open("data/SMSSpamCollection (2)", encoding='utf-8') as f:
        data = list(csv.reader(f, delimiter="\t"))
    import string


    def clean(s):
        translator = str.maketrans("", "", string.punctuation)
        return s.translate(translator)
    X, y = [], []
    for target, msg in data:
        X.append(msg)
        y.append(target)
     #   X =["I love this sandwich", 'This is an amazing place', 'I feel very good about these beers', 'This is my best work', 'What an awesome view', 'I do not like this restaurant', 'I am tired of this stuff', 'I can t deal with this', 'He is my sworn enemy', 'My boss is horrible', 'The beer was good', 'I do not enjoy my job', 'I ain t feeling dandy today', 'I feel amazing', 'Gary is a friend of mine', 'I can t believe I m doing this']
     #   y =['Positive', 'Positive', 'Positive', 'Positive', 'Positive', 'Negative', 'Negative', 'Negative', 'Negative', 'Negative', 'Positive', 'Negative', 'Negative', 'Positive', 'Positive', 'Negative']
    X = [clean(x).lower() for x in X]
    X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]
    model = NaiveBayesClassifier()
    model.fit(X_train, y_train)
    print(model.score(X_test, y_test))
    model = Pipeline([
        ('vectorizer', TfidfVectorizer()),
        ('classifier', MultinomialNB(alpha=0.05)),
    ])

    model.fit(X_train, y_train)
    print(model.score(X_test, y_test))
