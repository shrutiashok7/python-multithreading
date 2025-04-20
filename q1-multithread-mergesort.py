import threading
import time
import random

def merge(left, right):
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge_sort_threaded(arr, thread_count=2):
    if thread_count <= 1 or len(arr) <= 1:
        return merge_sort(arr)
    
    mid = len(arr) // 2
    
    #result containers
    left_result = [None]
    right_result = [None]
    
    #thread functions
    def left_thread():
        left_result[0] = merge_sort_threaded(arr[:mid], thread_count // 2)
    
    def right_thread():
        right_result[0] = merge_sort_threaded(arr[mid:], thread_count // 2)
    
    #create and start threads
    t1 = threading.Thread(target=left_thread)
    t2 = threading.Thread(target=right_thread)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    #merge results
    return merge(left_result[0], right_result[0])

def compare_sorts(arr_size=10000, thread_count=4):
    #random array generaton
    arr = [random.randint(1, 100000) for _ in range(arr_size)]
    arr_copy = arr.copy()
    
    print(f"Array size: {arr_size}")
    print(f"Thread count: {thread_count}")
    
    #single-threaded merge sort
    start_time = time.time()
    sorted_arr = merge_sort(arr)
    single_time = time.time() - start_time
    print(f"Single-threaded time: {single_time:.4f} seconds")
    
    #multi-threaded merge sort
    start_time = time.time()
    threaded_sorted_arr = merge_sort_threaded(arr_copy, thread_count)
    multi_time = time.time() - start_time
    print(f"Multi-threaded time: {multi_time:.4f} seconds")
    
    #verification
    print(f"Results match: {sorted_arr == threaded_sorted_arr}")
    print(f"Speedup: {single_time / multi_time:.2f}x")
    
    return sorted_arr, threaded_sorted_arr

if __name__ == "__main__":
    #example
    sample_arr = [38, 27, 43, 3, 9, 82, 10]
    print("Sample array:", sample_arr)
    sorted_sample = merge_sort_threaded(sample_arr)
    print("Sorted array:", sorted_sample)
    print()
    
    #comapre
    for size in [1000, 10000, 100000]:
        compare_sorts(size)
        print()