# coding=utf-8
import unittest
from collections import OrderedDict

from text2chem.core.formula_parser import __parse_parentheses as parse_parentheses
from text2chem.regex_parser import RegExParser


class TestParser(unittest.TestCase):

    def test_regex_parser_make_fraction_convertion(self):
        parser = RegExParser()
        formula_res = [
            ('Na2/3Ni(3/10-x)MgxMn7/10O2', 'Na2/3Ni3/10-xMgxMn7/10O2'),
            ('(Cu1/3Nb2/3)1/4Ti(3/4-x)ZrxO2', '(Cu1/3Nb2/3)1/4Ti3/4-xZrxO2'),
            ('(Cu1/3Nb2/3)(1/4-y)Ti(3/4-x)Zr(x+y)O2', '(Cu1/3Nb2/3)1/4-yTi3/4-xZrx+yO2'),
            ('(Cu1/3Nb2/3)(1/4-y-x)Ti(3/4-x)Zr(2x+y)O2', '(Cu1/3Nb2/3)(1/4-y-x)Ti3/4-xZr2*x+yO2'),
        ]
        for formula, res in formula_res:
            self.assertEqual(parser.make_fraction_convertion(formula), res)

    def test_core_formula_parser__parse_parentheses(self):
        init_formula_res = [
            ('Ti(OCH(CH3)2)4', {'C': '(8)+(4)', 'H': '(24)+(4)', 'O': '4', 'Ti': '1'}),
            ('Na2/3Ni3/10-xMgxMn7/10O2',
             {'Na': '0.667', 'Ni': '0.3-x', 'Mg': 'x', 'Mn': '0.7', 'O': '2'}
             ),
            ('(Cu1/3Nb2/3)1/4Ti3/4-xZrxO2',
             {'Cu': '0.083', 'Nb': '0.167', 'O': '2', 'Ti': '0.75-x', 'Zr': 'x'}
             ),
            ('(Cu1/3Nb2/3)1/4-yTi3/4-xZr(x+y)O2',
             {'Cu': '0.0833-0.333*y', 'Nb': '0.167-0.667*y', 'Ti': '0.75-x', 'Zr': 'x+y', 'O': '2'}
             ),
            ('(Cu1/3Nb2/3)(1/4-y-x)Ti3/4-xZr2*x+yO2',
             {'Cu': '0.0833-0.333*x-0.333*y', 'Nb': '0.167-0.667*x-0.667*y', 'Ti': '0.75-x', 'Zr': '2*x+y', 'O': '2'}
             ),
        ]
        for init_formula, res in init_formula_res:
            formula_dict = OrderedDict()
            formula_dict, _ = parse_parentheses(init_formula, "1", formula_dict)
            self.assertEqual(formula_dict, res)
