from vector import Vector
import numpy as np

class NumpyVector(Vector):
    ''' An implementation for vectors based on numpy arrays. '''

    def __init__(self, data):
        ''' Creates a new NumpyVector with a deep-copy of the 
        underlying data. The parameter 'data' must be 
        a NumpyVector or a numpy.array. '''
        if isinstance(data, NumpyVector):
            data = data.data

        self.data = np.array(data)

    def __len__(self):
        ''' Returns the (local) length. '''
        return len(self.data)

    def __getitem__(self, index):
        ''' Returns the value of the (local) index. '''
        return self.data[index]

    def __setitem__(self, index, value):
        ''' Sets the value of the (local) index. '''
        self[index] = value

    def scale(self, s):
        self.data *= s

    def inner(self, data):
        ''' Computes the inner product of the function and data. ''' 
        return np.dot(self.data, data)

    def norm(self, type="l2"):
        ''' Computes the function norm. Valid types are "L1", "L2", and "Linf"''' 
        if type=="L1":
            return sum(abs(self.data))
        elif type=="L2":
            return np.sqrt(sum(self.data**2))

    def axpy(self, a, x):
        ''' Adds a*x to the function. '''
        self.data += a*x.data