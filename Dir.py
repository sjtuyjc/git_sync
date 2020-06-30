#class Dir
import os
import glob
import hashlib
from filecmp import dircmp

class Dir(object):
  
  def __init__(self, name, path, root_path, editor = set(), delete = set()):
    self.name = name
    self.root_path = root_path
    self.path = path
    self.editor = editor
    self.delete = delete
    self.able = True
    self.files = {}
    self.subdirs = {}

#print the info of dir
  def print_dir(self):
    print('name:' + self.name + '\tpath:' + self.path + '\teditor:', end = '')
    print(self.editor, end = '\t')
    if len(self.delete) > 0:
      print('(deleted by ', end = '')
      print(self.delete)
      print(')')
    else:
      print('')
    for i in self.subdirs.values():
      i.print_dir()
    for i in self.files.values():
      print('name:' + i.name + '\tpath:' + i.path + '\teditor:', end = '')
      print(i.editor, end = '\t')
      if len(i.delete) > 0:
        print('\t(deleted by ', end = '')
        print(i.delete, end = '')
        print(')')
      else:
        print('')

  def print_dir_plus(self):
    print(os.path.join(os.path.split(self.root_path)[1], self.path) + ':')
    self.print_dir()
    print('')

#collect the files and subdirs in the dir
  def dir_init(self):
    os.chdir(os.path.join(self.root_path, self.path))
    for i in os.listdir('.'):
      if os.path.isfile(i):
        self.files[i] = (Dir(i, os.path.join(self.path, i), self.root_path, self.editor)) 
      if os.path.isdir(i):
        self.subdirs[i] = (Dir(i, os.path.join(self.path, i), self.root_path, self.editor))
    for i in self.subdirs.values():
      i.dir_init()
    os.chdir(self.root_path)

#compare two dirs and merge the editor
  def merge_with(self, dir):
    dcmp = dircmp(os.path.join(self.root_path, self.path), os.path.join(dir.root_path, dir.path))
    for i in dcmp.left_only + dcmp.common_funny:
      if i in self.files.keys():
        self.files.get(i).delete = self.files.get(i).delete.union(dir.editor)
      if i in self.subdirs.keys():
        self.subdirs.get(i).delete = self.subdirs.get(i).delete.union(dir.editor)
    for i in self.files.keys():
      if i in set(dcmp.common_files) - set(dcmp.same_files):
        self.files.get(i).editor = self.files.get(i).editor.union(dir.editor)
    for i in self.subdirs.keys():
      if i in dcmp.common_dirs:
        self.subdirs.get(i).merge_with(dir.subdirs.get(i))
    for i in dcmp.right_only:
      if i in dir.files.keys():
        if i in self.files.keys():
          self.files.get(i).editor = self.files.get(i).editor.union(dir.editor)
        else:
          self.files[i] = dir.files.get(i)
          self.files.get(i).root_path = self.root_path
      if i in dir.subdirs.keys():
        if i in self.subdirs.keys():
          self.subdirs.get(i).subdir_merge(dir.subdirs.get(i), glob.file_wkspc.get(list(self.subdirs.get(i).editor)[0]).root_path)
        else:
          self.subdirs[i] = dir.subdirs.get(i)
          self.subdirs.get(i).root_path = self.root_path
  
  def subdir_merge(self, dir, new_path):
    dcmp = dircmp(os.path.join(new_path, self.path), os.path.join(dir.root_path, dir.path))
    for i in dcmp.common_dirs:
      self.subdirs.get(i).subdir_merge(dir.subdirs.get(i), new_path)
    for i in set(dcmp.common_files) - set(dcmp.same_files):
      self.files.get(i).editor = self.files.get(i).editor.union(dir.editor)
    for i in dcmp.right_only:
      if i in dir.files.keys():
        self.files[i] = dir.files.get(i)
        self.files.get(i).root_path = self.root_path
      if i in dir.subdirs.keys():
        self.subdirs[i] = dir.subdirs.get(i)
        self.subdirs.get(i).root_path = self.root_path

#print info of compare between two dirs
  def compare_report(self, dir):
    print('in ' + self.path + ':')
    edi = list(dir.editor)[0]
    dcmp = dircmp(os.path.join(self.root_path, self.path), os.path.join(dir.root_path, dir.path))
    for i in dcmp.common_funny + dcmp.funny_files:
      print('funny file: ' + i)
    for i in dcmp.same_files:
      print('same file: ' + i)
    for i in dcmp.left_only:
      print('delete ' + i + ' by ' + edi)
    for i in (set(dcmp.common_files) - set(dcmp.same_files)):
      print('edit ' + i + ' by ' + edi)
    for i in dcmp.right_only:
      print('add ' + i + ' by ' + edi)
    for i in dcmp.common_dirs:
      self.subdirs.get(i).compare_report(dir.subdirs.get(i))

  def compare_report_plus(self, dir):
    tmp_path1 = os.path.join(os.path.split(self.root_path)[1], self.path)
    tmp_path2 = os.path.join(os.path.split(dir.root_path)[1], dir.path)
    print('compare ' + tmp_path1 + ' with ' + tmp_path2)
    self.compare_report(dir)
    print('')

#if there is more than one editors or files deleted, turn enable to false    
  def check_change(self):
    for i in self.files.values():
      if len(i.editor) > 1:
        i.able = False
      if len(i.delete) > 0:
        i.able = False
      self.editor = self.editor.union(i.editor)
      if i.able == False:
        self.able = False
    for i in self.files.keys():
      if i in self.subdirs.keys():
        self.able = False
    for i in self.subdirs.values():
      if len(i.delete) > 0:
        i.able = False
      i.check_change()
      self.editor = self.editor.union(i.editor)
      if i.able == False:
        self.able = False

#print the info of reasons why merge failed
  def conflict_log(self):
    if self.able == False:
      if len(self.delete) > 0:
        print(self.path + ' deleted by ', end = '')
        print(self.delete)
      for i in self.files.values():
        if len(i.editor) > 1:
          print(i.path + ' edited by ', end = '')
          print(i.editor)
        if len(i.delete) > 0:
          print(i.path + ' deleted by ', end = '')
          print(i.delete)
      for i in self.files.keys():
        if i in self.subdirs.keys():
          print(self.files.get(i).path + ' exist a subdir of the same name')
      for i in self.subdirs.values():
        i.conflict_log()

  def conflict_log_plus(self):
    print('WHY?')
    self.conflict_log()
    print('')
