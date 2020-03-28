import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2', verify=False)


@click.group()
def instances():
    """Commands for instances"""


@instances.command('list')
@click.option('--project', default=None, help="Only instances for project (tag project:<name>)")
def list_instances(project):
    "List EC2 instances"

    ec2_instances = get_ec2_instances(project)

    for i in ec2_instances:
        tags = {t['Key']: t['Value'] for t in i.tags or []}
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('project', '<no project>')
        )))
    return

@instances.command('stop')
@click.option('--project', default=None, help='Only instances for project')
def stop_instances(project):
    "Stop EC2 instances"

    ec2_instances = get_ec2_instances(project)

    for i in ec2_instances:
        print("Stopping {0}...".format(i.id))
        i.stop()

    return

@instances.command('start')
@click.option('--project', default=None, help='Only instances for project')
def start_instances(project):
    "Start EC2 instances"

    ec2_instances = get_ec2_instances(project)

    for i in ec2_instances:
        print("Starting {0}...".format(i.id))
        i.start()

    return

def get_ec2_instances(project):
    if project:
        filters = [{'Name': 'tag:project', 'Values': [project]}]
        return ec2.instances.filter(Filters=filters)
    else:
        return ec2.instances.all()

if __name__ == '__main__':
    instances()
