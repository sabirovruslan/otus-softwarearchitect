#!/usr/bin/env bash

echo "Create ns"
kubectl create namespace myapp

echo "Set context ns 'myapp'"
kubectl config set-context --current --namespace=myapp

minikube addons enable ingress

echo "Helm install auth-app"
helm dependency update ./auth-app/auth-app-chart
helm install auth-app ./auth-app/auth-app-chart

echo "Helm install simple-app"
helm install simple-app ./simple-app/simple-app-chart

kubectl apply -f auth-app-ingress.yaml -f simple-app-ingress.yaml