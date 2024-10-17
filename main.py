from fastapi import FastAPI
import numpy as np
import requests
import time

app = FastAPI()

def cpu_intensive_task():
    matrix_size = 500
    A = np.random.rand(matrix_size, matrix_size)
    B = np.random.rand(matrix_size, matrix_size)
    result = np.dot(A, B)
    return result

def memory_intensive_task():
    large_list = [i for i in range(10**7)]
    return len(large_list)

def network_intensive_task():
    response = requests.get('https://httpbin.org/delay/2')
    return response.json()

@app.get("/calculate")
def calculate():
    start_time = time.time()
    
    cpu_result = cpu_intensive_task()
    
    memory_result = memory_intensive_task()
    
    network_result = network_intensive_task()
    
    elapsed_time = time.time() - start_time
    return {
        "cpu_result": str(cpu_result[0][0]),
        "memory_result": memory_result,
        "network_result": network_result,
        "elapsed_time": elapsed_time
    }
