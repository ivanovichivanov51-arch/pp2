x = 300

def myfunc():
  x = 200
  print(x)

myfunc()

print(x)


def myfunc():
  x = 300
  def myinnerfunc():
    print(x)
  myinnerfunc()

myfunc()

def myfunc():
  x = 300
  print(x)

myfunc()

x = 300

def myfunc():
  global x
  x = 200

myfunc()

print(x)

