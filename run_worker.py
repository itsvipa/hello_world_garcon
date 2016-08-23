from garcon import activity

import flow


hello_world_flow = flow.HelloWorldFlow('dev', '1.0')
worker = activity.ActivityWorker(hello_world_flow)
worker.run()
