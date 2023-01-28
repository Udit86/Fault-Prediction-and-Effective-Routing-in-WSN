from pickle import TRUE
import numpy as np
from sklearn.neighbors import LocalOutlierFactor

class predictor(object):
    def __init__(self):
        self.predictor = LocalOutlierFactor(n_neighbors = 20,novelty=True)
        #self.predictor = LocalOutlierFactor(n_neighbors = 20)

    def fit_predictor(self,train_np):
        self.predictor.fit(train_np)

    def predict_outlier(self,sample):
        label = self.predictor.predict(sample)[-1]
        lof_score = -self.predictor.score_samples(sample)[-1]
        return label, lof_score