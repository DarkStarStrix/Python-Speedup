import numpy as np
import asyncio
import time
import matplotlib.pyplot as plt
import multiprocessing

from concurrent.futures import ProcessPoolExecutor
from rust_python_integration import rust_computation_wrapper


class RustPythonIntegration:
    def __init__(self):
        self.loop = asyncio.get_event_loop ()

    async def main_async(self, data):
        chunk_size = 1000  # Fixed chunk size
        chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

        result_queue = asyncio.Queue()
        tasks = [self.loop.run_in_executor(None, self.process_chunk, chunk, result_queue) for chunk in chunks]
        await asyncio.gather(*tasks)

        results = np.array([])  # Using a NumPy array for results
        while not result_queue.empty():
            results = np.append(results, result_queue.get_nowait())

        plt.plot(data, results, label='Processed Data')
        plt.xlabel('Input Data')
        plt.ylabel('Computed Result')
        plt.title('Rust Integration with Python, AsyncIO, and Multiprocessing')
        plt.legend()
        plt.show()

    @staticmethod
    def process_chunk(chunk, result_queue):
        with ProcessPoolExecutor() as executor:
            results = executor.map(rust_computation_wrapper, chunk)
        result_queue.put(list(results))


if __name__ == "__main__":
    start_time = time.time()

    rust_python_integration = RustPythonIntegration()
    data = np.arange(10_000)
    asyncio.run(rust_python_integration.main_async(data))

    print(f"Execution time: {time.time() - start_time} seconds")
