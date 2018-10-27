import boto.ec2
conn = boto.ec2.connect_to_region("us-east-1", aws_access_key_id:<access_key>,aws_secret_access_key:<secret_key>)
keyPair = conn.create_key_pair(<key_name>)
keyPair.save("")
group = conn.create_security_group("csc326-group9","Group 9")
group.authorize("icmp", -1, -1, "0.0.0.0/0")
group.authorize("tcp", 22, 22, "0.0.0.0/0")
group.authorize("tcp", 80, 80, "0.0.0.0/0")
resp = conn.run_instances("ami-9aaa1cf2", instance_type="t2.micro", key_name=<key_name>, security_groups=[group])

