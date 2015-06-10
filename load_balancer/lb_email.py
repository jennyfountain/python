#!/usr/bin/python

__author__ = 'jfountain'
__version__ = "1.0.0"

"""

This module provides all of the objects to manipulate the lbvserver API

"""

import logging
import requests
import json
import jsonpath
import commands
import smtplib

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.ERROR)
headers = {'Content-type': 'application/x-www-form-urlencoded'}
session = requests.session()

FROM = 'xx@xx.com'
TO = ['xx@xx.com']
SUBJECT = 'xxx'

def main(host, user, password):
        host = host
        user = user
        password = password
        email = []
        vip_url = 'http://' + host + '/nitro/v1/config/lbvserver?view=summary'
        stats = session.get(vip_url,  auth=('xx', 'xx'))
        list = json.loads(stats.content)
        vip = jsonpath.jsonpath(list, "$..lbvserver[?(@.curstate=='UP')]")
        down_vip = jsonpath.jsonpath(list, "$..lbvserver[?(@.curstate=='DOWN')]")
        if down_vip:
            for down in down_vip:
                down_vip_name = down['name']
                email.append(down_vip_name + "vip is down.")
        for line in vip:
            vip_name = line['name']
            url = 'http://' + host + '/nitro/v1/config/lbvserver_service_binding/' + vip_name
            binding = session.get(url,  auth=('xxx', 'xxx'))
            servers = json.loads(binding.content)
            for obj in servers["lbvserver_service_binding"]:
                svrhost = obj['ipv46']
                server = commands.getoutput("psql -t --host localhost --port xxx --dbname xx --user www -c \"select xxx from xxx.xx where address = '"+ svrhost +"'\"")
                if obj["curstate"] == "DOWN":
                    email.append(svrhost + " in the " + vip_name + " is down")
                if server == "f":
                    email.append(svrhost + " in the " + vip_name + " vip is set to FALSE in opsdb but is in the LB")
                if server == "":
                    email.append(svrhost + " in the " + vip_name + " vip is NOT in opsdb")
        if email:
            text = "\n".join(email)
            message = 'Subject: %s\n\n%s' % (SUBJECT, text)

            server = smtplib.SMTP('localhost')
            server.sendmail(FROM, TO,  message)
            server.quit()

if __name__ == "__main__":
        main('xxx', 'xxx', 'xx')