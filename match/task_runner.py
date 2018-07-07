import sched, time
import match.scores

s = sched.scheduler(time.time, time.sleep)

def run_task(sc): 
    print ("Doing stuff...")
    match.scores.store_data()
    s.enter(10, 1, run_task, (sc,))

s.enter(10, 1, run_task, (s,))

s.run()
