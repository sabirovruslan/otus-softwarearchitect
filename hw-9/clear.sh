#!/usr/bin/env bash

echo "Helm delete app charts"
helm delete order-app
helm delete payment-app
helm delete store-app

echo "Helm delete kafka-release"
helm delete kafka-release

echo "Delete"
kubectl delete all --all
kubectl delete namespace myapp

echo "Set context ns 'default'"
kubectl config set-context --current --namespace=default
