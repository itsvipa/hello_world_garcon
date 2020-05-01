Python package for helper cli scripts

Currently only one lonely command, `garcon-activity-local`

## garcon-activity-local

The `garcon-activity-local` command's purpose is to make it easy to analyze and run a garcon workflow's activities in one's local dev environment, without going through the hassle of setting up deciders/workers, waiting for SWF, etc.

### Install
```
pip install -e "git+ssh://git@github.com/theorchard/garcon-contrib.git#egg=contrib_cli&subdirectory=contrib-cli"
```
(don't forget the quotes when running from the commandline or you will be sad)

### Usage
```
usage: garcon-activity-local [-h] [-i] [-d] flow {list,run} ...

Garcon local activity util

positional arguments:
  flow         flow module [make sure it is in class path]
  {list,run}   local garcon command
    list       list activities
    run        run activity

optional arguments:
  -h, --help   show this help message and exit
  -c FLOW_CLASS, --class FLOW_CLASS
                        Name of the Flow class
  -i, --info   set logging to info
  -d, --debug  set logging to debug
```

### Examples

Assuming we checkout this module.....

#### Garcon Flow as a Class

List activities in a workflow
```
export PYTHONPATH=.
 garcon-activity-local  tests.fixtures.flow_object -c FlowObject list
>> Activity names include:
workflow_sample_bootstrap2
workflow_sample_bootstrap
workflow_sample_activity_1
workflow_sample_activity_2
workflow_sample_activity_3
```

Execute an activity in the workflow
```
export PYTHONPATH=.
cd tests
garcon-activity-local -i tests.fixtures.flow_object -c FlowObject run workflow_sample_activity_3
>> INFO:fixtures.flow_cli:activity_3
>> Context Result: {}
```

Execute an activity in the workflow with a passed context
```
export PYTHONPATH=.
cd tests
garcon-activity-local -i tests.fixtures.flow_object -c FlowObject run workflow_sample_bootstrap2 -c '{"context_test":"passing a context"}'
>> INFO:fixtures.flow_cli:bootstrap
>> INFO:fixtures.flow_cli:context_test: passing a context
>> Context Result: {'new_context': "I'm the new context"}
```


#### Garcon Flow as a Module

List activities in a workflow
```
export PYTHONPATH=.
cd tests
garcon-activity-local fixtures.flow_cli list
>> Activity names include ['workflow_sample_bootstrap', 'workflow_sample_bootstrap2', 'workflow_sample_activity_1', 'workflow_sample_activity_2', 'workflow_sample_activity_3']
```

Execute an activity in the workflow
```
export PYTHONPATH=.
cd tests
garcon-activity-local -i fixtures.flow_cli run workflow_sample_activity_3
>> INFO:fixtures.flow_cli:activity_3
>> Context Result: {}
```

Execute an activity in the workflow with a passed context
```
export PYTHONPATH=.
cd tests
garcon-activity-local -i fixtures.flow_cli run workflow_sample_bootstrap2 -c '{"context_test":"passing a context"}'
>> INFO:fixtures.flow_cli:bootstrap
>> INFO:fixtures.flow_cli:context_test: passing a context
>> Context Result: {'new_context': "I'm the new context"}
```
