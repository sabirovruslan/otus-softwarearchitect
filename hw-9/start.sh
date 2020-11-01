#!/usr/bin/env bash

echo "Create ns"
kubectl create namespace myapp

echo "Set context ns 'myapp'"
kubectl config set-context --current --namespace=myapp

minikube addons enable ingress

echo "Helm install kafka"
helm repo add bitnami https://charts.bitnami.com/bitnami
#helm install kafka-release bitnami/kafka
helm install kafka-release bitnami/kafka --set externalAccess.service.type=NodePort

echo "Helm install order-app"
helm dependency update ./order-app/chart
helm install order-app ./order-app/chart

echo "Helm install payment-app"
helm dependency update ./payment-app/chart
helm install payment-app ./payment-app/chart

echo "Helm install store-app"
helm dependency update ./store-app/chart
helm install store-app ./store-app/chart