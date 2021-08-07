#!/usr/bin/env python2.7.16
import re
from cssutils import CssUtils
from cssparser import CssParser

if __name__ == "__main__":
    filepath = './simple.css'

    cssutils = CssUtils()

    file_contents = cssutils.file_get_contents(filepath)

    parser = CssParser()
    parser.parse_css(file_contents)

    parser.get_next_token()
