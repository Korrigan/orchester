#!env python

import sys

from orchester.master import app, setup


if __name__ == '__main__':
    host = 'localhost'
    port = 5000
    setup()
    if len(sys.argv) >= 2:
        host = sys.argv[1]
    if len(sys.argv) >= 3:
        port = int(sys.argv[2])
    app.run(host=host, port=port, debug=True)
