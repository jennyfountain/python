#!/usr/bin/python

import redis
import xmlrpclib
import pystache
import socket

def get_redis_info():
        filename = "redis.txt"
        myservers = []
        all_redis_data = []
        with open(filename) as f:
            for line in f:
                myservers.append([n for n in line.strip().split(':')])
        for pair in myservers:
            try:
                host, port, project = pair[0], pair[1], pair[2]
                r = redis.StrictRedis(host=host, port=port)
                info = r.info()
                slave_info = []
                db_info = []
                r_info = dict()
                r_info['host'] = host
                r_info['project'] = project
                r_info['link'] = "http://servers.scs.myyearbook.com/index.php?page=search&type=hostname&searchterm="
                r_info['version'] = info['redis_version']
                r_info['config_file'] = info['config_file']
                r_info['tcp_port'] = info['tcp_port']
                r_info['memory'] = info['used_memory_human']
                r_info['server_role'] = info['role']
                if r_info['server_role'] != 'master':
                    r_info['master_host'] = info['master_host']
                    r_info['master_port'] = info['master_port']
                    r_info['connected_slaves'] = info['connected_slaves']
                if r_info['server_role'] != 'slave':
                    for item in info.items():
                        if 'slave' in item[0] and 'connected_slaves' not in item[0]:
                            r_info[item[0]+'_ip'] = socket.getfqdn(info[item[0]]['ip'])
                            r_info[item[0]+'_port'] = info[item[0]]['port']
                            slave_name = socket.getfqdn(info[item[0]]['ip'])
                            slave_info.append(slave_name+':'+str(info[item[0]]['port']))
                    r_info['slave_servers'] = str(slave_info).strip('[]')

                for database in info.items():
                    if 'db' in database[0] and 'rdb' not in database[0]:
                        dbstuff = str(database[0])
                        r_info['database_info'] = db_info.append([dbstuff])
                        r_info['database_info'] = str(db_info)
                all_redis_data.append(r_info)
            except IndexError:
                    print "Someone doesn't have a project!"

        return all_redis_data

if __name__ == '__main__':
    data = get_redis_info()

    USERNAME = 'xxx'
    PASSWORD = 'xxxx'

    template = 'redis_discovery.mustache'

    BASE = 'xxxx'
    SPACE = 'xxx'
    PAGE = 'Redis Server General Information'

    server = xmlrpclib.ServerProxy(BASE)
    token = server.confluence2.login(USERNAME, PASSWORD)
    page = server.confluence2.getPage(token, SPACE, PAGE)

    renderer = pystache.Renderer()
    output = renderer.render_path(template, {'redis': data})

    page['content'] = output
    server.confluence2.storePage(token, page)
