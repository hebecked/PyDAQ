import multiprocessing



class DAQ(multiprocessing.Process):

#que for taken data, for progresbar and termination
#needs ports , instruction file
#output file//handle by data_io
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.interrupt signal = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill means shutdown
                print '%s: Exiting' % proc_name
                self.task_queue.task_done()
                break
            print '%s: %s' % (proc_name, next_task)
            answer = next_task()
            self.task_queue.task_done()
            self.result_queue.put(answer)
        return	
