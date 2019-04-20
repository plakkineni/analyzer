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
def cli():
  """ Volumes & Instances """

@cli.group('volumes')
def volumes():
 """Commands for volumes"""

@cli.group('instances')
def cinstances():
  """Commands for instances"""

@cli.group('snap')
def snap():
  """ COmmands for snaps"""

@snap.command('create')
@click.option('--project',default='none',help='Enter Project Tag Name')
def createsnap(project):
 "Snap the volumes of the project"
 instances=filter_instances(project)

 for ec in instances:
  ec.stop()
  ec.wait_until_stopped()
  for vol in ec.volumes.all():
    print("Creating snapshot of volume {0} Instance: {1}.....".format(vol.id,ec.id))
    vol.create_snapshot()
    print(" Starting Instance {0}.....".format(ec.id))
    ec.start()
    ec.wait_until_running()

 return


@snap.command('delete')
@click.option('--project',default='none',help='Enter Project Tag Name')
def deletesnap(project):
 "Delete the snaps of volumes"
 instances=filter_instances(project)

 for ec in instances:
  for vol in ec.volumes.all():
   for snap in vol.snapshots.all():
     print("Deleting snapshot {0}.....".format(snap.snapshot_id))
     snap.delete()

 return



@snap.command('list')
@click.option('--project',default='none',help='Enter Project Tag Name')
def deletesnap(project):
 "List the snaps of volumes"
 instances=filter_instances(project)

 for ec in instances:
  for vol in ec.volumes.all():
   for snap in vol.snapshots.all():
    print(' : '.join((snap.snapshot_id,snap.volume_id,ec.id)))

 return


@volumes.command('volumes')
@click.option('--project',default='none',help='Enter Project Tag Name')
def listvolumes(project):
 "List Volumes for the associated Instances"
 instances=filter_instances(project)

 for ec in instances:
  for vol in ec.volumes.all():
    print(':'.join((vol.id,vol.state,vol.volume_type))) 

 return 

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
 cli()
