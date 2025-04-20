
Code 1:

By dividing the work across multiple threads, this program speeds up the traditional "divide and conquer" merge sort. Imagine several people sorting various parts of a deck of cards at the same time, then joining their sorted piles at the end. The threaded version operates on both halves simultaneously, whereas the standard merge sort handles each half one after the other.

output 1:
Sample array: [38, 27, 43, 3, 9, 82, 10]
Sorted array: [3, 9, 10, 27, 38, 43, 82]

Array size: 1000
Thread count: 4
Single-threaded time: 0.0010 seconds
Multi-threaded time: 0.0013 seconds
Results match: True
Speedup: 0.78x

Array size: 10000
Thread count: 4
Single-threaded time: 0.0131 seconds
Multi-threaded time: 0.0131 seconds
Results match: True
Speedup: 1.00x

Array size: 100000
Thread count: 4
Single-threaded time: 0.1648 seconds
Multi-threaded time: 0.1579 seconds
Results match: True
Speedup: 1.04x

Code 2:

Quicksort typically splits numbers into "smaller than" and "larger than" groups after selecting a "pivot" value. Then, it repeats this procedure for each group. The threaded version allows threads to function independently by allocating distinct groups to each thread. Instead of one person handling it all, it's like having multiple people organizing different book sections on a bookcase at simultaneously.

output 2:
Original array: [38, 27, 43, 3, 9, 82, 10]
Sorted array: [3, 9, 10, 27, 38, 43, 82]

Array size: 1000
Max threads: 4
Single-threaded time: 0.0006 seconds
Multi-threaded time: 0.0012 seconds
Thread pool time: 0.0884 seconds
Results match (threads): True
Results match (pool): True
Speedup (threads): 0.50x
Speedup (pool): 0.01x

Array size: 10000
Max threads: 4
Single-threaded time: 0.0083 seconds
Multi-threaded time: 0.0093 seconds

Code 3:

This program uses threads to open several "checkout lanes" rather than downloading files one at a time (like waiting in a single checkout line). A separate file is downloaded concurrently by each thread. This works particularly well since other downloads can continue to function while one waits for data from the internet. As a result, you will receive all of your data considerably more quickly, particularly if you are downloading from multiple sources.

output 3:
Concurrent File Downloader
=========================

How would you like to input URLs?
1. Enter URLs manually
2. Load URLs from a text file
3. Use sample URLs
4. Exit

Enter your choice (1-4): 3

Using sample URLs:
- https://www.netflix.com/in/
- https://www.apple.com/in/
- https://www.google.co.in/?client=safari&channel=mac_bm
- https://in.pinterest.com
- https://www.linkedin.com/in/shruti-ashok-641326310/

Enter download directory (default: downloads): downloads

Enter maximum number of concurrent downloads (default: 5): 4

Starting sequential downloads...
Downloaded file_1745149592.dat (0.0 KB) in 1.90 seconds
Downloaded file_1745149594.dat (33.9 KB) in 0.34 seconds
Downloaded file_1745149594.dat (0.0 KB) in 0.65 seconds
Downloaded file_1745149595.dat (0.0 KB) in 1.02 seconds
Downloaded file_1745149596.dat (1.5 KB) in 0.38 seconds

Sequential download completed: 5/5 files in 4.29 seconds

Starting threaded downloads with 4 threads...
Downloaded file_1745149596.dat (33.9 KB) in 0.35 seconds
Downloaded file_1745149596.dat (0.0 KB) in 0.54 seconds
Downloaded file_1745149597.dat (1.5 KB) in 0.31 seconds
Downloaded file_1745149596.dat (0.0 KB) in 0.76 seconds
Downloaded file_1745149596.dat (0.0 KB) in 1.91 seconds

Threaded download completed: 5/5 files in 1.91 seconds

Performance comparison:
- Sequential: 4.29 seconds
- Threaded:   1.91 seconds
- Speedup:    2.24x

Would you like to download more files? (y/n)
n
Goodbye!
