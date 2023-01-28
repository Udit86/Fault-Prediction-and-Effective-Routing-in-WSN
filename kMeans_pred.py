from pickle import TRUE
import numpy as np
from sklearn.cluster import KMeans

class K_Means_predictor(object):
    def __init__(self):
        self.predictor = KMeans(n_clusters = 10,init = 'k-means++')
        #self.predictor = LocalOutlierFactor(n_neighbors = 20)

    def fit_predictor(self,train_np):
        num_samples = np.shape(train_np)[0]
        train = np.empty((0,4),dtype='float32')
        for i in range(1,num_samples):
            data = np.array([(train_np[i-1][0]-train_np[i][0]),(train_np[i-1][3]-train_np[i][3]),(train_np[i-1][4]-train_np[i][4]),train_np[i][5]]).reshape(1,-1)
            train = np.append(train,data,axis=0)
            #train_np[i-1] = np.subtract(train_np[i],train_np[i-1])
        self.predictor.fit(train)

    def predict_outlier(self,data):
        sample = np.array([(data[-2][0]-data[-1][0]),(data[-1][3]-data[-2][3]),(data[-1][4]-data[-2][4]),data[-1][5]]).reshape(1,-1)
        #sample = np.subtract(data[-1],data[-2])
        score = self.predictor.score(sample.reshape(1,-1))
        print(score)
        if score <=-100000000000:
            label = 1
        else:
            label = 0
        #lof_score = -self.predictor.score_samples(sample)[-1]
        return label