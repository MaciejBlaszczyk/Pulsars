from sklearn.svm import SVC
import logging
from Statistics import Statistics
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class SVM(object):

    def __init__(self, train_data, test_data, train_labels, test_labels, kernels = [], gammas = [], coefs = []):
        self.kernels = kernels
        self.gammas = gammas
        self.coefs = coefs
        self.train_data = train_data
        self.train_labels = train_labels
        self.test_data = test_data
        self.test_labels = test_labels
        self.sensitivity = []
        self.specificity = []
        self.general_result = []
        self.precision = []
        self.statistics = Statistics()

    def perform(self):
        counter = 0
        for k in self.kernels:
            for g in self.gammas:
                for c in self.coefs:
                    counter += 1
                    logging.info(' Computing SVM ... '
                                 + str(int(100 * counter / (len(self.coefs) * len(self.gammas) * len(self.kernels)
                                 - (self.kernels.count('linear') * len(self.gammas) * len(self.coefs) - 1)
                                 - (self.kernels.count('rbf') * len(self.gammas) * (len(self.coefs) - 1)))))
                                 + '% done')

                    clf = SVC(kernel=k, gamma=g, coef0=c)
                    clf.fit(self.train_data, self.train_labels)
                    res = clf.predict(self.test_data)

                    self.statistics.perform(self.test_labels, res)
                    self.sensitivity.append(self.statistics.get_sensitivity())
                    self.specificity.append(self.statistics.get_specificity())

                    if k == 'linear' or k == 'rbf':
                        break
                if k == 'linear':
                    break

    def get_sensitivity(self):
        return self.sensitivity

    def get_specificity(self):
        return self.specificity

    def get_general_results(self):
        return self.general_result
