import re


re_white_space = re.compile(r'[\s]')

re_separator = re.compile(r'[\{\}\[\]\:\,~]')

re_not_separator = re.compile(r'[^\{\}\[\]\:\,~]')

re_not_regular_string = re.compile(r'[^\"]')

re_regular_string = re.compile(r"^\"(?:[^\"\\]|\\.)*\"$")

re_number = re.compile(r"^([-+]?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?)$")
