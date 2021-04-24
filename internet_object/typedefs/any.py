from internet_object.typedefs.typedef import TypeDef
from internet_object.utils import is_scalar
from internet_object.core import parse, InternetObject
from .common import clean

class AnyDef(TypeDef):

  definition = InternetObject.parse(
                  r"""
                  type        : { name:type, type:string, default:"any", choices:["any"] },
                  default     : { name:default, type:any, optional:T },
                  choices     : { name:choices, type:array, of:any, optional:T },
                  optional    : { name:optional, type:bool, default:F },
                  "null"      : { name:"null", type:bool, default:F }
                  """
                )

  def __init__(self):
    self.typename = 'any'

  def validate(self, val, memberDef):
    return True, None
