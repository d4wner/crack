#coding=utf-8


import threading
import Queue

from billiard.dummy import DummyProcess

#class work(DummyProcess):
class work(DummyProcess):
    def __init__(self, workQueue, result_queue, timeout=5, **kwargs):
        self.timeout = timeout
        self.result_queue = result_queue
        self.isRunning = False
        self.workQueue = workQueue
        DummyProcess.__init__(self, kwargs=kwargs)
#        self.daemon = True

    def stop(self):
        self.isRunning = False

    def run(self):
        self.isRunning = True
        while self.isRunning:
            try:
                func, args, kwargs = self.workQueue.get(timeout=self.timeout)
                result = apply(func, *args, **kwargs)
                self.workQueue.task_done()
                self.result_queue.put(result, False)
            except Queue.Empty:
                self.isRunning = False
            except:
                pass

class ThreadPool:
    def __init__(self, num_of_threads=10):
        self.workQueue = Queue.Queue()
        self.result_queue = Queue.Queue()
        self.threads = []

        for i in range(num_of_threads):
            thread = work(self.workQueue, self.result_queue)
            self.threads.append(thread)

    def add_job(self, fun, *args, **kwargs):
        self.workQueue.put((fun, args, kwargs))
    
    def get_result(self):
        results = []
        try:
            while True:
                result = self.result_queue.get(block=False)
                #print result
                results.append(result)
        except Exception,e:
            #print str(e)
            pass
        finally:
            #print results
            #print "@@@@@"
            return results

    def start(self):
        try:
            for t in self.threads:
                t.start()
        except:
            self.stop()

    def stop(self):
        for t in self.threads:
            t.stop()

    def wait_for_complete(self):
        try:
            for t in self.threads:
                while t.isAlive():
                    t.join(10)

        except KeyboardInterrupt:
            self.stop()
            print


if __name__ == "__main__":
    tp = ThreadPool(global_config.infos['thread_num'])
    for line in open('url.txt').readlines():
        hunter = hunter_plugin(line)
        tp.add_job(hunter.exploit)
    tp.start()
    try:
        tp.wait_for_complete()
        results = tp.get_result()
        print results
    except KeyboardInterrupt:
        tp.stop()

