import time

from garcon import decider

import flow


hello_world_flow = flow.HelloWorldFlow('dev', '1.0')
decider_worker = decider.DeciderWorker(hello_world_flow)
while(True):
    decider_worker.run()
    time.sleep(1)
