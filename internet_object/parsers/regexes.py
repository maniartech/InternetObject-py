import re


white_space = re.compile(r'[\s]')

separator = re.compile(r'[\{\}\[\]\:\,~]')

not_separator = re.compile(r'[^\{\}\[\]\:\,~]')

not_regular_string = re.compile(r'[^\"]')

regular_string = re.compile(r"^\"(?:[^\"\\]|\\.)*\"$")
