#!/usr/bin/python
import boto.ec2
import sys

AWS_ACCESS_KEY_ID = 'xxx'
AWS_SECRET_ACCESS_KEY = 'xxxx'
REGION = sys.argv[2]

box = sys.argv[3]

exclude_list = []
for exclude in sys.argv[3:]:
    exclude_list.append(exclude)

conn = boto.ec2.connect_to_region(REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

ec2_servers = conn.get_all_instances()
ec2_server = conn.get_all_instances(instance_ids=[box])

def stop():
    try:
        for r in ec2_servers:
            for i in r.instances:
                if i.state == 'running' and not i.id in exclude_list:
                    print 'Stopping', i
                    i.stop()
                else:
                    print i, 'is in the the excluded list or is already stopped.'
    except Exception, e:
        print e


def start():
    try:
        if ec2_server[0].instances[0].state == 'running':
            print ec2_server[0].instances[0], 'is already running'
        else:
            ec2_server[0].instances[0].start()
            print 'Starting', ec2_server[0].instances[0]
    except Exception, e:
        print e

if __name__ == '__main__':
    globals()[sys.argv[1]]()