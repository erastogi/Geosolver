#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 13:40:40 2017

@author: eti
"""
from collections import Counter
from geosolver.diagram.get_instances import get_all_instances , _get_polygons , get_instances
def parse_explicit_formulas(all_formulas, graph_parse) :
    
    explicit_formulas = list()
    formula_dict = {"congurent_triangle" : [ "triangle", "triangle" ] , "vertically_opposite_angles" : [ "angle" ,"angle" ] ,
                     "angle_sum_property" : ["traingle"] , "exterior_angle" : ["triangle" , "line" ] ,
                     "BisectsAngle" : ["line", "point"] , "perpendicular_bisector" :[ "Perpendicular"]}
                     #"Area" : [("triangle", "square" , "rectangle" , "rhombus" ,"trapezium")] ,
                     #"Perimeter" : [("triangle", "square" , "rectangle" , "rhombus" ,"trapezium")] }
    
    #triangle_dict =  get_all_instances(graph_parse,'triangle') 
    #line_graph = graph_parse.line_graph
    #square , rectangle,rhombus
    #------------ perpendicular , midpoint
    dct = {}
    for key , values in formula_dict.iteritems() :
        val_dct = Counter[values]        
        try :
           for obj in val_dct.keys() :  
              #check polygons and lines and angles    
              if obj in ["triangle", "quad", "square" ,"rhombus" , "rectangle", 'hexagon', 'trapezium' , 'line' , 'angle']:                     
                     if obj not in dct.keys() :
                         dct[obj] = get_all_instances(graph_parse, obj) #returns a dictionary
                       
                     nmber =   len(dct[obj]) - val_dct[obj]
                     if nmber < 0 :
                         raise Exception()      
              #check all formulas       
              if all(obj not in str(formula.signature) for formula in all_formulas) : 
                     raise Exception()       
        except Exception:
              continue      
        explicit_formulas.append(key)
    

   #check all the explicit formulas which can be proved

    for i,formula in enumerate(explicit_formulas) :
         #   implement formula 
         if out.conf < 0.95 :
             del explicit_formulas[i]


    #add valid explicit formulas to all_formulas
    all_formulas = all_formulas + explicit_formulas
    return(all_formulas)         