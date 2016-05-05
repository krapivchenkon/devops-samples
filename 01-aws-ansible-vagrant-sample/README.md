# Sample of simple AWS provisioning with ansible playbooks

## Description:
This sample shows how ec2 instances can be fully managed with ansible playbooks

### Features
- Uses ubuntu/trusty64 ami instance
- Contains playbooks for:
	- Launching instances (`--tags start`)
	- Stopping instances (`--tags stop`)
	- Terminating instances (`--tags term` or `--tags term_stopped`)
	- Simple health check tasks (`--tags check`)
	- Check status on current ec2 instances(`--tags status`)
- `TODO:` Uses EC2 Dynamic inventory scripts to create static **hosts_ec2** file
- Setup inbound ACL rules and ssh keys(`--tags setup`):
	- SSH and icmp rules are configured in default security group
	- SSH key-pair created automatically by **ec2_keys** module
- Playbooks are using **ec2_remote_facts** module with tag filters to add existing hosts to **ec2** group.
	- when running start/stop/term/restart instances host group created from the values returned by **ec2_remote_facts**


### Configuration assumptions
- all instances are created in default **security group**.
- [group_vars/all.yml](group_vars/all.yml) contains following configurations:
	- Default zone in `aws_default_region`
	- Path to ssh_private_key
	- Tag name that will be assigned to ec2 instances
### Prerequisites
- You'll need `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables set up.
- `virtualenv` and `pip` installed
- `TODO:` Installed `vagrant` if you want to use vagrant to spin off machines

## Setup
- First we need to prepare tools for running scripts. We will need `ansible, boto, awscli` python libs
    ```
    $ virtualenv --prompt "aws-demo-" venv
    $ . venv/bin/activate
    $ pip install -r requirements.txt
    ```

- Now we need to setup your aws user credentials:
    ```
    $ export AWS_ACCESS_KEY_ID='YOUR-KEY-ID'
    $ export AWS_SECRET_ACCESS_KEY='YOUR-SECRET-KEY'
    ```

-  Setup ssh key and inbound security rules
    ```
    $ ansible-playbook  sample_playbook.yml --tags setup
    ```

- **Start instances**
    ```
    $ ansible-playbook  sample_playbook.yml --tags start
    ```
	> Startup logic works in a way described below. Assume that:  
	> **all_inst** - number of instances that should be in running state  
	> **stop_inst** - number of currently stopped instances of the same type(from **ec2_remote_facts**)  
	> **run_inst** -  - number of currently running instances of the same type(from **ec2_remote_facts**)  
	>
 
	```python
	if run_inst < all_inst:
		startInstances(all_inst-run_inst)

	following command will ensure that we are running correct number of instances
	this is the case when there are not enough stopped instances (all_inst>(run_inst+stop_inst)):

	run_ec2_task_with_exact_count(all_inst)
	```   
	
- **Stop instances**   
	Following will stop all running instances
    ```
    $ ansible-playbook  sample_playbook.yml --tags stop
    ```

- **Terminate instances**   
	Following will terminate all instances with specific tag
    ```
    $ ansible-playbook  sample_playbook.yml --tags term
    ```
	Following will terminate only stopped instances with specific tag
    ```
    $ ansible-playbook  sample_playbook.yml --tags term_stopped
    ```



## Checking environment
- Run health checks on ec2 host group
	```
	$ ansible-playbook  sample_playbook.yml --tags check
	$ ansible-playbook  sample_playbook.yml --tags status
	```

- Connect to instance via ssh:   
	`TODO:` script wrapper to easy connect to required instance
    ```
    $ssh -i ./id_rsa ubuntu@ec2-xx-xxx-xx-xxx.eu-west-1.compute.amazonaws.com
    ```

## Configuration
 
- If you are running `virtualenv` path to python should be set in group vars [group_vars/all.yml](group_vars/all.yml):
    ```
    ansible_python_interpreter: "{{ lookup('env','PWD') }}/venv/bin/python"
    ```

## Links
- [Ansible ec2 module docs](http://docs.ansible.com/ansible/ec2_module.html#this-is-a-core-module)