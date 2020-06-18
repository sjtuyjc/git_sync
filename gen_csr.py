import os
import re
import glob
import shutil
import datetime
import time
from Dir import Dir
from Module import Module

work_path = os.getcwd()

names = locals()
for i in glob.module_list:
  names[i] = Module(i)
  glob.module_wkspc.append(names[i]) 

if __name__ == '__main__':
  for i in glob.module_wkspc[2:]:
    i.git_clone()
    i.generate_csr()
    i.recover_file(glob.dir_recover)
    i.add_commit('.', 'regenerate csr')
    i.git_push()
    os.chdir(work_path)