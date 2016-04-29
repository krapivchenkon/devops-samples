# Sample of simple AWS provisioning with ansible playbooks

## Description:
This sample shows how ec2 instances can be fully managed with ansible playbooks

### Features
- Uses ubuntu/trusty64 ami instance
- Contains playbooks for:
	- Launching instances (`--tags start`)
	- `TODO:` Stopping instances (`--tags stop`)
	- `TODO:` Terminating instances (`--tags term`)
	- `TODO:` Restarting instances (`--tags restart`)
	- `TODO:` Simple health check tasks (`--tags check`)
- `TODO:` Uses EC2 Dynamic inventory scripts to create static **hosts_ec2** file
- `TODO:` On starting instance ssh and icmp rules are configured in default security group
- `TODO:` SSH key-pair created automatically on startup
- `TODO:` Playbooks are using ec2_remote_facts with tag filters to add existing hosts to **ec2hosts** group.
	- when running start/stop/term/restart instances host group created from the values returned by **ec2_remote_facts**

### Configuration assumptions
- all instances are created in default **security group**.
- [group_vars/ec2.yml](group_vars/ec2.yml) contains following configurations:
	- `TODO:` Tag name that will be assigned to ec2 instances
- [group_vars/all.yml](group_vars/all.yml) contains following configurations:
	- `TODO:` Default zone in `aws_default_region`
### Prerequisites
- You'll need `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables set up.
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
    # eu-west-1 is Ireland
    $ export AWS_DEFAULT_REGION=eu-west-1
    ```

- Generate ssh key and exchange it with server (`TODO:` should be part of ansible playbook)
    ```
    ssh-keygen -t rsa -b 4096 -C "youremail@example.com" -f ./id_rsa && chmod 600 id_rsa.pub
    aws ec2 import-key-pair --key-name ec2demo --public-key-material file://./id_rsa.pub
    ```

- Add dynamic inventory scripts using ansible(`ec2.py` and `ec2.ini`) (`TODO:`should be part of playbook)
    ```
    ansible-playbook -vvv sample_playbook.yml -i hosts
    ```

- `TODO:` Add ssh inbound rule to security group configuration (should be done by ec2_groups module)
- Start instances
    ```
    $ ansible-playbook -vvv sample_playbook.yml -i ec2.py
    ```

- Stop instances (`TODO: ` add task to playbook)
- Restart instances (`TODO: ` add task to playbook)

## Checking environment
- Get list of instances usings `ec2.py`:
    ```
    $ ./ec2.py --list
    {
      "_meta": {
        "hostvars": {}
        }
    }
    # to refresh cache run:
    $ ./ec2.py --refresh-cache
    ```

- Connect to instances via ssh:
    ```
    $ssh -i ./id_rsa ubuntu@ec2-xx-xxx-xx-xxx.eu-west-1.compute.amazonaws.com
    ```

- Ping hosts with dynamic inventory scripts
    ```
    $ ansible -vvv -i ec2.py -u ubuntu eu-west-1 -m ping --key-file=./id_rsa
    $ ansible-playbook  -vvv sample_playbook.yml -i ec2.py --key-file=id_rsa
    ```

## Configuration
- Dynamic inventory cache configuration

    EC2 inventory cache time can be configured in [ec2.ini](https://raw.githubusercontent.com/ansible/ansible/devel/contrib/inventory/ec2.ini) file:
  ```
  # The number of seconds a cache file is considered valid. After this many
  # seconds, a new API call will be made, and the cache file will be updated.
  # To disable the cache, set this value to 0
  cache_max_age = 300
  ```
 
- If you are running `virtualenv` path to python should be set in group vars [group_vars/all.yml](group_vars/all.yml):
    ```
    ansible_python_interpreter: "{{ lookup('env','PWD') }}/venv/bin/python"
    ```

## Links
- [Ansible ec2 module docs](http://docs.ansible.com/ansible/ec2_module.html#this-is-a-core-module)