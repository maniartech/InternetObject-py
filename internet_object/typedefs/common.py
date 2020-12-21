from core import errors, undefined

def clean(value, node, memberDef):

  # When data is not passed, it is set as None
  if node is None:
    # Ensure that optional is True
    if memberDef.optional:
      return memberDef.default or undefined, True
    else:
      raise errors.VALUE_REQUIRED

  # data is set as None
  if value is None:
    if memberDef.nullable:
      return None, True

  return value, False
