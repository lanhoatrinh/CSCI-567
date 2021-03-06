import numpy as np


class KMeans():

    '''
        Class KMeans:
        Attr:
            n_cluster - Number of cluster for kmeans clustering (Int)
            max_iter - maximum updates for kmeans clustering (Int) 
            e - error tolerance (Float)
    '''

    def __init__(self, n_cluster, max_iter=100, e=0.0001):
        self.n_cluster = n_cluster
        self.max_iter = max_iter
        self.e = e

    def fit(self, x):
        '''
            Finds n_cluster in the data x
            params:
                x - N X D numpy array
            returns:
                A tuple
                (centroids a n_cluster X D numpy array, y a size (N,) numpy array where cell i is the ith sample's assigned cluster, number_of_updates an Int)
            Note: Number of iterations is the number of time you update the assignment
        '''
        assert len(x.shape) == 2, "fit function takes 2-D numpy arrays as input"
        np.random.seed(42)
        N, D = x.shape
      
        # TODO:
        # - comment/remove the exception.
        # - Initialize means by picking self.n_cluster from N data points
        # - Update means and membership until convergence or until you have made self.max_iter updates.
        # - return (means, membership, number_of_updates)

        # DONOT CHANGE CODE ABOVE THIS LINE
        K = self.n_cluster
        mu = np.empty((0,D),float)
        idx_arr = np.random.choice(N, K, replace = True)
        mu = np.append(mu, x[idx_arr], axis = 0)
        assert (K,D) == mu.shape
        r = np.zeros(N, dtype = int)
        J = 10**10

        for step in range(self.max_iter):
                d2 = np.empty((0,N),float)
                Jnew = 0
                for i in range(K):
                        vt = mu[i] - x
                        l2 = np.sum(vt * vt, axis = 1)
                        d2 = np.append(d2, [l2], axis = 0)
                r = np.argmin(d2, axis = 0)
                for i in range(K):
                        Jnew += np.sum( d2[i,:]* np.array(r == i) )                       
                        
                Jnew /= N
                
                if abs(J-Jnew) <= self.e:
                        break
                J = Jnew
                
                for k in range(K):
                        rk = np.array(r==k)
                        mu[k] = np.dot(rk,x)
                        count = np.count_nonzero(r == k)
                        if count > 0:
                                 mu[k] = mu[k]/count
                step +=1
        return(mu,r,step)
 
        # DONOT CHANGE CODE BELOW THIS LINE

class KMeansClassifier():

    '''
        Class KMeansClassifier:
        Attr:
            n_cluster - Number of cluster for kmeans clustering (Int)
            max_iter - maximum updates for kmeans clustering (Int) 
            e - error tolerance (Float) 
    '''

    def __init__(self, n_cluster, max_iter=100, e=1e-6):
        self.n_cluster = n_cluster
        self.max_iter = max_iter
        self.e = e

    def fit(self, x, y):
        '''
            Train the classifier
            params:
                x - N X D size  numpy array
                y - (N,) size numpy array of labels
            returns:
                None
            Stores following attributes:
                self.centroids : centroids obtained by kmeans clustering (n_cluster X D numpy array)
                self.centroid_labels : labels of each centroid obtained by 
                    majority voting ((N,) numpy array) 
        '''

        assert len(x.shape) == 2, "x should be a 2-D numpy array"
        assert len(y.shape) == 1, "y should be a 1-D numpy array"
        assert y.shape[0] == x.shape[0], "y and x should have same rows"

        np.random.seed(42)
        N, D = x.shape
        # TODO:
        # - comment/remove the exception.
        # - Implement the classifier
        # - assign means to centroids
        # - assign labels to centroid_labels

        # DONOT CHANGE CODE ABOVE THIS LINE
        centroids, r, step = KMeans(self.n_cluster, max_iter=100, e=1e-6).fit(x)
        centroid_labels = np.empty(0,)

        # Training
        for k in range(self.n_cluster):
                 vote = np.empty((0,))
                 rk = np.array(r==k)
                 if np.count_nonzero(rk) == 0:
                          label = 0
                 else:
                          c = np.unique(y)
                          for ci in c:
                                  check = np.array(y == ci)
                                  count = np.sum(rk * check)
                                  vote = np.append(vote, [count])
                          label = np.argmax(vote)
                 centroid_labels = np.append(centroid_labels, label)

         
        # DONOT CHANGE CODE BELOW THIS LINE

        self.centroid_labels = centroid_labels
        self.centroids = centroids

        assert self.centroid_labels.shape == (self.n_cluster,), 'centroid_labels should be a numpy array of shape ({},)'.format(
            self.n_cluster)

        assert self.centroids.shape == (self.n_cluster, D), 'centroid should be a numpy array of shape {} X {}'.format(
            self.n_cluster, D)

    def predict(self, x):
        '''
            Predict function

            params:
                x - N X D size  numpy array
            returns:
                predicted labels - numpy array of size (N,)
        '''

        assert len(x.shape) == 2, "x should be a 2-D numpy array"

        np.random.seed(42)
        N, D = x.shape
        # TODO:
        # - comment/remove the exception.
        # - Implement the prediction algorithm
        # - return labels

        # DONOT CHANGE CODE ABOVE THIS LINE
        d2 = np.empty((0,N),float)
        for i in range(self.n_cluster):
            vt = self.centroids[i] - x
            l2 = np.sum(vt * vt, axis = 1)
            d2 = np.append(d2, [l2], axis = 0)
        r = np.argmin(d2, axis = 0)
        labels = np.take(self.centroid_labels, r)    
        # DONOT CHANGE CODE BELOW THIS LINE
        return labels

