import sys

from main import create_app

if __name__ == '__main__':
    path = './main'
    if path not in sys.path:
        sys.path.append(path)
    app = create_app()
    app.run()




