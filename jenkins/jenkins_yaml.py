import yaml
import boto.ec2
import sys
import json

AWS_ACCESS_KEY_ID = 'xxxx'
AWS_SECRET_ACCESS_KEY = 'xxxxx'

fname = sys.argv[1]
REGION = sys.argv[2]

stream = open(fname, 'r')
data = yaml.load(stream)

conn = boto.ec2.connect_to_region(REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
ec2_servers = conn.get_all_instances()
ec2_nodes = []

for r in ec2_servers:
            for i in r.instances:
                if i.state == 'running':
                    ec2_nodes.append(i.tags['Name'])


data[1]['job']['parameters'][0]['xx']['xx'] = ec2_nodes

with open(fname, 'w') as yaml_file:
    yaml_file.write(yaml.dump(data, default_flow_style=False))