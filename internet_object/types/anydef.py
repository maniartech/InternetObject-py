from utils import is_scalar


class AnyDef:

  def parse(self, tree, memberDef):

    if is_scalar(tree):
      return tree.val



