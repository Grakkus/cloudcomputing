import boto3

ec2 = boto3.resource('ec2', region_name='us-east-1')

filters = [
  {
    'Name': 'instance-state-name',
    'Values': ['pending', 'running']
  }
]
instances = ec2.instances.filter(Filters=filters)

for instance in instances:
    instance.terminate()
    print("Terminated instance " + str(instance.id))
