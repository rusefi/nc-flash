"""Twenty explicit index7/priority3 requests through original enqueue/dispatch.

38C4 initializes queues,391A enqueues eachrequest,3B8A selects anddispatches;
3CB8 consumes the request and idle3D0C ends each observed cycle. Requests have
no physical cadence. ADC result samples do not simulate conversion completion.
"""
from probe_control_task_dispatch import main

if __name__=='__main__':
    main(queued=True,cycles=20,filename='control-queued-acquisition-probe.json')
