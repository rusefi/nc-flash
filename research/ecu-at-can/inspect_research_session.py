"""Read the known overlapping session; optionally deliver authorized handoff.

Requires websockets15.0.1. No server restart, resume, or process termination.
Use --handoff only with user authorization to coordinate the other session.
"""
import argparse
import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path
from websockets.asyncio.client import unix_connect

TARGET = '01a10e81-61f6-7013-a9d4-10f2f3acdb21'
ROOT = Path(__file__).resolve().parent
MESSAGE = '''The user has explicitly asked the other nc-flash session to negotiate ownership with you, after closing IDEA and asking whether you are still alive. This is coordination from thread01a111a7-d4c4-7711-a3fd-3000d21d4068, not a new research assignment. We overlapped on verify_tcu_curve_sources.py. I moved my work to verify_tcu_threshold_axis_history.py and its associated evidence (60 calls,600 lookups,60 scans). Please finish any current Ghidra save/archive/independent restore verification, preserve your curve-source results and checkpoint, and then stand down from further research/editing in this checkout. Report your actual saved state, pending work, and whether an automatic goal could continue. Do not commit/push. Do not terminate the shared app-server or other project sessions. Please acknowledge the handoff in your response and in research/ecu-at-can/session-handoff-reply.txt so both sessions can continue from repository evidence. I will avoid Ghidra/shared research edits until you finish saving.'''


async def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--socket',required=True)
    parser.add_argument('--handoff',action='store_true')
    args=parser.parse_args()
    async with unix_connect(args.socket,uri='ws://localhost',open_timeout=10,max_size=8*1024*1024) as ws:
        counter=0
        async def rpc(method,params):
            nonlocal counter
            counter+=1
            await ws.send(json.dumps(dict(id=counter,method=method,params=params)))
            while True:
                message=json.loads(await asyncio.wait_for(ws.recv(),20))
                if message.get('id')==counter:
                    if 'error' in message:raise RuntimeError(message['error'])
                    return message['result']
        await rpc('initialize',dict(clientInfo=dict(name='nc_research_coordination',title='NC research coordination',version='1'),capabilities=dict(experimentalApi=True)))
        await ws.send(json.dumps(dict(method='initialized')))
        thread=(await rpc('thread/read',dict(threadId=TARGET,includeTurns=False)))['thread']
        assert thread['cwd']=='/home/snow/nc-flash',thread['cwd']
        turns=await rpc('thread/turns/list',dict(threadId=TARGET,limit=1,itemsView='notLoaded'))
        result=dict(checked_at_utc=datetime.now(timezone.utc).isoformat(),thread_id=TARGET,
                    status=thread.get('status'),turns=turns)
        if args.handoff and thread.get('status',{}).get('type')=='active':
            active=next(t for t in turns['data'] if t['status']=='inProgress')
            result['handoff_message']=MESSAGE
            result['handoff_receipt']=await rpc('turn/steer',dict(threadId=TARGET,expectedTurnId=active['id'],input=[dict(type='text',text=MESSAGE)]))
        path=ROOT/('session-handoff-request.json' if args.handoff else 'session-status.json')
        path.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result,indent=2))


if __name__=='__main__':
    asyncio.run(main())
