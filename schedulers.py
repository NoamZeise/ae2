import math

from des import SchedulerDES
from event import Event, EventTypes
from process import ProcessStates

class FCFS(SchedulerDES):
    def scheduler_func(self, cur_event):
        self.processes[cur_event.process_id].process_state = ProcessStates.READY
        return self.processes[cur_event.process_id]

    def dispatcher_func(self, cur_process):
        cur_process.process_state = ProcessStates.RUNNING
        time = cur_process.run_for(cur_process.remaining_time, self.time)
        cur_process.process_state = ProcessStates.TERMINATED
        return Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_DONE, event_time=time)
        


class SJF(SchedulerDES):
    def scheduler_func(self, cur_event):
        pass

    def dispatcher_func(self, cur_process):
        pass


class RR(SchedulerDES):
    def scheduler_func(self, cur_event):
        pass

    def dispatcher_func(self, cur_process):
        pass


class SRTF(SchedulerDES):
    def scheduler_func(self, cur_event):
        pass

    def dispatcher_func(self, cur_process):
        pass
