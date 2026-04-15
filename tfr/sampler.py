import time
import psutil

class Sampler:
    def __init__(self, interval=10):
        self.interval = interval

    def sample_once(self):
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_io_counters()
        net = psutil.net_io_counters()

        processes = []
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(p.info)
            except Exception:
                continue

        top_cpu = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:3]
        top_mem = sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:3]

        return {
            'timestamp': time.time(),
            'cpu_total': cpu,
            'mem_total': mem,
            'disk_read': disk.read_bytes,
            'disk_write': disk.write_bytes,
            'net_sent': net.bytes_sent,
            'net_recv': net.bytes_recv,
            'proc_count': len(processes),
            'top_cpu': top_cpu,
            'top_mem': top_mem
        }

    def run(self, callback):
        while True:
            data = self.sample_once()
            callback(data)
            time.sleep(self.interval)
