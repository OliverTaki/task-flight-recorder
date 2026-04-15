from tfr.sampler import Sampler
from tfr.storage import Storage

storage = Storage()
sampler = Sampler(interval=10)

def handle(data):
    storage.insert(data)
    print(f"[{data['timestamp']}] CPU={data['cpu_total']} MEM={data['mem_total']}")

if __name__ == '__main__':
    sampler.run(handle)
