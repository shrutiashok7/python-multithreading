import threading
import time
import random
import concurrent.futures

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quicksort(arr, low, high):
    if low < high:
        pivot_idx = partition(arr, low, high)
        quicksort(arr, low, pivot_idx - 1)
        quicksort(arr, pivot_idx + 1, high)

def single_threaded_quicksort(arr):
    arr_copy = arr.copy()
    quicksort(arr_copy, 0, len(arr_copy) - 1)
    return arr_copy

def threaded_quicksort(arr, low, high, max_threads, current_depth=0):
    if low < high:
        pivot_idx = partition(arr, low, high)
        
        if current_depth < max_threads:
            left_done = threading.Event()
            
            def sort_left():
                threaded_quicksort(arr, low, pivot_idx - 1, max_threads, current_depth + 1)
                left_done.set()
            
            thread = threading.Thread(target=sort_left)
            thread.start()
            
            threaded_quicksort(arr, pivot_idx + 1, high, max_threads, current_depth + 1)
            
            left_done.wait()
        else:
            quicksort(arr, low, pivot_idx - 1)
            quicksort(arr, pivot_idx + 1, high)

def multi_threaded_quicksort(arr, max_threads=4):
    arr_copy = arr.copy()
    threaded_quicksort(arr_copy, 0, len(arr_copy) - 1, max_threads)
    return arr_copy

def multi_threaded_quicksort_pool(arr, max_workers=4):
    if len(arr) <= 1:
        return arr
    
    arr_copy = arr.copy()
    pivot = arr_copy.pop()
    
    left = [x for x in arr_copy if x <= pivot]
    right = [x for x in arr_copy if x > pivot]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_left = executor.submit(multi_threaded_quicksort_pool, left, max_workers)
        future_right = executor.submit(multi_threaded_quicksort_pool, right, max_workers)
        
        sorted_left = future_left.result()
        sorted_right = future_right.result()
    
    return sorted_left + [pivot] + sorted_right

def compare_quicksorts(arr_size=10000, max_threads=4):
    arr = [random.randint(1, 100000) for _ in range(arr_size)]
    print(f"Array size: {arr_size}")
    print(f"Max threads: {max_threads}")
    
    start_time = time.time()
    single_sorted = single_threaded_quicksort(arr)
    single_time = time.time() - start_time
    print(f"Single-threaded time: {single_time:.4f} seconds")
    
    start_time = time.time()
    multi_sorted = multi_threaded_quicksort(arr, max_threads)
    multi_time = time.time() - start_time
    print(f"Multi-threaded time: {multi_time:.4f} seconds")
    
    start_time = time.time()
    pool_sorted = multi_threaded_quicksort_pool(arr, max_threads)
    pool_time = time.time() - start_time
    print(f"Thread pool time: {pool_time:.4f} seconds")
    
    print(f"Results match (threads): {single_sorted == multi_sorted}")
    print(f"Results match (pool): {single_sorted == pool_sorted}")
    print(f"Speedup (threads): {single_time / multi_time:.2f}x")
    print(f"Speedup (pool): {single_time / pool_time:.2f}x")

if __name__ == "__main__":
    small_array = [38, 27, 43, 3, 9, 82, 10]
    print("Original array:", small_array)
    sorted_array = multi_threaded_quicksort(small_array)
    print("Sorted array:", sorted_array)
    print()
    
    for size in [1000, 10000, 50000]:
        compare_quicksorts(size)
        print()