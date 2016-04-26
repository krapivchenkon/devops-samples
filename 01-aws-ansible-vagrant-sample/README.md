# Provisioning with vagrant to AWS and ansible playbooks


## Description:
This sample shows how ec2 instance can be started with ansible ec2 module and fully managed by ansible playbooks

### Features
    - Uses ubuntu/trusty ami instance
    - env can be restored easily on aws and localy with the same ansible playbooks
    - \#TODO fully automated instance start - all keys created and SG rules are added from ansible scripts
    - \#TODO shows sample of using ec2 dynamic inventory
    - \#TODO use `vagrant` to start both local and ec2 instances
    - \#TODO ec2 dynamic inventory scripts downloaded by playbook
    


### Prerequisites
- You'll need AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY envronment variables set up.
- installed `vagrant` if you want to use vagrant to spin off machines




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

# TODO should be part of ansible playbook
ssh-keygen -t rsa -b 4096 -C "youremail@example.com" -f ./id_rsa && chmod 600 id_rsa.pub
# TODO should be part of ansible playbook
aws ec2 import-key-pair --key-name ec2demo --public-key-material file://./id_rsa.pub

ansible-playbook -vvv sample_playbook.yml -i hosts

add ssh rule to SG configuration

\#TODO add dynamic inventory scripts using ansible

ssh -i ./id_rsa ubuntu@ec2-54-229-90-177.eu-west-1.compute.amazonaws.com


# ping hosts with dynamic inventory scripts
ansible -vvv -i ec2.py -u ubuntu eu-west-1 -m ping --key-file=./id_rsa

\#TODO use ssh key from group vars

ansible-playbook  -vvv sample_playbook.yml -i ec2.py --key-file=id_rsa
\#TODO dynamic inventory caching

\#TODO using results of inventory script

\#TODO setup zone vars to group_vars variables


## Open Questions and TODOs
 - What is local action
 - ansible + aws only
     - start/stop ec2 instance with ansible
     - ping 
     - sample of running status check playbooks hostname.yml playbook
     - restart same instances without creating new

 - \#TODO adding vagrant
 - vagrant file contains vars from env
 - 


\#TODO check the case when ec2_facts returns multiplie instances



## Links
- Ansible ec2 module
http://docs.ansible.com/ansible/ec2_module.html#this-is-a-core-module

