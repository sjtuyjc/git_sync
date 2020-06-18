import os

def remove(target_file, start_str, end_str):
  if not os.path.isfile(target_file):
    print('file cannot found')
    return 1
  with open(target_file, 'r') as f:
    lines = f.readlines()
  start_index = 0
  end_index = 0
  for i in range(len(lines)):
    if lines[i] == start_str:
      start_index = i
    if lines[i] == end_str:
      end_index = i
  if not (start_index and end_index):
    print('str cannot found')
    return 1
  else:
    lines = lines[:start_index] + lines[end_index+1:]
  with open(target_file, 'w') as f:
    f.writelines(lines)
  return 0

def move_file(src_file, target_path = '../../common/abstract/'):
  if not os.path.isfile(src_file):
    print('file cannot found')
    return(1)
  os.system('mv ' + src_file + ' ' + target_path)
