from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import numpy as np

class Dec_Tree_predictor(object):
    def __init__(self,input_file):
        self.predictor = DecisionTreeClassifier(criterion = "entropy", splitter = "best")
        training_set = pd.read_csv(input_file).to_numpy()
        training_data = training_set[:,:3]
        training_labels = training_set[:,-1]
        self.predictor.fit(training_data,training_labels)

    def predict_fault(self,sample):
        label = self.predictor.predict(sample)
        return label