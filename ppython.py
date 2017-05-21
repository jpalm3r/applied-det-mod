import math, sys, time
import pp

def mersenne_primes(n):

    """ Return a list of the prime numbers <= n. """

    sieve = [True] * (n // 2)
    for i in range(3, int(math.sqrt(n))+1, 2):
        if sieve[i//2]:
            sieve[i*i//2::i] = [False] * ((n - i*i - 1) // (2*i) +1)
    return [2] + [2*i+1 for i in range(1, n // 2) if sieve[i]]

#print """Usage: python sum_primes.py [ncpus]
#    [ncpus] - the number of workers to run in parallel,
#    if omitted it will be set to the number of processors in the system
#"""

# tuple of all parallel python servers to connect with
ppservers = ()
#ppservers = ("10.0.0.1",)

if len(sys.argv) > 1:
    ncpus = int(sys.argv[1])
    # Creates jobserver with ncpus workers
    job_server = pp.Server(ncpus, ppservers=ppservers)
else:
    # Creates jobserver with automatically detected number of workers
    job_server = pp.Server(ppservers=ppservers)

print "Starting pp with", job_server.get_ncpus(), "workers"

# Submit a job of calulating sum_primes(100) for execution.
# sum_primes - the function
# (100,) - tuple with arguments for sum_primes
# (isprime,) - tuple with functions on which function sum_primes depends
# ("math",) - tuple with module names which must be imported before sum_primes execution
# Execution starts as soon as one of the workers will become available

job1 = job_server.submit(mersenne_primes, (1000,), ("math",))

# Retrieves the result calculated by job1
# The value of job1() is the same as sum_primes(100)
# If the job has not been finished yet, execution will wait here until result is available
result = job1()

print ("Mersenne primes below 100 are %s" %(result))

start_time = time.time()

# The following submits 8 jobs and then retrieves the results
inputs = (100000, 100100, 100200, 100300, 100400, 100500, 100600, 100700)
jobs = [(input, job_server.submit(mersenne_primes,(input,), ("math",))) for input in inputs]
for input, job in jobs:

    print ("Mersenne primes below %s are %s" %(input, job()))

print "Time elapsed: ", time.time() - start_time, "s"
job_server.print_stats()
