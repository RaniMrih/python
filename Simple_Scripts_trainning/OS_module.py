import os
from datetime import datetime

#print all os attr
#print(dir(os))

#print working directory
# print(os.getcwd())
# os.chdir('/Users/rmrih/Rani_GitHub/python/Simple_Scripts_trainning')
# print(os.getcwd())

#list all files in current directory
# print(os.listdir())

#create directory
#os.mkdir('Test-dir')
#create directory and sub dir
# os.makedirs('Test-dir/sub-test-dir')

#remove directory
#os.rmdir('Test-dir')
#remove directory and sub dir
# os.removedirs('Test-dir/sub-test-dir')

#rename files
# os.rename('org-file.txt','new-file-name.txt')

#file status
# print(os.stat('oop.py'))
# print(os.stat('oop.py').st_size)

#get file modification time
# mod_time=os.stat('oop.py').st_mtime
# print(datetime.fromtimestamp(mod_time))

#get all dir and files tree
# for dirpath, dirnames, filenames in os.walk(os.getcwd()):
# for dirpath, dirnames, filenames in os.walk('/Users/rmrih/Rani_GitHub/python/Simple_Scripts_trainning'):
#     print('Current path : ', dirpath)
#     print('Directories : ', dirnames)
#     print('Files : ', filenames)
#     print()

#print env variables
#print(os.environ)
# print(os.environ.get('HOME'))

#create file in my home directory(dont work)
# path="/Users/rmrih/"
# print(os.environ.get('~'))
# file_path = os.path.join(os.environ.get('/Users/rmrih/'),'test.txt')
# print(file_path)

#check if exists
# print(os.path.exists('/Users/rmrih/test.txt'))

#split directory path and file name
# print(os.path.split('/Users/rmrih/Desktop/test.txt'))

#get only directory path
# print(os.path.dirname('/Users/rmrih/Desktop/test.txt'))

#get only file name
# print(os.path.basename('/Users/rmrih/Desktop/test.txt'))

#check if file or directory
# print(os.path.isfile('/Users/rmrih/Desktop/test.txt'))
# print(os.path.isdir('/Users/rmrih/'))

#all os.path usage
print(dir(os.path))









