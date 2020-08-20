import json


def print_ast_stack(stack):
  for item in stack:
    print("---")
    print(item)


def pretty_print(value):
  print(json.dumps(value, indent=2))
