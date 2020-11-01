#!/usr/bin/env bash

echo "Helm delete order-app"
helm delete order-app

echo "Helm delete kafka-release"
helm delete kafka-release

echo "Delete"
kubectl delete all --all
kubectl delete namespace myapp

echo "Set context ns 'default'"
kubectl config set-context --current --namespace=default
