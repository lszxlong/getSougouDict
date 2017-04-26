import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
importr("cidian")
ss = robjects.r('decode_scel(scel = "/home/zxl/IdeaProjects/python/getSougouDict1/dict/1/185577588.scel", output = "/home/zxl/IdeaProjects/python/getSougouDict/2.txt", cpp =  TRUE)')
print(ss)