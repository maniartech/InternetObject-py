from utils import is_scalar
from core import parse, InternetObject
from .common import clean

class ArrayDef:

  definition = InternetObject.parse(
                  r"""
                  type?: {string, default:string, choices:[string]},
                  default: string,
                  minLen: {int, min:0},
                  maxLen: {int, min:0},
                  len: {int, min:0},
                  "null": bool,
                  optional: bool
                  """
                )

  def parse(self, node, memberDef):
    val, is_final = clean(node, memberDef)

    if is_final:
      return val


