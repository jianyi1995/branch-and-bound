"""
using B&B algorithm to solve Binary ILP problem
"""
from Solve import solve as solver


class BandB(object):
    """
    this class is to implement the branch and bound algorithm for the binary integer programming problem
    
    Attributes:
        :param float incumbent: the current optimal objective function value
        :param dict queue: the active nodes, the key is their bound, the value is a list of fixed nodes with this bound,
        :param list solution: the solution corresponding to the optimal objective function value
        :param number: the variable number of original problem
        :type number: int
        :param cons: the constraints of original problem
        :type cons: list of list
        :param list obj: the objective function of original problem
        :param number constant: the constant in the objective function
        
    """
    def __init__(self, number, cons, obj, constant=0):
        """
        init class with original problem parameter
        """
        self.incumbent = float('-inf')
        self.queue = {}
        self.solution = []
        self.number = number
        self.cons = cons
        self.obj = obj
        self.constant = constant

    @staticmethod
    def is_int(solution):
        """
        this is a static method to check whether any element in solution is integer.
        
        Attributes:
            :param list solution: the solution gotten by using linear programming solver.
            
        :return: if any element is integer, return None, else return the index of the first non_integer
        """
        for i in solution:
            i = float(i)
            if not i.is_integer():
                return solution.index(i)
        return None

    def get_current_lp(self, fixed):
        """
        substituting the fixed variables for their fixed value and get the new lp programming problem
        do not need to worry about whether all the variables are fixed, in that case we can check whether it is feasible
        
        Attributes:
            :param list fixed: presents whether the variable is fixed, [1, -1, 0] means x1 is fixed to 1, x2 is not fixed, x3 is fixed to 0
        
        :return: the new lp programming problem parameter, i.e. the number of variable, cons and obj
        """
        origin_cons = self.cons.copy()
        origin_obj = self.obj.copy()
        number = 0
        cons = []
        cons_number = len(origin_cons)
        cons_constant = [0] * cons_number
        obj = [origin_obj[0]]
        constant = self.constant
        for i in range(cons_number):
            cons.append([])
        for i in range(self.number):
            if fixed[i] == 0:
                pass
            elif fixed[i] == 1:
                constant += self.obj[i + 1]
                for j in range(cons_number):
                    cons_constant[j] += self.cons[j][i]
            else:
                number += 1
                obj.append(origin_obj[i + 1])
                for j in range(cons_number):
                    cons[j].append(origin_cons[j][i])
        for j in range(cons_number):
            cons[j].append(origin_cons[j][-2])
            cons[j].append(origin_cons[j][-1] - cons_constant[j])
        return number, cons, obj, constant

    def add_active(self, fixed, index, opt):
        """
        this method add new active nodes into self.queue
        Attributes:
            :param fixed: the fixed of his father node
            :param index: the element index that will be branched, it refers to the new lp programming
            :param opt: the optimal value of father
        """
        branch_i = 0
        # branch_i means the variable index that needs to be branch
        while index >= 0:
            if fixed[branch_i] == -1:
                index -= 1
            branch_i += 1
        branch_i -= 1
        key = self.queue.get(opt, None)
        if not key:
            self.queue[opt] = []
        tmp = fixed.copy()
        tmp[branch_i] = 0
        self.queue[opt].append(tmp)
        tmp = fixed.copy()
        tmp[branch_i] = 1
        self.queue[opt].append(tmp)

    def get_active(self):
        """
        get an active node which has the greatest bound value and delete it from the queue
        
        :return: the fixed list of this node to generate the new lp
        """
        key = max(self.queue)
        fixed = self.queue[key].pop(0)
        if not self.queue[key]:
            self.queue.pop(key)
        return fixed



