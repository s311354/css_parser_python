import re

class CssUtils:

    def file_get_contents(self, filename):
        file_input = open(filename, 'r')
        file_contents = file_input.read()
        return file_contents

    def is_str_array(self, haystack, needle):
        print("Needle: {}".format(needle))
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
        if re.search("(?! |\n|\t|\r|\0xb)", istring):
            first = re.search("(?! |\n|\t|\r|\0xb)", istring).start()
        else:
            first = 0

        if first == -1:
            return istring
        else:
            last = max(istring.rfind(i) for i in " \n\t\r\0xb")
#             print "Last position: {}, Trim: {}".format(last, istring[first: last - first + 1])
            return istring[first: last - first + 1]


    def ctype_space(self, c):
        return c == ' ' or c == '\t' or c == '\n' or c == 11

