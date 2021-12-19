import inspect
from pprint import pprint


def foo():

   name = inspect.stack()[0].filename
   name = name.split('\\')[-1][:-3]
   pprint(name)
   print('\n\n')
   pprint(inspect.stack()[1])


foo()
