from geosolver.expression.expression_parser import expression_parser
from geosolver.expression.prefix_to_formula import prefix_to_formula
from geosolver.grounding.states import MatchParse
from geosolver.ontology.ontology_definitions import FormulaNode, issubtype, VariableSignature, signatures, FunctionSignature
from geosolver.ontology.instantiator_definitions import instantiators
from geosolver.utils.num import is_number
from geosolver.diagram.get_instances import get_all_instances

__author__ = 'minjoon'


def parse_match_formulas(match_parse):
    assert isinstance(match_parse, MatchParse)
    graph_parse = match_parse.graph_parse
    core_parse =graph_parse.core_parse
    match_atoms = []
    triangle_dict = get_all_instances(graph_parse,'triangle')    
    for label, terms in match_parse.match_dict.iteritems():
        for term in terms:
            assert isinstance(term, FormulaNode)
            if issubtype(term.return_type, 'entity'):
                if term.signature.id == "Angle":
                    res = FormulaNode(signatures['Ge'], [FormulaNode(signatures['Pi'], []), FormulaNode(signatures['MeasureOf'], [term])])
                    match_atoms.append(res)
                continue

            # FIXME : to be obtained by tag model

            left_term = prefix_to_formula(expression_parser.parse_prefix(label))

            """
            if is_number(label):
                left_term = FormulaNode(FunctionSignature(label, "number", []), [])
            else:
                vs = VariableSignature(label, 'number')
                left_term = FormulaNode(vs, [])
            """

            atom = FormulaNode(signatures['Equals'], [left_term, term])
            match_atoms.append(atom)

            if term.signature.id == "Div":
                # TODO : this should be only constrained if the observed angle is < 180
                # TODO : In fact, the labeling should be reorganized. (x --> x*\degree)
                res = FormulaNode(signatures['Ge'], [180, left_term])
                match_atoms.append(res)
                
                ###adding right_traingle formulas
           
            """if left_term.signature.id == '90' :
                
                
                
                
                
                
                for points,data in triangle_dict.iteritems() :
                        p0, p1 = core_parse.intersection_points[points[0]] , core_parse.intersection_points[points[1]]
                        p2 =  core_parse.intersection_points[points[2]]
                        triangle  = instantiators['triangle'](p0,p1,p2)
                        result = 0 #IsInscribedIn( triangle , dd['instance'])
                        if result.conf > 0.9 :
                            triangle_variable = FormulaNode(signatures['Triangle'],
                                            [core_parse.point_variables[points[0]], core_parse.point_variables[points[1]],
                                            core_parse.point_variables[points[2]]])
    
                            variable_node = FormulaNode(signatures['IsRightTriangle'], [triangle_variable, circle_variable])
                            match_atoms.append(variable_node)                
"""

    return match_atoms
