#!/usr/bin/env bash

echo "Create ns"
kubectl create namespace monitoring
kubectl create namespace myapp

echo "Set context ns 'monitoring'"
kubectl config set-context --current --namespace=monitoring

echo "Helm install prometheus-operator"
helm install prom stable/prometheus-operator -f prometheus.yaml --atomic

echo "Helm install nginx-ingress"
helm install nginx stable/nginx-ingress -f nginx-ingress.yaml --atomic

echo "Set context ns 'myapp'"
kubectl config set-context --current --namespace=myapp

echo "Helm install myapp"
helm dependency update ./hw2-chart
helm install myapp ./hw3-chart
