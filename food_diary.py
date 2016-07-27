#! /usr/bin/python
# -*- coding: UTF-8 -*-

# script that serves the diary entries from the mysql database

import cgi
import cgitb
import MySQLdb
import yaml

cgitb.enable()

with open('credentials.yml', 'r') as c:
    cred = yaml.load(c)

db = MySQLdb.connect(host='localhost',
                     user=cred['user'],
                     passwd=cred['password'],
                     db='food_diary')

cur = db.cursor()

form = cgi.FieldStorage()
if 'delete' in form:
    cur.execute('delete from entries where \
            date = %s and breakfast = %s and lunch = %s and dinner = %s limit 1',
            (str(form['date'].value),
            str(form.getvalue('breakfast', '')),
            str(form.getvalue('lunch', '')),
            str(form.getvalue('dinner', ''))))
if 'date' in form and 'delete' not in form:
    cur.execute('insert into entries (date, breakfast, lunch, dinner) values \
            (%s, %s, %s, %s)', (form.getvalue('date', ''),
                                form.getvalue('breakfast', ''),
                                form.getvalue('lunch', ''),
                                form.getvalue('dinner', '')))

cur.execute('select * from entries order by date')

print "Content-Type: text/html\n"

print "<table border='1' width='100%'>"
print "<tr><th style='width:24%'>Date</th> \
        <th style='width:24%'>Breakfast</th> \
        <th style='width:24%'>Lunch</th> \
        <th style='width:24%'>Dinner</th> \
        <th style='width:4%'>Delete</th></tr>"

row_type = {0: 'date', 1: 'breakfast', 2: 'lunch', 3: 'dinner'}
rows = cur.fetchall()
for i, row in enumerate(rows):
    display = ' class="hidden" style="display:None;"' if i < len(rows) - 30 else ''
    print "<tr{0} id='row{1}'>".format(display, i)
    for j, item in enumerate(row):
        print "<td onclick='editElem(\"{0}{1}\");'><center id='{0}{1}'>".format(i, row_type[j])+str(item)+"</center></td>"
    print "<td><input type='button' value='X' onclick='deleteRow({0})'></td>".format(i)
    print "</tr>"

print "</table>"
db.close()
