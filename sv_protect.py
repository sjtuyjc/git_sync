import os

def sv_protect(form = '.sv',res = '.svp', exclude = ('common', 'tools', 'core', 'fullchip', 'verif')):
  form_len = 0 - len(form)
  for i in os.listdir('.'):
    if os.path.isfile(i) and i[form_len:] == form:
      print(i)
      tmp = os.system('vcs -full64 -sverilog -auto2protect128 ' + i)
      if tmp == 0:
        os.system('rm ' + i)
        os.system('mv ' + i[:form_len] + res + ' ' + i)
    elif os.path.isdir(i) and i not in exclude:
      print(i)
      pwd = os.getcwd()
      os.chdir(i)
      sv_protect(form, res, set())
      os.chdir(pwd)
    else:
      pass

if __name__ == "__main__":
  os.system('source ~/.bashrc')
  sv_protect()
