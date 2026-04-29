import re

def naive_patterns(finish, stock):
    """
    Generates patterns of feasible cuts from stock width to meet specified finish widths. not considering the weight contraint
    """
    patterns = []
    skey = list(stock.keys())[0]
    for f in finish:
        feasible = False
        num_cuts_by_width = int((stock[skey]["width"] - stock[skey]["min_margin"]) / finish[f]["width"])
        
        if num_cuts_by_width > 0:
          feasible = True
          cuts_dict = {key: 0 for key in finish.keys()}
          cuts_dict[f] = num_cuts_by_width
          trim_loss = stock[skey]['width'] - sum([finish[f]["width"] * cuts_dict[f] for f in finish.keys()])
          trim_loss_pct = round(trim_loss/stock[skey]['width'] * 100, 3)
          patterns.append({"cuts": cuts_dict, 'trim_loss':trim_loss, "trim_loss_pct": trim_loss_pct })
            
        if not feasible :
            pass

    return patterns