import re


if __name__ == "__main__":
    filepath = './css_style.txt'

    cssfile = open(filepath, 'r')
    csstext = cssfile.read()

    matches = re.findall("^\.icon.*\n+.*\n+}",  csstext, re.MULTILINE)

    for match in matches:
        print (match)


