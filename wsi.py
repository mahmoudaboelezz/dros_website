import os
import sys

# import wsgi
print(sys.path)
print(os.getcwd())
os.chdir(os.getcwd() + '/website')
print('######################')
print(os.getcwd())
