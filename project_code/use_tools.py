"""
This file uses the functions in tools.py

:Author: Sandra
:Last updated: 11/09/2024
"""

import tools
import numpy

def run_all():
    """
    This function uses the functions imported from tools.py
    
    var2 is subtracted from var1
    
    Parameters:
        None
        
    Returns:
        None
    
    """
    x = 4
    y = 3
    
    a = tools.add(x,y)
    b = tools.subtract(x,y)
    
    return 0
    
if __name__=='__main__':
    run_all()