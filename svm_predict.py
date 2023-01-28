from sklearn import svm
import pandas as pd
import numpy as np

class SVM_predictor(object):
    def __init__(self,input_file):
        self.predictor = svm.SVC()
        training_set = pd.read_csv(input_file).to_numpy()
        training_data = training_set[:,1:3]
        training_labels = training_set[:,-1]
        print(np.shape(training_set))
        print(np.shape(training_data))
        print(np.shape(training_labels))
        self.predictor.fit(training_data,training_labels)

    def predict_fault(self,sample):
        label = self.predictor.predict(sample)
        return label