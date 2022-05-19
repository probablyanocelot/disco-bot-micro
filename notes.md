1. PROPER QUEUE SETUP

(possible solution? check validity)
Well, one way is to use a queue design that can keep an internal lists of waiting and working threads. You can then create several consumer threads to wait on the queue and, when work arrives, set a known consumer thread to do the work. When the thread has finished, it calls into the queue to remove itself from the working list and add itself to the waiting list.

The consumer threads each have an 'abort' atomic that can signal the thread to finish early. There will be some latency while the thread performs inner loops, but that will not matter....

If new work arrives at the queue from the producer, and the working queue is not empty, the 'abort' bool of the working thread/s can be set and their priority set to the minimum possible. The new work can then be dispatched onto one of the waiting threads from the pool, so setting it working.

The waiting threads will need a 'start' function that signals an event/sema/condvar that the wait thread..well..waits on. That allows the producer that supplied work to set that specific thread running, rather than the 'usual' practice where any thread from a pool may pick up work.

Such a design allows new work to be started 'immediately', makes the previous work thread irrelevant by de-prioritizing it and avoids the overheads of thread/process termination.


2. PSYCOPG2 on python-alpine

    INSTALL PSYCOPG2 (NOT PYSCOPG2-BINARIES); MAYBE NEED DEPENDENCIES
        https://github.com/psycopg/psycopg2/issues/684