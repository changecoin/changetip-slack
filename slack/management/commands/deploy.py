from boto.opsworks.layer1 import OpsWorksConnection
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import getpass
import json
import os
import subprocess
import socket


def console_call(command):
    try:
        return subprocess.check_output(command).replace("\n", "")
    except:
        return None


def get_git_user():
    return console_call(["git", "config", "user.email"])


def get_git_branch():
    return console_call(["git", "rev-parse", "--abbrev-ref", "HEAD"])


def get_git_commit():
    return console_call(["git", "rev-parse", "HEAD"])

def get_json():
    params = {}
    params['github-user'] = os.environ.get('CIRCLE_USERNAME', get_git_user())
    params['git-branch'] = os.environ.get('CIRCLE_BRANCH', get_git_branch())
    params['git-commit'] = os.environ.get('CIRCLE_SHA1', get_git_commit())
    return params


class Command(BaseCommand):
    help = 'Trigger a deployment in AWS OpsWorks'

    option_list = BaseCommand.option_list + (
        make_option('--env',
                    action='store',
                    dest='environment',
                    default='production',
                    help='The environment suffix of the stack to deploy to (e.g. "development", "staging", "production")'),
    )

    def handle(self, *args, **options):
        opsworks = OpsWorksConnection()
        stack_resp = opsworks.describe_stacks()
        stack_id = None
        stack_name = None

        for stack in stack_resp['Stacks']:
            if stack['Name'].startswith('web') and stack['Name'].endswith(options['environment']):
                stack_id = stack['StackId']
                stack_name = stack['Name']
                break
        if not stack_id:
            raise CommandError('Stack does not exist.' % options['environment'])

        # get application
        app_resp = opsworks.describe_apps(stack_id=stack_id)
        app_id = app_resp['Apps'][0]['AppId']
        app_name = app_resp['Apps'][0]['Name']

        # get layer
        for layers in opsworks.describe_layers(stack_id=stack_id)['Layers']:
            if layers['Name'] == 'bots':

                # deploy to the instances of particular layer
                for instance in opsworks.describe_instances(layer_id=layers['LayerId'])['Instances']:
                    custom_json = json.dumps(get_json())
                    comment = "Deploying %s from %s@%s at %s to %s on %s" % (
                        app_name,
                        getpass.getuser(),
                        socket.gethostname(),
                        datetime.now().isoformat(' '),
                        instance['Hostname'],
                        stack_name)

                    deployment = opsworks.create_deployment(stack_id, {'Name': 'deploy'}, app_id=app_id,
                        instance_ids=[instance['InstanceId']], custom_json=custom_json, comment=comment)

                    print "https://console.aws.amazon.com/opsworks/home?#/stack/%s/deployments/%s" % (stack_id, deployment['DeploymentId'])
