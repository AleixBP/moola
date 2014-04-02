from optimisation_algorithm import *


class  LinearOperator(object):
    def __init__(self, matvec):
        self.matvec = matvec
    def __mul__(self,x):
        return self.matvec(x)
    def __rmul__(self,x):
        return NotImplemented
    def __call__(self,x):
        return self.matvec(x)

        

class LHess(LinearOperator):
    '''
    This class implements the limit-memory BFGS approximation of the inverse Hessian.
    '''
    def __init__(self, Hinit=1, max_len = 10):
        self.Hinit = Hinit
        self.max_len = max_len
        self.y   = []
        self.s   = []
        self.rho = []
    def __len__(self):
        assert( len(self.y) == len(self.s) )
        return len(self.y)+1
    def __getitem__(self,k):
        if k==0:
            return self.Hinit
        return (self.rho[k-1], self.y[k-1], self.s[k-1])
    def update(self,yk, sk):
        if len(self) == self.max_len:
            self.y   = self.y[1:]
            self.s   = self.s[1:]
            self.rho = self.rho[1:]
        self.y.append(yk)
        self.s.append(sk)
        self.rho.append( yk.dot(sk) )
    def matvec(self,x,k = -1):
        if k == -1:
            k = len(self)-1
        if k == 0:
            return self.Hinit * x
        rhok, yk, sk = self[k]     
        t = x - rhok * x.dot(sk) * yk
        t = self.matvec(t, k-1)
        t = t - rhok * yk.dot(t) * sk
        t = t + rhok * x.dot(sk) * sk
        return t

class BFGS(OptimisationAlgorithm):
    """
        Implements the BFGS method. 
     """
    def __init__(self, tol=1e-4, Hinit=1, options={}, hooks={}, **args):
        '''
        Initialises the steepest descent algorithm. 
        
        Valid options are:
        
         * tol: Functional reduction stopping tolerance: |j - j_prev| < tol. Default: 1e-4.
         * H_init: Initial approximation of the inverse Hessian.
         * options: A dictionary containing additional options for the steepest descent algorithm. Valid options are:
            - maxiter: Maximum number of iterations before the algorithm terminates. Default: 200. 
            - disp: dis/enable outputs to screen during the optimisation. Default: True
            - gtol: Gradient norm stopping tolerance: ||grad j|| < gtol.
            - line_search: defines the line search algorithm to use. Default: strong_wolfe
            - line_search_options: additional options for the line search algorithm. The specific options read the help 
              for the line search algorithm.
            - an optional callback method which is called after every optimisation iteration.
         * hooks: A dictionariy containing user-defined "hook" functions that are called at certain events during the optimisation.
            - before_iteration: Is called after before each iteration.
            - after_iteration: Is called after each each iteration.
          '''

        # Set the default options values
        self.tol = tol
        self.Hinit = Hinit
        self.gtol = options.get("gtol", 1e-4)
        self.maxiter = options.get("maxiter", 200)
        self.disp = options.get("disp", True)
        self.line_search = options.get("line_search", "strong_wolfe")
        self.line_search_options = options.get("line_search_options", {})
        self.ls = get_line_search_method(self.line_search, self.line_search_options)
        self.callback = options.get("callback", None)
        self.hooks = hooks

    def __str__(self):
        s = "BFGS method.\n"
        s += "-"*30 + "\n"
        s += "Line search:\t\t %s\n" % self.line_search 
        s += "Maximum iterations:\t %i\n" % self.maxiter 
        return s

    def display(self):
        print "disp be written"


    def check_convergence(self):
        print "check_convergergence to be written"
        return False, ""

    def perform_line_search(self, xk, pk):
        print "perform_line_search to be written"
        return 1.

    def solve(self, problem, xinit):
        '''
            Arguments:
             * problem: The optimisation problem.

            Return value:
              * solution: The solution to the optimisation problem 
         '''
        obj = problem.obj

        Hk = LHess(self.Hinit)
        xk = xinit.copy()
        dJ_old = obj.derivative(xk)

        # Start the optimisation loop
        it = 0
        while True:
            #hook("before_iteration", j, grad)
            self.display()

            conv, reason = self.check_convergence()
            if conv is True:
                break
            
            # compute search direction
            pk = - (Hk * dJ_old)
            
            # do a line search and update
            ak = self.perform_line_search(xk, pk)            
            sk = ak * pk 
            xk += sk
            #from IPython import embed; embed()
            print xk.data[0]

            # evaluate gradient at the new point
            dJ = obj.derivative(xk)
            yk = dJ - dJ_old
            
            # update the approximate Hessian
            Hk.update(yk, sk)

            dJ_old = dJ
            it += 1

            if it > 15:
                break
            

        self.display()

        return {"Optimizer" :xk,
                "Number of iterations": it}

