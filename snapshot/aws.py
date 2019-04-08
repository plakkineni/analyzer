import boto3


if '__name__' == '__main__':
 isession=boto3.Session(profile_name='shotty')
 ec2 = session.resource('ec2')

 for ec in ec2.instances.all():
  print(ec) 
