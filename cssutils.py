import re
from xml.etree.ElementTree import ElementTree, Element, Comment, SubElement, tostring

class CssUtils(object):
    def file_get_contents(self, filename):
        file_input = open(filename, 'r')
        file_contents = file_input.read()
        return file_contents

    def is_str_array(self, haystack, needle):
#         print("Needle: {}".format(needle))
        if re.search(needle, haystack):
            return True
        else:
            return False

    def escaped(self, istring, pos):
        return not (self.s_at(istring, pos-1) != '\\' or self.escaped(istring, pos-1))

    def s_at(self, istring, pos):
        if pos > (len(istring) - 1) or pos < 0:
            return 0
        else:
            return istring[pos]

    def trim(self, istring):
        first = re.search("(?! |\n|\t|\r)", istring).start() if re.search("(?! |\n|\t|\r)", istring) else len(istring)

        last = max(istring.rfind(i) for i in " \n\t\r")
        last = last - 1 if last > 0 else len(istring)

#         print "First position: {}, Last position: {}, Trim String: {}".format(first, last, istring[first:last + 1])
        return istring[first:last + 1]

    def build_value(self, subvalues):
        ret = ""
        for pos, string in enumerate(subvalues):
            ret += subvalues[pos]
            if not pos == (len(subvalues) - 1):
                lastvalue = self.s_at(subvalues[pos], len(subvalues[pos])-1)
                nextvalue = self.s_at(subvalues[pos+1],0)
                ret += " "
        return ret

    def ctype_space(self, c):
        return c == ' ' or c == '\t' or c == '\n' or c == 11

    def build_xml(self, tokens, filename, method=None):

        root = Element("html", attrib ={})
        root.text = '\n\t'

        csstoken = dict()
        csstoken['warp'] = tokens
        csstoken['container'] = tokens
        child = self.build_content(csstoken)

        root.append(child)

        # Writes the element tree to a file, as XML
        tree = ElementTree(root)
        if method == "xml":
            tree.write(filename, method = method)
        elif method == "text":
            tree.write(filename, method = method)

    def build_content(self, dictdata, parent_node=None, parent_name = ''):
        def node_for_value(name, value, parent_node, parent_name):
            node = SubElement(parent_node, parent_name, attrib = {name: value})
            node.text = 'Contents'
            node.tail = '\n\t\t'
            return node

        # create an <body> element to hold all child elements
        if parent_node is None:
            node = Element('body')
            node.text = '\n\t\t'
            node.tail = '\n'
        else:
            node = SubElement(parent_node, 'div')
            node.text = '\n\t\t'
            node.tail = '\n\t\t'

        for key, value in dictdata.iteritems():
            if isinstance(value, dict):
                self.build_content(value, node, key)
            else:
                node_for_value(key, value, node, parent_name)
        return node
