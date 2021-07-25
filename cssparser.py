import re
from cssutils import CssUtils

class CssParser:

    # PAT: parsing at-block, such as @charset, @namespace, and @import 
    parse_status = ["PIS", "PIP", "PIV", "PINSTR", "PIC", "PAT"]
    token_type = ["CHARSET", "IMPORT", "NAMESP", "AT_START", "AT_END", "SEL_START", "SEL_END", "PROPERTY", "VALUE", "COMMENT", "CSS_END"]

    """Docstring for CssParser. """
    def __init__(self):
        self.tokens = "{};:()@='\"/,\\!$%&*+.<>?[]^`|~"
        self.token_ptr = 1
        self.line = 1
        self.start_line= 0
        self.start_pos = 0
        self.selector_nest_level = 0
        self.cur_selector = ""
        self.cur_at = ""
        self.cur_property = ""
        self.cur_string = ""
        self.cur_value = ""
        self.cur_sub_value = ""
        self.cur_sub_value_arr = []
        self.csstokens = {}
        self.cur_function_arr = dict()
        self.sel_separate = dict()

    def parse_css(self, css_input):

        astatus = "PIS"
        old_status = "PIS"
        afrom = []
        str_char = []
        str_in_str = False
        invalid_at = False
        str_size = len(css_input)
        self.record_position("PIS", "PIS", css_input, 0, str_size, True)

        for pos, string in enumerate(css_input):
            if string == '\n' or string == '\r':
                self.line += 1

            # record current position for selected state transitions
            print("Current Posistion: {}".format(pos))
            if old_status != astatus:
                self.record_position(old_status, astatus, css_input, pos, str_size)

            old_status = astatus

            if astatus == "PIS":
               (astatus, pos, afrom, invalid_at) = self.parse_in_selector(css_input, pos, astatus, afrom, invalid_at, str_char, str_size)
            elif astatus == "PIP":
                (astatus, pos, afrom, invalid_at) = self.parse_in_property(css_input, pos, astatus, afrom, invalid_at)
            elif astatus == "PIV":
                (astatus, pos, afrom, invalid_at, pn) = self.parse_in_value(css_input, pos, astatus, afrom, invalid_at, str_char, str_size)

            print("Pre Status: {}, Current Status: {}".format(old_status, astatus))



    def record_position(self, old_status, new_status, css_input, pos, str_size, force = False):
        record = False

        # any state into a comment
        if new_status == "PIC":
            record = True

        # start of a porperty
        if old_status == "PIS" and new_status == "PIP":
            record = True
        if old_status == "PIV" and new_status == "PIP":
            record = True

        # from porperties to values
        if old_status == "PIP" and new_status == "PIV":
            record = True

        # starting a new selector
        if old_status == "PIV" and new_status == "PIS":
            record = True
        if old_status == "PIP" and new_status == "PIS":
            record = True

        if record or force:

            self.start_pos = re.search("(?! |\n|\t|\r)", css_input[pos:]).start() + pos
            if self.start_pos >= str_size:
                self.start_pos = -1

            self.start_line = self.line
            print("Start Posistion: {}, Start Line: {}".format(self.start_pos, self.start_line))




    def parse_in_selector(self, css_input, pos, astatus, afrom, invalid_at, str_char, str_size):
        if(self.is_token(css_input, pos)):
            print("PIS Is Token")

            if css_input[pos] == '/' and CssUtils().s_at(css_input, pos + 1) == '*':
                afrom = "PIS"
                astatus = "PIC"
                ++ pos

            elif css_input[pos] == '"' or css_input[pos] == '\'':
                self.cur_string = css_input[pos]
                astatus = "PINSTR"
                self.str_char = css_input[pos]
                afrom = "PIS"
            elif css_input[pos] == '{':
                astatus = "PIP"
                self.add_token("SEL_START", self.cur_selector)

            elif css_input[pos] == '}':
                self.add_token("AT_END", self.cur_at)
                self.cur_at = ""
                self.cur_selector = ""
                self.sel_separate = dict()

            elif not (css_input[pos] == "*" and (CssUtils().s_at(css_input, pos + 1) == '.' or CssUtils().s_at(css_input, pos + 1) == '[' or CssUtils().s_at(css_input, pos + 1) == ':' or CssUtils().s_at(css_input, pos + 1) == '#')):
                self.cur_selector += css_input[pos]

        else:
            lastpos = len(self.cur_selector) - 1
            print("Last Posistion: {}".format(lastpos))

            if (lastpos == -1) or not ((CssUtils().ctype_space(self.cur_selector[lastpos]) or (self.is_token(self.cur_selector, lastpos) and self.cur_selector[lastpos] == ',')) and CssUtils().ctype_space(css_input[pos])):

                self.cur_selector += css_input[pos]

        return astatus, pos, afrom, invalid_at

    def parse_in_property(self, css_input, pos, astatus, afrom, invalid_at):
        if self.is_token(css_input, pos):
            print("PIP {} Is Token".format(css_input[pos]))
            if css_input[pos] == ':' or (css_input[pos] == '=' and not self.cur_property == ""):
                astatus = "PIV"
                self.add_token("PROPERTY", self.cur_property)

            elif css_input[pos] == '/' and CssUtils().s_at(css_input, pos+1) == '*' and self.cur_property == "":
                astatus = "PIC"
                ++ pos
                afrom = "PIP"

            elif css_input[pos] == '}':
                self.explode_selectors()
                astatus = "PIS"
                invalid_at = False
                self.add_token("SEL_END", self.cur_selector)
                self.cur_selector = ""
                self.cur_property = ""

            elif css_input[pos] == ';':
                cur_property = ""
            else:
                print("Unexpected character '{}'in property name".format(css_input[pos]))

        elif not CssUtils().ctype_space(css_input[pos]):
            self.cur_property += css_input[pos]

        return astatus, pos, afrom, invalid_at

    def parse_in_value(self, css_input, pos, astatus, afrom, invalid_at, str_char, str_size):
        pn = (((css_input[pos] == '\n' or css_input[pos] == '\r') and self.property_is_next(css_input, pos + 1)) or pos == str_size - 1)

        print("CSS InPut: {} Pin: {}".format(css_input[pos], pn))
        if pn:
            print("Added semicolon to the end of declaration")
        if self.is_token(css_input, pos) or pn:
            print("PIV {} Is Token".format(css_input[pos]))
            if css_input[pos] == '{':
                print("Unexpected character '{}' in {}".format(css_input[pos], self.cur_selector))

            if css_input[pos] == '/' and CssUtils().s_at(css_input, pos+1) == '*':
                astatus = "PIC"
                ++pos
                afrom = "PIV"
            elif css_input[pos] == ';' or pn:
                astatus = "PIP"
            elif not css_input[pos] == '}':
                self.cur_sub_value += css_input[pos]

            print("Selector: {}".format(self.cur_selector))
            if (css_input[pos] == '}' or css_input[pos] == ';' or pn) and not self.cur_selector == "" :

                if self.cur_at == "":
                    self.cur_at = "standard"

                # kill all whitespace
                self.cur_at = CssUtils().trim(self.cur_at)
                self.cur_selector = CssUtils().trim(self.cur_selector)
