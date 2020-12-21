from internet_object.utils import helpers
from internet_object.core import errors, undefined


class TypeDef:


  def clean(_, value, node, memberDef):

    # When data is not passed, it is set as None
    if node is None:
      # Ensure that optional is True
      if memberDef.optional:
        # import pdb; pdb.set_trace()
        return memberDef.get("default") or undefined, True
      else:
        raise errors.VALUE_REQUIRED

    # data is set as None
    if value is None:
      if memberDef.nullable:
        return None, True

    return value, False

  def parse(self, node, memberDef):
    val = None if node is None else node.val
    val, is_final = self.clean(val, node, memberDef)
    if is_final:
      return val

    is_valid, reason = self.validate(val, memberDef)
    if is_valid is False:
      typename = self.typename or ''
      path = memberDef.get('path') or memberDef.get('name')
      helpers.pretty_print(memberDef)
      raise errors.ValidationError(
        "validation-failed (%s.%s) for %s at %s,%s" % (
          typename, reason, path, node.row, node.col
        )
      )

    return val
