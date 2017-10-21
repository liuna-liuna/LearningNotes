#!/usr/bin/env python
# -*- coding: utf-8 -*-

# title         : xpath_css_expr_validator
# description   : n.a
# author        : liuna
# version       : 0.1
# usage         : python xpath_css_expr_validator.py
# date          : 2017-10-21
# notes         : 
#            ref:  Python检查xpath和csspath表达式是否合法  http://www.cnblogs.com/jhao/p/6052381.html
#            ref:  XPath 语法   http://www.w3school.com.cn/xpath/xpath_syntax.asp
#            ref:  CSS 高级语法 http://www.w3school.com.cn/css/css_syntax_pro.asp 
# python version: 2
# ================================================================================
# imports
from lxml import etree
from StringIO import StringIO
from cssselect.parser import SelectorError
from cssselect.xpath import HTMLTranslator

# consts
DUMMY_HTML_STRING_1 = '<foo><bar></bar></foo>'
DUMMY_XPATH_EXPR_CORRECT_1 = './div[@class="name"]/a/text()'
DUMMY_XPATH_EXPR_WRONG_1 = './div(@class="name")'
DUMMY_CSS_EXPR_CORRECT_1 = '.content > a'
DUMMY_CSS_EXPR_WRONG_1 = '.content > a[123]'
TYPE_DEFAULT_XPATH = 'xpath'
TYPE_DEFAULT_CSS = 'css'

# class
class XpathCssExprValidator(object):
    def __init__(self, type=TYPE_DEFAULT_XPATH, dummy_html=DUMMY_HTML_STRING_1):
        self.type_ = type
        self.dummy_html = dummy_html

    def _is_valid_xpath_expr(self, tobechecked_str):
        tree = etree.parse(StringIO(self.dummy_html))
        try:
            tree.xpath(tobechecked_str)
            return True
        except etree.XPathEvalError as e:
            return False

    def _is_valid_css_expr(self, tobechecked_str):
        try:
            HTMLTranslator().css_to_xpath(tobechecked_str)
            return True
        except SelectorError as e:
            return False

    def is_valid(self, tobechecked_str, type=None):
        if type and type == TYPE_DEFAULT_CSS:
            res = self._is_valid_css_expr(tobechecked_str)
        else:
            res = self._is_valid_xpath_expr(tobechecked_str)
        return res


# main entry
if __name__ == '__main__':
    xpath_str = DUMMY_XPATH_EXPR_CORRECT_1
    css_str = DUMMY_CSS_EXPR_CORRECT_1
    validator = XpathCssExprValidator()
    print('[INFO] {} is valid {}? {}'.format(xpath_str, 'xpath', validator.is_valid(xpath_str)))
    print('[INFO] {} is valid {}? {}'.format(css_str, 'css', validator.is_valid(css_str, type='css')))
    xpath_str = DUMMY_XPATH_EXPR_WRONG_1
    css_str = DUMMY_CSS_EXPR_WRONG_1
    print('[INFO] {} is valid {}? {}'.format(xpath_str, 'xpath', validator.is_valid(xpath_str)))
    print('[INFO] {} is valid {}? {}'.format(css_str, 'css', validator.is_valid(css_str, type='css')))
