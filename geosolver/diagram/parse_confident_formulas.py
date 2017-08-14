import itertools
from geosolver.diagram.get_instances import get_all_instances
from geosolver.ontology.ontology_definitions import FormulaNode, signatures, FunctionSignature
from geosolver.ontology.instantiator_definitions import instantiators
from geosolver.ontology.ontology_semantics import IsInscribedIn, IsChordOf, IsRadiusLineOf, IsDiameterLineOf, Tangent, Parallel , PointLiesOnLine
import numpy as np

__author__ = 'minjoon'

def parse_confident_formulas(graph_parse):
    eps = 0.5 # to be updated by the scale of the diagram
    core_parse = graph_parse.core_parse
    line_graph = graph_parse.line_graph
    circle_dict = graph_parse.circle_dict
    confident_formulas = []

    for from_key, to_key, data in line_graph.edges(data=True):
        line_variable = FormulaNode(signatures['Line'],
                                     [core_parse.point_variables[from_key], core_parse.point_variables[to_key]])
        points = data['points']
        for point_key, point in points.iteritems():
            point_variable = core_parse.point_variables[point_key]
            variable_node = FormulaNode(signatures['PointLiesOnLine'], [point_variable, line_variable])
            confident_formulas.append(variable_node)
    #checking Parallel lines
        #remove lines formed by points of intersection 
        lg =  line_graph.copy()
        lg.remove_nodes_from(points.keys())
        for  fk , tk , data2 in lg.edges(data=True) :
             if len(set(data2['points'].keys()) - set(points.keys())) == len(data2['points']) :
                        result = Parallel(data['instance'],data2['instance'])
                        if result.conf > 0.95 :   
                            line_variable2 = FormulaNode(signatures['Line'],
                                     [core_parse.point_variables[fk], core_parse.point_variables[tk]])
                            variable_node = FormulaNode(signatures['Parallel'], [line_variable, line_variable2])
                            confident_formulas.append(variable_node)
       

    #include formulas involving traingle and circle
    formulas = [IsChordOf , IsRadiusLineOf , IsDiameterLineOf, Tangent ]
    triangle_dict = get_all_instances(graph_parse,'triangle') 
    for center_key, d in circle_dict.iteritems():
        for radius_key, dd in d.iteritems():
            circle_variable = FormulaNode(signatures['Circle'],
                                           [core_parse.point_variables[center_key],
                                            core_parse.radius_variables[center_key][radius_key]])
            points = dd['points']
            for point_key, point in points.iteritems():
                point_variable = core_parse.point_variables[point_key]
                variable_node = FormulaNode(signatures['PointLiesOnCircle'], [point_variable, circle_variable])
                confident_formulas.append(variable_node)

   

    # Just enforce non collapsing between known labels?
    #for circle_key,d in circle_dict.iteritems() :
        #for radius_key, dd in d.iteritems():
               #circle_variable = FormulaNode(signatures['Circle'],
               #                                           [core_parse.point_variables[center_key],
               #                  core_parse.radius_variables[center_key][radius_key]])
            for points,data in triangle_dict.iteritems() :
                   p0, p1 = core_parse.intersection_points[points[0]] , core_parse.intersection_points[points[1]]
                   p2 =  core_parse.intersection_points[points[2]]
                   triangle  = instantiators['triangle'](p0,p1,p2)   
                   result = IsInscribedIn( triangle , dd['instance'])
                   if result.conf > 0.9 :
                         triangle_variable = FormulaNode(signatures['Triangle'],
                                            [core_parse.point_variables[points[0]], core_parse.point_variables[points[1]],
                                            core_parse.point_variables[points[2]]])
    
                         variable_node = FormulaNode(signatures['IsInscribedIn'], [triangle_variable, circle_variable])
                         confident_formulas.append(variable_node)
                    
        
    ## include other formulas involving circles :
        #chordof , diameter , radius ,tangent
            for from_key, to_key, data in line_graph.edges(data=True): 
                   line_variable =  FormulaNode(signatures['Line'],
                                     [core_parse.point_variables[from_key], core_parse.point_variables[to_key]])
                   
                   for formula in formulas :
                        result = formula( data['instance'] , dd['instance'])
                        if result.conf > 0.95 :                          
                            variable_node = FormulaNode(signatures[str(formula).split(' ')[1]], [line_variable, circle_variable])
                            confident_formulas.append(variable_node)
                
    
    """
    for key, angle in get_all_instances(graph_parse, 'angle', True).iteritems():
        r = FormulaNode(signatures['Pi'], [])/2.0
        formula = FormulaNode(signatures['Ge'], [r, FormulaNode(signatures['MeasureOf'], [angle])])
        tv = graph_parse.core_parse.evaluate(formula)
        if tv.norm == 0:
            confident_formulas.append(formula)
    """

    return confident_formulas
