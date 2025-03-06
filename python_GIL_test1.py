import multiprocessing
import threading
import time

def cpu_task():
    count = 0
    for _ in range(10**7): 
        count += 1

if __name__ == "__main__":
    start = time.time()
    p1 = multiprocessing.Process(target=cpu_task)
    p2 = multiprocessing.Process(target=cpu_task)

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    end = time.time()
    print(f"Total time taken: {end - start:.2f} seconds")
