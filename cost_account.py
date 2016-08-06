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
                     db='cost_account')

cur = db.cursor()

form = cgi.FieldStorage()
if 'delete' in form:
    with open('text', 'w') as t:
        t.write(str(form['date'].value))
    cur.execute('delete from entries where \
            date = %s and type = %s and description = %s and abs(cost - %s) <= 1e-5 limit 1',
            (str(form['date'].value),
            str(form.getvalue('type', '')),
            str(form.getvalue('description', '')),
            str(form.getvalue('cost', ''))))
if 'date' in form and 'delete' not in form:
    cur.execute('insert into entries (date, type, description, cost) values \
            (%s, %s, %s, %s)', (form.getvalue('date', ''),
                                form.getvalue('type', ''),
                                form.getvalue('description', ''),
                                form.getvalue('cost', '')))

cur.execute('select * from entries order by date')

print "Content-Type: text/html\n"

print "<table id='account_table' border='1' width='100%'>"
print "<tr><th style='width:24%'>Date</th> \
        <th style='width:24%'>Type</th> \
        <th style='width:24%'>Description</th> \
        <th style='width:24%'>Cost</th> \
        <th style='width:4%'>Delete</th></tr>"

row_type = {0: 'date', 1: 'type', 2: 'description', 3: 'cost'}
rows = cur.fetchall()
for i, row in enumerate(rows):
    display = ' class="hidden" style="display:None;"' if i < len(rows) - 30 else ''
    print "<tr{0} id='row{1}'>".format(display, i)
    for j, item in enumerate(row):
        var = '$' if j == 3 else ''
        print "<td onclick='editElem(\"{0}{1}\");'><center id='{0}{1}'>".format(i, row_type[j])+var+str(item)+"</center></td>"
    print "<td><input type='button' value='X' onclick='deleteRow({0})'></td>".format(i)
    print "</tr>"

print "</table>"
db.close()
