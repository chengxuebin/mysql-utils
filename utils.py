import re

"""some simple utilities.

"""
__author__ = "chengxuebin@outlook.com"
__copyright__ = "Copyright 2022 RBXBZD"
__license__ = "MIT"
__version__ = "1.0"


class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'


class PrettyPrint:
  def __init__(self, col_options):
    self.col_options = col_options

  def CountChineseCharacters(self, str):
    count = 0
    for x in str:
      if re.search(u'[\u4e00-\u9fff]', x) != None:
        count += 1
    return count

  def PrintSplitRow(self):
    format = ""
    # 补位字符为-
    options = {"c": "-"}
    for i, o in enumerate(self.col_options):
      format += "+{c:{c}<{w" + str(i) + "}}"
      options["w"+str(i)] = o["width"]
    format += "+"
    print(format.format(**options))

  def PrintRow(self, cols):
    if len(cols) != len(self.col_options):
      raise RuntimeError("Coloum count is mismatched.")
    format = ""
    # 补位字符为空格
    options = {"c": " "}
    # 每列首页各有1个空格
    col_space = 2
    for i, o in enumerate(self.col_options):
      col = cols[i]
      # 计算字符串内的中文字符数
      wchar_count = self.CountChineseCharacters(str(col))
      format += "| {col" + str(i) + ":{c}" + o["align"] + "{w" + str(i) + "}} "
      # 每个中文字符占用2个西文字符宽度，所以总长度要缩短
      options["w"+str(i)] = o["width"]-wchar_count-col_space
      options["col"+str(i)] = col
    format += "|"
    print(format.format(**options))
