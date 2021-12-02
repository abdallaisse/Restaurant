# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 19:35:41 2020

@author: abdil
"""

class Display:
    def __init__ (self,item,price):
        self.item_name = item
        self.item_price = price
    
    def display_items(self):
        print("{} : {}".format(self.item_name, self.item_price))
    
    