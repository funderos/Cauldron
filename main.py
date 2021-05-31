#!/usr/bin/env python
"""Script for starting Cauldron application (development web server) in debug mode"""

from website import create_app

__author__ = "Benjamin Funder"
__version__ = "1.0"

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
