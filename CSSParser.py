import re
from cssutils import CssUtils

class CssParser:

    # PAT: parsing at-block, such as @charset, @namespace, and @import 
    parse_status = ["PIS", "PIP", "PIV", "PINSTR", "PIC", "PAT"]
    token_type = ["CHARSET", "IMPORT", "NAMESP", "AT_START", "AT_END", "SEL_START", "SEL_END", "PROPERTY", "VALUE", "COMMENT", "CSS_END"]


    """Docstring for CssParser. """
    def __init__(self):
        self.tokens = "{};:()@='\"/,\\!$%&*+.<>?[]^`|~"
        self.token_ptr = 0
        self.line = 1
        self.start_line= 0
        self.start_pos = 0
        self.cur_sub_value_arr = dict()
        self.cur_function_arr = dict()

    def parse_css(self, css_input):

        astatus = "PIS"
        old_status = "PIS"
        afrom = []
        str_char = []
        str_in_str = False
        invalid_at = False
        self.record_position("PIS", "PIS", css_input, 0, True)

        str_size = len(css_input)
        print("String Size: {}".format(str_size))
        for pos, string in enumerate(css_input):
            if string == '\n' or string == '\r':
                self.line += 1
#                 print("Start Line: {}".format(self.line))

            # record current position for selected state transitions
            if old_status != astatus:
                self.record_position(old_status, astatus, css_input, pos)

            old_status = astatus

            if astatus == "PIS":
                self.parse_in_selector(css_input, pos, astatus, afrom, invalid_at, str_char, str_size)



    def record_position(self, old_status, new_status, css_input, pos, force = False):
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
            start_pos = re.search(r"^[( |\n|\t|\r|\0xb)]", css_input[pos:]).start()
            self.start_line = self.line
            print("Start Positopn: {}, Start Line: {}".format(start_pos, self.start_line))

    def parse_in_selector(self, css_input, pos, astatus, afrom, invalid_at, str_char, str_size):
        if(self.is_token(css_input, pos)):
            print("Is Token")

    def is_token(self, istring, pos):
        return CssUtils().is_str_array(self.tokens, istring[pos]) and not (CssUtils().escaped(istring, pos))


