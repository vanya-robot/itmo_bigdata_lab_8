# Kubernetes Commands for Lab 8

## Apply Manifests
```bash
kubectl apply -f k8s/
```

## View Pods
```bash
kubectl get pods
```

## View Logs of a Pod
```bash
kubectl logs <pod-name>
```

## Monitor Resource Utilization
```bash
kubectl top pods
```

# Resource Utilization Monitoring

## Spark Resource Monitoring
To monitor the resource utilization of the Spark pod, use the following command:
```bash
kubectl top pod -l app=spark
```
This will display CPU and memory usage for the Spark pod.

## Hadoop Resource Monitoring
To monitor the resource utilization of Hadoop NameNode and DataNode, use:
```bash
kubectl top pod -l app=hadoop-namenode
kubectl top pod -l app=hadoop-datanode
```
These commands will show the CPU and memory usage for the respective pods.