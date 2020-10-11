#!/usr/bin/env bash

echo "Create ns"
kubectl create namespace myapp

echo "Set context ns 'myapp'"
kubectl config set-context --current --namespace=myapp

minikube addons enable ingress

echo "Helm install order-app"
helm dependency update ./order-chart
helm install order-app ./order-chart