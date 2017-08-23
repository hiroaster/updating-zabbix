#!/usr/bin/env python
#edit: wenyang
#
#coding:utf-8
import os
import json
import sys
import ConfigParser
from fuction import zabbixapi
from dbconn import get_status



def update_graph_name(hostname,itemname,desc,user,password,urlline):
    test = zabbixapi(urlline,user,password)
    hostinfo = test.host_get(hostname)
    hostid = hostinfo[0]['hostid']
    res = test.temp_graph_get(hostid)
    for i in range(len(res['result'])):
        graphid = res['result'][i]['graphid']
        graphname = res['result'][i]['name']
        if 'Eth-Trunk' in graphname:
            newname = graphname.split("-")[0]+"-"+graphname.split("-")[1]
        else:
            newname  = graphname.split("-")[0]
        if  itemname == newname :
            params = {"graphid":graphid,'name':itemname+"-"+desc}  
            res = test.update_graph(params)    
            print res
            break


def update_item_status(hostname,itemname):
    test = zabbixapi(urlline,user,password)
    res = test.host_get(hostname)
    hostid = res[0]['hostid']
    item = test.item_get(hostid)
    for i in range(len(item['result'])):
        itemid = item['result'][i]['itemid']
        name = item['result'][i]['name']
        status = item['result'][i]['status']
        if itemname in name :
            params = {"itemid":itemid,"status":"0"}
            res = test.item_update(params)
            print res







def main():

    #define a list for store msg
    a=[]

    #read db config file
    cf = ConfigParser.ConfigParser()
    cf.read("db.conf")
    secs = cf.sections()
    if 'db' in secs:
        db_ip = cf.get("db", "db_ip")
        db_user = cf.get("db", "db_user")
        db_pass = cf.get("db", "db_pass")
        zb_user = cf.get("db", "zb_user")
        zb_pass = cf.get("db", "zb_pass")
        zb_url =  cf.get("db", "zb_url")

    else:
        sys.exit()

#determine if the new port-status changed,if changed update db.
    filename = "swlist.txt"
    info=open(filename,'r').readlines()
    for line in info:
        try:
            hostname= line.split()[2]

        except:
            continue
        else:
            res = get_status(hostname,db_ip,db_user,db_pass)
        if res:
        	for i in range(len(res)):
        		host = res[i][0]
        		itemname = res[i][1]
        		stats = res[i][2]
        		desc  = res[i][3]
        		try:
        			update_graph_name(host,itemname,desc,zb_user,zb_pass,zb_url)

        		except:
        			continue

        		if stats == '1':
        			rest = update_item_status(host,itemname)

