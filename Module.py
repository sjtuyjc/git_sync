import os
import re
import glob

class Module(object):

  def __init__(self, name, local = False):
    self.name = name
    self.local = local
    if local == False:
      self.url = 'ssh://' + glob.user + '@' + glob.localhost + self.name
    else:
      self.url = os.path.join(os.getcwd(), self.name)
    self.remotes = []

  def git_clone(self, dir_name = ''):
    if self.local == False:
      if len(dir_name) != 0:
        os.system('git clone ' + self.url + ' ' + dir_name)
        self.local = True
        self.url = os.path.join(os.getcwd(), dir_name)
      else:
        os.system('git clone ' + self.url)
        self.local = True
        self.url = os.path.join(os.getcwd(), self.name)
    else:
      print('Already in local')

  def add_remote(self, remote):
    os.chdir(self.url)
    os.system('git remote add -f ' + remote.name + ' ' +  remote.url)
    self.remotes.append(remote.name)

  def remove_remote(self):
    os.chdir(self.url)
    for i in self.remotes:
      os.system('git remote remove ' + i)

  def checkout_remote(self, remote, dir = 'common'):
    os.chdir(self.url)
    os.system('git checkout ' + remote.name + '/master ' + dir)

  def recover_file(self, file_list):
    os.chdir(self.url)
    file_str = ' '.join(file_list)
    os.system('rm -rf ' + file_str)
    os.system('git checkout HEAD ' + file_str)

  def generate_csr(self):
    os.chdir(self.url)
    for files in os.listdir('.'):
      if os.path.isdir(files) and 'csr' in os.listdir(files):
        for csr_file in os.listdir(os.path.join(files, 'csr')):
          if re.match(r'.+_pb.txt', csr_file):
            os.system('tools/gcsr -b ' + files + '/csr/' + csr_file + ' -rtl -m ' + files)

  def add_commit(self, dir = 'common/', comment = 'a commit by '+ glob.user):
    os.chdir(self.url) 
    os.system('git add ' + dir)
    os.system('git commit -m \'' + comment + '\'')

  def check_commit(self, str):
    match_dir = r'.*' + str + r'.*'
    os.chdir(self.url)
    latest_commit = os.popen('git log --oneline -1').read()
    if re.match(match_dir, latest_commit):
      pass
    else:
      os.system('git commit --allow-empty -m \'' + str + ' (empty)\'')

  def change_commit(self, comment):
    os.chdir(self.url)
    os.system('git commit --amend -m \'' + comment + '\'')

  def git_review(self):
    os.chdir(self.url)
    os.system('git remote rename origin gerrit')
    os.system('git review')

  def git_push(self):
    os.chdir(self.url)
    os.system('git push')

