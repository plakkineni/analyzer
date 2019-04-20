import boto3
import click

session=boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

def filter_instances(project): 

 instances=[]
 instances=ec2.instances.all()
 filter=[{'Name':'tag:Project', 'Values':[project]}]

 if not project == 'none':
  instances=ec2.instances.filter(Filters=filter)
 else:
  "List EC2 Instances"
  instances=ec2.instances.all()

 return instances


@click.group()
def cinstances():
  """Commands for instances"""


@cinstances.command('list')
@click.option('--project',default='none',help='Enter Project Tag name')
def listinstances(project):
 "List Instances for the Project"
 instances=filter_instances(project)
 
 for ec in instances:
  tags = { t['Key']: t['Value'] for t in ec.tags or [] }
  print(','.join((ec.id,ec.instance_type,ec.state['Name'],ec.public_dns_name,tags.get('Project','<no project>'))))  

 return

@cinstances.command('stop')
@click.option('--project',default='none',help='To stop Instances')
def stopinstances(project):
 "Stop EC2 instances" 
 instances=filter_instances(project)

 for ec in instances:
  print("Stopping {0}.....".format(ec.id)) 
  ec.stop()

 return

@cinstances.command('start')
@click.option('--project',default='none',help='To start Instances')
def startinstances(project):
 "Start EC2 instances"
 instances=filter_instances(project)

 for ec in instances:
  print("Starting {0}.....".format(ec.id))
  ec.start()

 return

if __name__ == '__main__':
 cinstances()
