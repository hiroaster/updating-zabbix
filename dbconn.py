#!/usr/bin/env python
#edit: wenyang
#
# -*- coding: utf-8 -*-
# encoding: utf-8
#!/usr/bin/python

import MySQLdb
import time
ISOTIMEFORMAT='%Y-%m-%d'
today = time.strftime(ISOTIMEFORMAT,time.localtime())

def get_status(hostname,db_ip,db_user,db_pass):


    db = MySQLdb.connect(db_ip,db_user,db_pass,"enigma")
    cursor = db.cursor()

    sql = "select Hostname,Itemname,Portstatus,Portdesc from  alert_rule  where Hostname='"+hostname+"'"

  #  sql=sql_base+sql_body
    try:

        #results = cursor.execute(sql)
        cursor.execute(sql)
        results = cursor.fetchall()
        if results:
            return results
        else:
            return False
    except:
        print "Error: unable to fecth data"
    db.close()




