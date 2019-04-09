import boto3
import click

session=boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

@click.command()
def listinstances():
 "List EC2 Instances"
 for ec in ec2.instances.all():
  print(','.join((ec.id,ec.instance_type,ec.state['Name'],ec.public_dns_name)))  

 return

if __name__ == '__main__':
  listinstances()
