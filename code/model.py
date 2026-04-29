import pandas as pd
import numpy as np
import copy
import os

from pulp import LpMaximize, LpMinimize, LpProblem, LpAffineExpression, LpVariable, lpSum, PULP_CBC_CMD, LpBinary, value

class InventoryProblem:

    def __init__(self, finish, stocks):

        self.finish =  [item.copy() for item in finish] 
        self.stocks =  [item.copy() for item in stocks] 
    
    def make_naive_patterns(self):
        """
        Generates patterns of feasible cuts from stock width to meet specified finish widths.
        """
        self.patterns = []
        for f in self.finish:
            feasible = False
            for s in self.stocks:

                num_cuts_by_width = int((self.stocks[s]["width"]-self.stocks[s]["min_margin"]) / self.finish[f]["width"])
                num_cuts_by_weight = round((self.finish[f]["need_cut"] * self.stocks[s]["width"] ) / (self.finish[f]["width"] * self.stocks[s]['weight']))
                num_cuts = min(num_cuts_by_width, num_cuts_by_weight)

                if num_cuts > 0:
                    feasible = True
                    cuts_dict = {key: 0 for key in self.finish.keys()}
                    cuts_dict[f] = num_cuts
                    trim_loss = self.stocks[s]['width'] - sum([self.finish[f]["width"] * cuts_dict[f] for f in self.finish.keys()])
                    trim_loss_pct = round(trim_loss/self.stocks[s]['width'] * 100, 3)
                    self.patterns.append(
                        {"stock":s,
                        'trim_loss':trim_loss, 
                        "trim_loss_pct": trim_loss_pct ,
                        "stock_weight": self.stocks[s]['weight'], 
                        'stock_width':self.stocks[s]['width'],
                        "cuts": cuts_dict
                        }
                    )
                    
            if not feasible:
                print(f"No feasible pattern was found for {f}")
                continue

    def _new_pattern_problem(self, width_s, ap_upper_bound, demand_duals, MIN_MARGIN):

        prob = LpProblem("NewPatternProblem", LpMaximize)
        # Decision variables - Pattern
        ap = {f: LpVariable(f"ap_{f}", lowBound=0, upBound = ap_upper_bound[f], cat="Integer") for f in self.finish.keys()}
        # Objective function
        prob += lpSum(ap[f] * demand_duals[f] for f in self.finish.keys()), "MarginalCut"
        # Constraints - subject to stock_width - MIN MARGIN
        prob += lpSum(ap[f] * self.finish[f]["width"] for f in self.finish.keys()) <= width_s - MIN_MARGIN, "StockWidth_MinMargin"
        # Constraints - subject to trim loss 4% 
        prob += lpSum(ap[f] * self.finish[f]["width"] for f in self.finish.keys()) >= 0.96 * width_s , "StockWidth"
        
        # Solve the problem
        prob.solve(PULP_CBC_CMD(msg=False, timeLimit=60))
        marg_cost = value(prob.objective)
        
        pattern = {f: int(ap[f].varValue) for f in self.finish.keys()}
        
        return marg_cost, pattern
    
    def generate_dual_pattern(self):
        prob = LpProblem("GeneratePatternDual", LpMinimize)

        # Sets
        F = list(self.finish.keys())
        P = list(range(len(self.patterns)))

        # Parameters
        s = {p: self.patterns[p]["stock"] for p in range(len(self.patterns))}
        a = {(f, p): self.patterns[p]["cuts"][f] for p in P for f in F}
        demand_finish = {f: self.finish[f]["demand_line"] for f in F}
        upper_demand_finish = {f: self.finish[f]["upper_demand_line"] for f in F}

        # Decision variables #relaxed integrality
        x = {p: LpVariable(f"x_{p}", lowBound=0, upBound=20, cat="Continuous") for p in P}

        # OBJECTIVE function minimize stock used:
        prob += lpSum(x[p] for p in P), "Cost"

        # Constraints
        for f in F:
            prob += (
                lpSum(a[f, p] * x[p] for p in P) >= demand_finish[f], 
                f"Demand_{f}"
            )
            prob += (lpSum(a[f, p] * x[p] for p in P) <= upper_demand_finish[f], 
                     f"UpperDemand_{f}" 
            )

        # Solve the problem
        prob.solve(PULP_CBC_CMD(msg=False, options=['--solver', 'highs']))

        # Extract dual values
        dual_values = {f: prob.constraints[f"Demand_{f}"].pi for f in F}

        ap_upper_bound = {
            f: max([self.patterns[i]['cuts'][f] for i, _ in enumerate(self.patterns)], default=0) 
            for f in self.finish.keys()
        }
        demand_duals = {f: dual_values[f] for f in F}

        marginal_values = {}
        pattern = {}
        for s in self.stocks.keys():
            marginal_values[s], pattern[s] = self._new_pattern_problem( 
                self.stocks[s]["width"], ap_upper_bound, demand_duals, self.stocks[s]["min_margin"]
            )
        try:
            s = max(marginal_values, key=marginal_values.get) 
            cuts_dict =pattern[s]
            new_pattern = {"stock":s, 
                           'stock_weight': self.stocks[s]['weight'], 
                           'stock_width': self.stocks[s]["width"],
                           "cuts": cuts_dict
                           }
            
        except ValueError or TypeError:
            new_pattern = None
        return new_pattern