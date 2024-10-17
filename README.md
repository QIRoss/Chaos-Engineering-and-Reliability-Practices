# Chaos Engineering and Reliability Practices

Alternative solution/studies based in day 41-42 of 100 Days System Design for DevOps and Cloud Engineers.

https://deoshankar.medium.com/100-days-system-design-for-devops-and-cloud-engineers-18af7a80bc6f

Days 41–50: Reliability Engineering

Day 41–42: Implement advanced chaos engineering practices using tools like Gremlin.

## Project Overview

This project demonstrates advanced chaos engineering practices using Docker and Pumba to stress-test a FastAPI application. The FastAPI app simulates CPU, memory, and network operations, and ```stress-ng``` and ```toxiproxy```are  used to inject faults such as network latency, packet loss, CPU stress, and memory exhaustion to evaluate the application’s resilience.

## How to Use

Clone the repository and navigate to the project directory.

Start the FastAPI application with Docker Compose:

Access the FastAPI app at ```http://localhost:8000/calculate```.

Use Pumba to inject chaos into the running container and observe the app's behavior.

## Simulate Stress Instructions

### Stress-ng CPU an Memory Scenarios:

To stress the CPU for 30 seconds, run:
```
docker exec -d fastapi-chaos-app stress-ng --cpu 4 --timeout 30s
```

To stress the memory by allocating 1GB for 30 seconds:
```
docker exec -d fastapi-chaos-app stress-ng --vm 1 --vm-bytes 1G --timeout 30s
```

### Toxiproxy Chaos Scenarios

Start the Toxiproxy container:
```
docker run -d -p 8474:8474 --name toxiproxy shopify/toxiproxy
```

Create a network proxy for your FastAPI container using Toxiproxy:
```
curl -XPOST 'http://localhost:8474/proxies' -d '
{
  "name": "fastapi_proxy",
  "listen": "0.0.0.0:8001",
  "upstream": "fastapi-chaos-app:8000"
}'
```

Add 1000ms of network latency to the FastAPI app via Toxiproxy:
```
curl -XPOST 'http://localhost:8474/proxies/fastapi_proxy/toxics' -d '
{
  "name": "latency_toxic",
  "type": "latency",
  "attributes": {
    "latency": 1000
  }
}'
```

```
curl -XPOST 'http://localhost:8474/proxies/fastapi_proxy/toxics' -d '
{
  "name": "bandwidth_toxic",
  "type": "bandwidth",
  "attributes": {
    "rate": 100
  }
}'
```

To remove the toxic you created (e.g., latency_toxic):
```
curl -XDELETE 'http://localhost:8474/proxies/fastapi_proxy/toxics/latency_toxic'
```

## Author
This project was implemented by [Lucas de Queiroz dos Reis][2]. It is based on the [100 Days System Design for DevOps and Cloud Engineers][1].

[1]: https://deoshankar.medium.com/100-days-system-design-for-devops-and-cloud-engineers-18af7a80bc6f "Medium - Deo Shankar 100 Days"
[2]: https://www.linkedin.com/in/lucas-de-queiroz/ "LinkedIn - Lucas de Queiroz"