# Déploiement Kubernetes - Guide Rapide

## Prérequis

- Docker Desktop avec Kubernetes activé
- kubectl installé

## Installation

### 1. Activer Kubernetes dans Docker Desktop

Docker Desktop > Settings > Kubernetes > Enable Kubernetes

### 2. Construire l'image

```bash
docker build -t clients-api:latest TEACHING-K8S_dummy_api-main
```

### 3. Installer l'Ingress Controller

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.11.2/deploy/static/provider/cloud/deploy.yaml

kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s
```

### 4. Déployer l'application

```bash
kubectl apply -f k8s/
```

### 5. Tester

```bash
# Health check
curl http://localhost/beautiful_unicorn/health

# Liste des clients
curl http://localhost/beautiful_unicorn/clients

# Créer un client
curl -X POST http://localhost/beautiful_unicorn/clients \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Test","last_name":"User","email":"test@example.com"}'

# Récupérer un client
curl http://localhost/beautiful_unicorn/clients/1

# Supprimer un client
curl -X DELETE http://localhost/beautiful_unicorn/clients/1
```

## Commandes utiles

```bash
# Voir les pods
kubectl get pods

# Voir les logs de l'API
kubectl logs -l app=api --tail=50 -f

# Voir les logs MySQL
kubectl logs -l app=mysql --tail=50

# Supprimer tout
kubectl delete -f k8s/
```

## Endpoints

- Health: http://localhost/beautiful_unicorn/health
- API Clients: http://localhost/beautiful_unicorn/clients
