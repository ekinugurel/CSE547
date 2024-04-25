import numpy as np
from scipy.sparse.linalg import spsolve
from scipy import sparse


m = 1882
n = 3000
f = 3
lamda = 0.01

X = sparse.csr_matrix(np.zeros((m, f)) + 0.5)  
Y = sparse.csr_matrix(np.zeros((n, f))) 

# construct the preference matrix and confidence matrix
# YOUR CODE HERE
P = 
C = 


def ALS(X, Y, P, C, m, n, f, lamda, MAX_ITER = 100):
	""""
	X: initial user matrix
	Y: initial item matrix
	P: preference matrix
	C: confidence matrix
	"""
	# construct lambda * I
	# YOUR CODE HERE
	lamda_eye = 

	for t in range(MAX_ITER):
		# update item matrix
		# YOUR CODE HERE
		xTx = X.T.dot(X)
		for item in range(n):
			p_i = P[:, item]
			C_i_I =        # the sparse matrix: C_i - I
			left = 		   # please use the trick in spec 
			right = 	   # please use the trick in spec 
			y_i = spsolve(left, right)
        	Y[item] = y_i
		
		# update user matrix   
		# YOUR CODE HERE     	
        yTy = Y.T.dot(Y)
        for u in range(m):
        	p_u = P[user, :]
        	C_u_I =        # the sparse matrix: C_u - I
        	left = 		   # please use the trick in spec 
        	right =        # please use the trick in spec 
        	x_u = spsolve(left, right)
        	X[user] = x_u
    return X, Y

    