## Запуск в Minikube

1. Запустить кластер:
```bash
minikube start
```

2.  Применить манифесты 
```bash
kubectl apply -f 1_configmap.yaml
kubectl apply -f 2_postgres_deployment.yaml
kubectl apply -f 3_spark-deployment.yaml
```
