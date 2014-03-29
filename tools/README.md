Deploying orchester
===================

Requirements
------------

### Deployment target

For both node and master, you need a sshable box with the following:

- A user 'orchester' with a homedir in /home/orchester
- A group 'supervisor' (orchester must be member of this group)
- Supervisord properly configured to allow supervisor group membres to use
  supervisorctl (chown root:supervisor and chmod 770 on /var/run/supervisor.sock)
- Mongodb installed and running

You must also have 2 symlinks (no need to create a valid directory structure,
deploy scripts will take care of it) for orchester config:

 - `ln -fs /home/orchester/orchester.io/orchester-master/current/etc/orchester-master/supervisor.conf /etc/supervisor/conf.d/orchester-master.conf`
 - `ln -fs /home/orchester/orchester.io/orchester-node/current/etc/orchester-node/supervisor.conf /etc/supervisor/conf.d/orchester-node.conf`


### Client host

You must install the following python packages on your local host:

 - `pip install fabric`
 - `pip install fabtools`

Or simpler:

`pip install -r requirements.txt`


Deployment
----------

Fabric usage in our case is the following:

`fab -H <host> -i <ssh_key> <module>.<command>:<environment>`

With:

- `<host>`: The target host
- `<ssh_key>`: Path to an allowed private key for the user 'orchester' on <host>
- `<module>`: The module to deploy ('master' or 'node')
- `<environment>`: The environment to use ('staging' or 'prod')
- `<command>`: See below


### Deploying the master

You first need to setup the directory structure, virtualenvs and stuff:

`fab -H <host> -i <ssh_key> master.setup:staging`

Then you may deploy with

`fab -H <host> -i <ssh_key> master.deploy:staging`


### Deploying the node

Same shit here.

You first need to setup the directory structure, virtualenvs and stuff:

`fab -H <host> -i <ssh_key> node.setup:staging`

Then you may deploy with

`fab -H <host> -i <ssh_key> node.deploy:staging`


Release management
------------------

It is possible to revert to a previous deployment with the rollback command.

`fab -H <host> -i <ssh_key> master.rollback:<release>`

`<release>` is optional and may specify the release id you want to rollback


You can list releases and their metadata with:

`fab -H <host> -i <ssh_key>  master.releases`


Next features
-------------

- Deploying all the infrastructure with only one command:
  `fab deploy:staging`

- Resetting an initial database state with all configured:
  `fab resetdb:staging`

- Deploying more stuf and deploying deploy tools so you can deploy your
  deploy deployed deploy while you deploy
