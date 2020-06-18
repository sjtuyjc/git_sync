import os
import glob
import shutil
from Dir import Dir
from Module import Module
from filecmp import dircmp

work_path = os.getcwd()

names = locals()
for i in glob.module_list:
  names[i] = Module(i)
  glob.module_wkspc.append(names[i]) 

for i in glob.module_wkspc:
  i.git_clone()

for i in glob.module_wkspc[1:]:
  i.add_remote(glob.module_wkspc[0])
  for dir in glob.dir_to_sync:
    os.chdir(i.url)
    os.system('rm -rf ' + dir)
    i.checkout_remote(glob.module_wkspc[0], dir)
    i.add_commit(dir = dir, comment = 'sync from fullchip')
    i.git_push()
