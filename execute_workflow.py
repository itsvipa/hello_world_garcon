import json

import boto.swf.layer2 as swf

import flow

initial_context = dict(foo='bar')
hello_world_flow = flow.Flow('dev', '1.0')
workflow_execution = swf.WorkflowType(
        name=hello_world_flow.name,
        domain=hello_world_flow.domain,
        version=hello_world_flow.version,
        task_list=hello_world_flow.name).start(
            input=json.dumps(initial_context))

print("Launching SWF for flow '{}' with WorkflowId '{}' and RunId '{}'".format(
    workflow_execution.name,
    workflow_execution.workflowId,
    workflow_execution.runId))
