import math

from des import SchedulerDES
from event import Event, EventTypes
from process import ProcessStates

def get_shortest_event(self, cur_event):
    max_priority = cur_event
    for i in range(len(self.events_queue)):
        if self.events_queue[i].event_time > self.time:
            break
        if self.processes[self.events_queue[i].process_id].remaining_time < self.processes[max_priority.process_id].remaining_time:
            temp = max_priority
            max_priority = self.events_queue[i]
            self.events_queue[i] = temp
    self.processes[max_priority.process_id].process_state = ProcessStates.READY
    return max_priority

def non_pre_emptive_dispatcher(self, cur_process):
    cur_process.process_state = ProcessStates.RUNNING
    time = cur_process.run_for(cur_process.remaining_time, self.time) + self.time
    cur_process.process_state = ProcessStates.TERMINATED
    return Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_DONE, event_time=time)

class FCFS(SchedulerDES):
    def scheduler_func(self, cur_event):
        self.processes[cur_event.process_id].process_state = ProcessStates.READY
        return self.processes[cur_event.process_id]

    def dispatcher_func(self, cur_process):
        return non_pre_emptive_dispatcher(self, cur_process)

class SJF(SchedulerDES):
    def scheduler_func(self, cur_event):
        return self.processes[get_shortest_event(self, cur_event).process_id]

    def dispatcher_func(self, cur_process):
        return non_pre_emptive_dispatcher(self, cur_process)

class RR(SchedulerDES):
    def scheduler_func(self, cur_event):
        self.processes[cur_event.process_id].process_state = ProcessStates.READY
        return self.processes[cur_event.process_id]

    def dispatcher_func(self, cur_process):
        cur_process.process_state = ProcessStates.RUNNING
        time = cur_process.run_for(self.quantum, self.time) + self.time
        if cur_process.remaining_time <= 0:
            cur_process.process_state = ProcessStates.TERMINATED
            return Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_DONE, event_time=time)
        else:
            cur_process.process_state = ProcessStates.NEW
            return Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_REQ, event_time=time)


class SRTF(SchedulerDES):
    def scheduler_func(self, cur_event):
        return self.processes[get_shortest_event(self, cur_event).process_id]

    def dispatcher_func(self, cur_process):
        cur_process.process_state = ProcessStates.RUNNING
        run_time = cur_process.remaining_time
        if self.next_event_time() - self.time < cur_process.remaining_time:
            run_time = self.next_event_time() - self.time
        time = cur_process.run_for(run_time, self.time) + self.time
        if cur_process.remaining_time <= 0:
            cur_process.process_state = ProcessStates.TERMINATED
            return Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_DONE, event_time=time)
        else:
            cur_process.process_state = ProcessStates.NEW
            return Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_REQ, event_time=time)
