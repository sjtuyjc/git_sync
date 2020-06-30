#merge specific dirs in all different repos
import os
import re
import glob
import shutil
import datetime
import time
from Dir import Dir
from Module import Module
from filecmp import dircmp
from shell import remove
from shell import move_file
from sv_protect import sv_protect

work_path = os.getcwd()

names = locals()
for i in glob.module_list:
  names[i] = Module(i)
  glob.module_wkspc.append(names[i]) 

#after merge where to checkout the dirs and files
def checkout(dir, l):
  for i in dir.files.values():
    if len(i.editor) == 0:
      l.get('root').append(i.path)
    elif len(i.editor) == 1:
      l.get(list(i.editor)[0]).append(i.path)
  for i in dir.subdirs.values():
    if len(i.editor) == 0:
      l.get('root').append(i.path)
    elif len(i.editor) == 1:
      l.get(list(i.editor)[0]).append(i.path)
    else:
      checkout(i, l)

#make an empty repo at local and return the module
def git_init(repo):
  os.mkdir(repo)
  tmp = Module(repo, True)
  os.chdir(tmp.url)
  os.system('git init')
  os.chdir(work_path)
  return tmp

if __name__ == '__main__':
  print('MERGE REPORT OF ' + datetime.datetime.now().strftime("%Y%m%d"))
  for i in glob.module_wkspc:
    i.git_clone()
    os.chdir(i.url)
    #if (glob.dic[i.name] + '_top.shell.sv' in os.listdir(os.path.join('common','abstract'))):
    #  os.system('rm -rf common/abstract/' + glob.dic[i.name] + '_top.shell.sv')
    #if os.path.isdir(glob.dic[i.name]) and glob.dic[i.name] not in ['common', 'tools', 'verif', 'core', 'fullchip'] and 'rtl' in os.listdir(glob.dic[i.name]):
    #  if glob.dic[i.name] + '_top.sv' in os.listdir(os.path.join(glob.dic[i.name], 'rtl')):
    #    os.chdir(glob.dic[i.name] + '/rtl')
    #    tmp = os.system('vcs -full64 -sverilog -auto2protect128 ' + glob.dic[i.name] + '_top.sv')
    #    if tmp == 0:
    #      remove(glob.dic[i.name] + '_top.svp', '`protected128\n', '`endprotected128\n')
    #      os.system('mv ' + glob.dic[i.name] + '_top.svp ' + glob.dic[i.name] + '_top.shell.sv')
    #      move_file(glob.dic[i.name] + '_top.shell.sv')
    for files in os.listdir('.') :
      if i.name not in ['dlc_fullchip', 'dlc_core'] and os.path.isdir(files) and 'rtl' in os.listdir(files) and files + '_top.sv' in os.listdir(os.path.join(files, 'rtl')):
        os.chdir(os.path.join(files, 'rtl'))
        tmp = os.system('vcs -full64 -sverilog -auto2protect128 ' + files + '_top.sv')
        if tmp == 0 :
          remove(files + '_top.svp', '`protected128\n', '`endprotected128\n')
          os.system('mv -f ' + files + '_top.svp ' + os.path.join(i.url, 'common', 'abstract', files + '_top.shell.sv'))
        os.chdir(i.url)
    i.add_commit('common', 'update shell.sv according to top.sv')
    os.chdir(work_path)
  for dir in glob.dir_to_sync:
    checkout_list = {}
    checkout_list['root'] = []
    for i in glob.module_list:
      checkout_list[i] = []
    os.chdir(glob.module_wkspc[0].url)
    os.system('git log --pretty=oneline | grep \'sync ' + dir + ' to ' + glob.module_wkspc[0].name + '\' > tmp.txt')
    root_commit = ''
    try:
      f = open('tmp.txt', 'r')
      root_commit = f.read(10)
    finally:
      if f:
        f.close()
    #print(root_commit)
    os.remove('tmp.txt')
    if len(root_commit) == 0:
      print('getting root commit id failed')
    else:
      os.chdir(work_path)
      root = Module(glob.module_list[0])
      root.git_clone('root')
      #print(root.url)
      os.chdir(root.url)
      os.system('git reset --hard ' + root_commit)
      root_dir = Dir(dir, dir, root.url)
      root_dir.dir_init()
      #root_dir.print_dir_plus()
      os.chdir(work_path)  
      for i in glob.module_wkspc:
        os.chdir(i.url)
        tmp = Dir(dir, dir, i.url, {i.name})
        tmp.dir_init()
        #tmp.print_dir_plus()
        glob.file_wkspc[i.name] = tmp
      for i in glob.file_wkspc.values():
        #root_dir.compare_report_plus(i)
        root_dir.merge_with(i)
      print('after merge:')
      root_dir.print_dir_plus()
      root_dir.check_change()
      if root_dir.able == False:
        print('merge failed')
        root_dir.conflict_log_plus()
      else:
        print('merge successed')
        checkout(root_dir, checkout_list)
        print(checkout_list)
        print('\n')
        os.chdir(work_path)
        sync = git_init('sync')
        for i in glob.module_wkspc:
          sync.add_remote(i)
          for j in checkout_list.get(i.name):
            sync.checkout_remote(i, j)
        sync.remove_remote()
        sync.add_commit(dir, 'merge all')
        for i in glob.module_wkspc:
          i.add_remote(sync)
          i.checkout_remote(sync, dir)
          i.remove_remote()
          os.chdir(i.url)
          i.add_commit(dir, 'sync ' + dir + ' to ' + i.name)
          if glob.module_wkspc.index(i) == 0:
            i.check_commit('sync ' + dir + ' to ' + i.name)
          i.git_push() 
    os.chdir(work_path)
    os.system('rm -rf sync root')
  #for i in glob.module_wkspc:
  #  if i.name not in ['dlc_fullchip', 'dlc_core']:
  #    i.generate_csr()
  #    i.recover_file(glob.dir_recover)
  #    i.add_commit('.', 'regenerate csr')
  #    i.git_push()