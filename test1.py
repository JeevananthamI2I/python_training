import threading
import requests
import time

urls = [
    "https://www.example.com",
    "https://www.wikipedia.org",
    "https://www.python.org",
    "https://www.github.com",
    "https://www.stackoverflow.com"
]

def fetch_page(url):
    print(f"Fetching: {url}")
    response = requests.get(url)
    print(f"Completed: {url} | Size: {len(response.content)} bytes")


start_time = time.time()
for url in urls:
    fetch_page(url)
end_time = time.time()
print(f"Time taken without threading: {end_time - start_time:.2f} seconds\n")

start_time = time.time()

threads = []
for url in urls:
    thread = threading.Thread(target=fetch_page, args=(url,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

end_time = time.time()
print(f"Time taken with threading: {end_time - start_time:.2f} seconds")
