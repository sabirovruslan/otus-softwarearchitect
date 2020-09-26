#!/usr/bin/env bash

echo "Create ns"
kubectl create namespace myapp

echo "Set context ns 'myapp'"
kubectl config set-context --current --namespace=myapp

echo "Helm add repo ambassador"
helm repo add datawire https://getambassador.io
helm install aes datawire/ambassador -f ambassador_values.yaml
kubectl apply -f ambassador/

echo "Helm install auth-app"
helm dependency update ./auth-app/auth-app-chart
helm install auth-app ./auth-app/auth-app-chart

echo "Helm install simple-app"
helm install simple-app ./simple-app/simple-app-chart
