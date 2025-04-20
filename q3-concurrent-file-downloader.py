import os
import time
import threading
import requests
from urllib.parse import urlparse

def download_file(url, output_dir="downloads"):
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        filename = os.path.basename(urlparse(url).path)
        if not filename:
            filename = f"file_{int(time.time())}.dat"
        
        filepath = os.path.join(output_dir, filename)
        
        start_time = time.time()
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        file_size = int(response.headers.get('content-length', 0))
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        end_time = time.time()
        print(f"Downloaded {filename} ({file_size/1024:.1f} KB) in {end_time - start_time:.2f} seconds")
        return True
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")
        return False

def sequential_download(urls, output_dir="downloads"):
    print("\nStarting sequential downloads...")
    start_time = time.time()
    success_count = 0
    
    for url in urls:
        if download_file(url, output_dir):
            success_count += 1
    
    end_time = time.time()
    total_time = end_time - start_time
    print(f"\nSequential download completed: {success_count}/{len(urls)} files in {total_time:.2f} seconds")
    return total_time

def threaded_download(urls, output_dir="downloads", max_threads=5):
    print("\nStarting threaded downloads with", max_threads, "threads...")
    start_time = time.time()
    threads = []
    success_count = [0]
    
    def download_and_count(url):
        if download_file(url, output_dir):
            success_count[0] += 1
    
    for url in urls:
        thread = threading.Thread(target=download_and_count, args=(url,))
        threads.append(thread)
        thread.start()
        
        while threading.active_count() > max_threads:
            time.sleep(0.1)
    
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    total_time = end_time - start_time
    print(f"\nThreaded download completed: {success_count[0]}/{len(urls)} files in {total_time:.2f} seconds")
    return total_time

def get_urls_from_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return []

def main():
    print("Concurrent File Downloader")
    print("=========================")
    
    while True:
        print("\nHow would you like to input URLs?")
        print("1. Enter URLs manually")
        print("2. Load URLs from a text file")
        print("3. Use sample URLs")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            print("\nEnter URLs one per line (enter a blank line to finish):")
            urls = []
            while True:
                url = input()
                if not url:
                    break
                urls.append(url)
                
        elif choice == '2':
            file_path = input("\nEnter the path to the text file containing URLs: ")
            urls = get_urls_from_file(file_path)
            
        elif choice == '3':
            urls = [
                "https://www.netflix.com/in/",
                "https://www.apple.com/in/",
                "https://www.google.co.in/?client=safari&channel=mac_bm",
                "https://in.pinterest.com",
                "https://www.linkedin.com/in/shruti-ashok-641326310/"
            ]
            print("\nUsing sample URLs:")
            for url in urls:
                print(f"- {url}")
                
        elif choice == '4':
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")
            continue
        
        if not urls:
            print("No URLs to download. Please try again.")
            continue
        
        output_dir = input("\nEnter download directory (default: downloads): ") or "downloads"
        
        try:
            max_threads = int(input("\nEnter maximum number of concurrent downloads (default: 5): ") or "5")
        except ValueError:
            max_threads = 5
            print("Invalid number, using default of 5 threads.")
        
        sequential_time = sequential_download(urls, output_dir)
        threaded_time = threaded_download(urls, output_dir, max_threads)
        
        speedup = sequential_time / threaded_time if threaded_time > 0 else 0
        print(f"\nPerformance comparison:")
        print(f"- Sequential: {sequential_time:.2f} seconds")
        print(f"- Threaded:   {threaded_time:.2f} seconds")
        print(f"- Speedup:    {speedup:.2f}x")
        
        print("\nWould you like to download more files? (y/n)")
        if input().lower() != 'y':
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()