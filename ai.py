class BookPerceptron: #Object-Oriented Programming and Creativity
    def __init__(self, num_features): #Object-Oriented Programming
        self.learning_rate = 0.1
        self.weights = [0.0 for _ in range(num_features)] #Comprehensions
        self.bias = 0.0

    def _activation(self, x):
        return 1 if x > 0 else 0

    def predict(self, features):
        return self._activation(sum(w * x for w, x in zip(self.weights, features)) + self.bias)

    def train(self, training_data, targets, epochs=100):
        for epoch in range(epochs):
            for features, target in zip(training_data, targets):
                prediction = self.predict(features)
                error = target - prediction
                if error != 0:
                    self.weights = [w + (self.learning_rate * error * f) for w, f in zip(self.weights, features)]
                    self.bias += self.learning_rate * error

    def get_explanation(self, features, feature_names):
        contributions = [w * x for w, x in zip(self.weights, features)]
        prediction = self.predict(features)

        if prediction == 1:
            best_idx = contributions.index(max(contributions))
            return prediction, feature_names[best_idx]
        else:
            worst_idx = contributions.index(min(contributions))
            return prediction, feature_names[worst_idx]


def extract_features(book, genre_scores, author_scores):
    pages_feat = (book.pages - 300) / 300.0
    pages_feat = max(-1.0, min(pages_feat, 1.0))

    genre_feat = sum(genre_scores.get(g.lower(), 0.0) for g in book.genre) / len(book.genre) if book.genre else 0.0
    author_feat = author_scores.get(book.author.lower(), 0.0)

    return [pages_feat, genre_feat, author_feat]