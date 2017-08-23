#!/usr/bin/env python
#edit: wenyang
#
# -*- coding: utf-8 -*-
import json
import urllib2
import sys
class zabbixapi:
    def __init__(self,urlset,user,password):
        self.url = "http://"+urlset+"/api_jsonrpc.php"
        self.header = {"Content-Type": "application/json"}

        self.user = user
        self.password = password
        self.authID = self.user_login()

#get authentication code 
    def user_login(self):
        data = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "user.login",
                    "params": {
                        "user": self.user,
                        "password": self.password,
                        },
                    "id": 0
                    })
        request = urllib2.Request(self.url,data)
        for key in self.header:
            request.add_header(key,self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Auth Failed, Please Check Your Name And Password:",e.code
        else:
            response = json.loads(result.read())
            result.close()
            authID = response['result']
            return authID
            
            
#build a request : data in and response out             
    def get_data(self,data,hostip=""):
        request = urllib2.Request(self.url,data)
        for key in self.header:
            request.add_header(key,self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server could not fulfill the request.'
                print 'Error code: ', e.code
            return 0
        else:
            response = json.loads(result.read())
            result.close()
            return response

    def host_get(self,hostname):
        data = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "host.get",
                    "params": {
                        "output":"extend",
                        "filter": {"host": [hostname]}
                        },
                    "auth": self.authID,
                    "id": 1
                })
        res = self.get_data(data)['result']
        return res


    def temp_graph_get(self,hostid):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "graph.get",
                "params": {
                    "output": "extend",
                    "hostids": hostid,
                    "sortfield": "name",
#                    "filter":{"name":interface},
                },
                "auth":self.authID, 
                "id": 1
            }
   
        )
        res = self.get_data(data)
        return res



    def update_graph(self,params):  
        data = json.dumps(  
        {
        "jsonrpc": "2.0",
        "method": "graph.update",
        "params": params,
        "auth":self.authID, 
        "id": 1
               }
               )
        res = self.get_data(data)
        return res


    def item_get(self,hostid):
        data = json.dumps({
            
            
                "jsonrpc": "2.0",
                "method": "item.get",
                "params": {
                    "output": "extend",
                    "hostids": hostid,
        #            "filter":{"name":itemname},
                },
                
                "auth": self.authID, 
                "id": 1           
            
        })
        res = self.get_data(data)
        return res


    def item_update(self,params):
        data = json.dumps(
            
            {
                "jsonrpc": "2.0",
                "method": "item.update",
                "params": params,
                "auth": self.authID, 
                "id": 1
            }

        )
        res = self.get_data(data)
        return res 