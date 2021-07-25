import re

class CssUtils:

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
#         print("Last: {}".format(last))
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