#                 self.cur_value = CssUtils().trim(self.cur_value)
                self.cur_property = CssUtils().trim(self.cur_property).lower()
                self.cur_sub_value = CssUtils().trim(self.cur_sub_value)

                if not self.cur_sub_value == "":
                    self.cur_sub_value_arr.append(self.cur_sub_value)
                    self.cur_sub_value = ""

                self.cur_value = CssUtils().build_value(self.cur_sub_value_arr)

                self.add_token("VALUE", self.cur_value)

                # Split multiple selectors here if necessary
                self.cur_property = ""
                self.cur_sub_value_arr = []
                self.cur_value = ""


        elif not pn:
            print("Sub Value: {}".format(css_input[pos]))
            self.cur_sub_value += css_input[pos]
            if CssUtils().ctype_space(css_input[pos]):
                if not CssUtils().trim(self.cur_sub_value) == "":
                    self.cur_sub_value_arr.append(self.cur_sub_value)
                self.cur_sub_value = ""

        return astatus, pos, afrom, invalid_at, pn



    def property_is_next(self, istring, pos):
        istring = istring[pos:len(istring)-pos]
        pos = re.search(':', istring).start() if re.search(':', istring) else pos
        if pos == -1:
            return False
        istring = CssUtils().trim(istring[0:pos]).lower()
#         print("Porperty: {}, Posistion: {}".format(istring, pos))
        return True

    def is_token(self, istring, pos):
        return CssUtils().is_str_array(self.tokens, istring[pos]) and not (CssUtils().escaped(istring, pos))

    def add_token(self, tokentype, data, force = False):
        temp = dict()
        tempdata = data if tokentype == "COMMENT" else CssUtils().trim(data)
        temp = {'Type': tokentype, 'Posistion': self.start_pos, 'Line': self.start_line, 'Data': tempdata}

        # multidimensional dictionary
        self.csstokens.setdefault(self.start_line, {})[tokentype] = temp

        print("Line: {} Token: {}".format(self.start_line, self.csstokens[self.start_line]))

        if tokentype == "SEL_START":
            self.selector_nest_level += 1
        if tokentype == "SEL_END":
            self.selector_nest_level -= 1

    def get_next_token(self):

        atoken = dict()

        while self.token_ptr <= len(self.csstokens):
            for tokentype in self.csstokens[self.token_ptr]:
                atoken = self.csstokens[self.token_ptr][tokentype]
                print("Pos: {} Line: {} Type: {} Data: {}".format(atoken["Posistion"], atoken["Line"], atoken["Type"], atoken["Data"]))

            self.token_ptr += 1


    def get_type_name(self, ttype):
        return self.token_type_names[ttype]

    def explode_selectors(self):
        self.sel_separate = dict()
