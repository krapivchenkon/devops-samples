# Sample of simple AWS provisioning with ansible playbooks

## Description:
This sample shows how ec2 instance can be started with ansible ec2 module and fully managed by ansible playbooks

### Features
- Uses ubuntu/trusty ami instance
- env can be restored easily on aws and localy with the same ansible playbooks
- Uses EC2 Dynamic inventory scripts

### Prerequisites
- You'll need `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` envronment variables set up.
- Installed `vagrant` if you want to use vagrant to spin off machines

## Setup
- First we need to prepare tools for running scripts:
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

- Add ssh inbound rule to security group configuration (`TODO:` should be done by ec2_groups module)
- Start instances
    ```
    $ ansible-playbook -vvv sample_playbook.yml -i ec2.py
    ```

- Stop instances (`TODO: ` add task to playbook)
- Restart instances (`TODO: ` add task to playbook)

## Checking environment
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

