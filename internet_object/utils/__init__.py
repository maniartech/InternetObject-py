
def is_datatype(v):
  return v in [
      'any',
      'string',
      'number',
      'object',
      'array',
      'bool',
  ]


def is_scalar(v):
  return v in [
      'string',
      'number',
      'bool',
  ]


def is_container(v):
  return v in [
      'object',
      'array',
  ]
