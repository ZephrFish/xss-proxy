# xss-proxy
BeEF-inspired XSS proxy service

Dependencies:
pip install flask

pip install flask-cors


This is just a PoC atm...

run app.py
from same directory, run python -m SimpleHTTPServer

open xss-proxy.html hosted by SimpleHTTPSever

sqlite database will get updated with responses made by the xss script


Helper scripts:

run makedb.py to create/reset the database dummy data

run dbtest.py to view database contents
