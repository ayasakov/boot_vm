from distutils.core import setup


def main():
    setup(name='ExecuteCommand',
      version='1.0',
      py_modules=['executecommand'])

    setup(name='TestExecuteCommand',
          version='1.0',
          py_modules=['testexecutecommand'])

if __name__ == "__main__":
    main()