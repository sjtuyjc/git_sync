import os
import re
import glob
from shell import remove
from shell import move_file
from sv_protect import sv_protect
from Module import Module

work_path = os.getcwd()

names = locals()
for i in glob.module_list[1:]:
  names[i] = Module(i)
  glob.module_wkspc.append(names[i])

if __name__ == '__main__':
  fullchip = Module(glob.module_list[0])
  fullchip.git_clone()
  core = Module(glob.module_list[1])
  core.git_clone()
  print(fullchip.url + '\n' + core.url)
  os.chdir(core.url)
  for i in os.listdir('.'):
    if (i not in ['common', 'tools', 'core', 'verif'] and os.path.isdir(i) and i[0] != '.'):
      os.system('rm -rf ' + i)
  os.chdir('verif')
  for i in os.listdir('.'):
    if (i != 'core'):
      os.system('rm -rf ' + i)
  os.chdir(core.url)
  for i in glob.module_wkspc[1:4]:
    core.add_remote(i)
    tmp = glob.dic.get(i.name) + ' verif'
    core.checkout_remote(i, tmp)
    #core.add_commit(tmp, 'sync ' + i.name + ' to ' + fullchip.name)
  os.chdir(core.url)
  #for i in os.listdir('.'):
  #  if os.path.isdir(i) and 'csr' in os.listdir(i):
  #    for j in os.listdir(os.path.join(i, 'csr')):
  #      if re.match(r'.+_pb.txt', j):
  #        os.system('tools/gcsr -b ' + i + '/csr/' + j + ' -rtl -m ' + i)
  #core.add_commit('common', 'sync shell')
  #sv_protect()
  core.recover_file(glob.dir_recover)
  core.add_commit('.', 'sync modules but not protect sv files')
  core.remove_remote()
  core.git_push()
  
  os.chdir(fullchip.url)
  for i in os.listdir('.'):
    if (i not in ['common', 'tools', 'fullchip', 'verif'] and os.path.isdir(i) and i[0] != '.'):
      os.system('rm -rf ' + i)
  os.chdir('verif')
  for i in os.listdir('.'):
    if (i != 'fullchip'):
      os.system('rm -rf ' + i)
  os.chdir(fullchip.url)
  for i in glob.module_wkspc:
    fullchip.add_remote(i)
    tmp = glob.dic.get(i.name) + ' verif'
    fullchip.checkout_remote(i, tmp)
    #fullchip.add_commit(tmp, 'sync ' + i.name + ' to ' + fullchip.name)
  #os.chdir(fullchip.url)
  #os.system('rm -rf common/abstract/*')
  #for i in os.listdir('.'):
  #  if os.path.isdir(i) and i not in ['common', 'tools', 'verif', 'fullchip'] and 'rtl' in os.listdir(i):
  #    if i + '_top.sv' in os.listdir(os.path.join(i, 'rtl')):
  #      os.chdir(i + '/rtl')
  #      tmp = os.system('vcs -full64 -sverilog -auto2protect128 ' + i + '_top.sv')
  #      if tmp == 0:
  #        remove(i + '_top.svp', '`protected128\n', '`endprotected128\n')
  #        os.system('mv ' + i + '_top.svp ' + i + '_top.shell.sv')
  #        move_file(i + '_top.shell.sv')
  #  os.chdir(fullchip.url)
  #for i in os.listdir('.'):
  #  if os.path.isdir(i) and 'csr' in os.listdir(i):
  #    for j in os.listdir(os.path.join(i, 'csr')):
  #      if re.match(r'.+_pb.txt', j):
  #        os.system('tools/gcsr -b ' + i + '/csr/' + j + ' -rtl -m ' + i)
  #fullchip.add_commit('common', 'sync shell')
  #sv_protect()
  fullchip.recover_file(glob.dir_recover)
  fullchip.add_commit('.', 'sync modules but not protect sv files')
  #fullchip.remove_remote()
  fullchip.git_push()
