class Solver:
    
    def __init__(self,function,start=0,tolerance=1E-8,maxiter=20):
        self.fn=function
        self.guess=start
        self.tolerance=tolerance
        self.maxiter=20
        self.iteration=0  #iteration counter
        self.root=None
    
    def state(self):
        print 'Iterate=',self.guess
        print 'Residual=',abs(self.fn(self.guess))
        print 'Iteration=',self.iteration
        if self.root!=None:
            print 'Root=',self.root

class BracketSolver(Solver):
    def __init__(self,function,guess=0,tolerance=1E-8,maxiter=20,left=-1,right=1):
            Solver.__init__(self,function,guess,tolerance,maxiter)
            self.left=left
            self.right=right
            self.lval=self.fn(left)
            self.rval=self.fn(right)
            if self.lval*self.rval > 0:
                print 'Warning: No Root guarantee',self.fn(left),self.fn(right)
            if self.left >= self.right:
                print 'Warning, Invalid Interval'
            
    def solve(self,type='bisection'):
            self.iteration+=1
            while self.iteration < self.maxiter:
                if type=='bisection':
                    self.guess=.5*(self.left+self.right) #bisect bracket
                    test=self.fn(self.guess)
                    if abs(test)<self.tolerance:  #we found a root
                        self.root=self.guess
                        return 
                    else:   #iterate
                        if self.lval*test < 0:
                            self.rval=test
                            self.right=self.guess
                            self.iteration+=1
                        else:
                            self.lval=test
                            self.left=self.guess
                            self.iteration+=1

def myfun(x):
    from math import cos
    return cos(x)-x
