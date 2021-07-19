import re

class CssUtils:

    def file_get_contents(self, filename):
        file_input = open(filename, 'r')
        file_contents = file_input.read()
        return file_contents

    def is_str_array(self, haystack, needle):
        if re.search(needle, haystack):
            return True
        else:
            return False

    def escaped(self, istring, pos):
        return self.s_at(istring, pos-1) != '\\' or self.escaped(istring, pos-1)

    def s_at(self, istring, pos):
        if pos > (len(istring) - 1) or pos < 0:
            return 0
        else:
            return istring[pos]

