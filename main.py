#!/usr/bin/env python2.7.16
import re
from cssutils import CssUtils
from cssparser import CssParser

from xml.etree.ElementTree import ElementTree, Element, Comment

if __name__ == "__main__":
    filepath = './simple.css'

    parser = CssParser(filepath)
    parser.iterate_token()

    parser.write("test.xml", "xml")
