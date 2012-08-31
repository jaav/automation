from bottle import run, default_app,debug, route
import sys
import commands
from funcs import say_hello_world


@route('/hello')
def hello():
    return say_hello_world()

app = default_app()
debug(True)

def main():
    run(host='localhost',port=8070)

if __name__ =='__main__':
    sys.exit(main())
