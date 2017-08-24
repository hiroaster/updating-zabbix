#!/usr/bin/env python
# edit: wenyang
#
# coding:utf-8
import os
import json
import sys
import ConfigParser
from multiprocessing import Process, Pool
from fuction import zabbixapi
from dbconn import get_status


def update_interface_info(params):
	hostname = params['hostname']
	itemname = params['itemname']
	desc = params['desc']
	stats = params['stats']
	zb_user = params['zb_user']
	zb_pass = params['zb_pass']
	zb_url = params['zb_url']

	test = zabbixapi(zb_url, zb_user, zb_pass)
	hostinfo = test.host_get(hostname)
	hostid = hostinfo[0]['hostid']

        # sync port description
	res = test.temp_graph_get(hostid)
	for i in range(len(res['result'])):
		graphid = res['result'][i]['graphid']
		graphname = res['result'][i]['name']
		if 'Eth-Trunk' in graphname:
			newname = graphname.split("-")[0] + "-" + graphname.split("-")[1]
		else:
			newname = graphname.split("-")[0]
		if itemname == newname:
			graph_params = {"graphid": graphid, 'name': itemname + "-" + desc}
			res = test.update_graph(graph_params)
			print res
			break

	item = test.item_get(hostid)
	for i in range(len(item['result'])):
		itemid = item['result'][i]['itemid']
		name = item['result'][i]['name']

		if stats == '1':
			if itemname == name.split(".")[0]:
				sta_params = {"itemid": itemid, "status": "0"}
				res1 = test.item_update(sta_params)
				print res1


def main():

    # define a list for store msg
	a = []

    # read db config file
	cf = ConfigParser.ConfigParser()
	cf.read("db.conf")
	secs = cf.sections()
	if 'db' in secs:
		db_ip = cf.get("db", "db_ip")
		db_user = cf.get("db", "db_user")
		db_pass = cf.get("db", "db_pass")
		zb_user = cf.get("db", "zb_user")
		zb_pass = cf.get("db", "zb_pass")
		zb_url = cf.get("db", "zb_url")

	else:
		sys.exit()

	filename = "swlist.txt"
	info = open(filename, 'r').readlines()
	for line in info:
		pool = Pool(10)
		try:
			hostname = line.split()[2]

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

				params = {

				'hostname':host,
				'itemname':itemname,
				'stats':stats,
				'desc':desc,
				'zb_user':zb_user,
				'zb_pass':zb_pass,
				'zb_url':zb_url,

				}

				pool.apply_async(update_interface_info,(params,))

			pool.close()
			pool.join()

			print host+" is done"

if __name__ == "__main__":
	main()
