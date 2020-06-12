import json


def print_ast_stack(stack):
  for item in stack:
    print("---")
    print(item)


def print_json(value):
  print(json.dumps(value, indent=2))
