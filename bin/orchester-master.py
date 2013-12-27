#!env python

from orchester.master import app, setup


if __name__ == '__main__':
    setup()
    app.run(debug=True)
