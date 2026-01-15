# Réponses aux questions pédagogiques

## Volume et persistance

### Quel est le rôle d'un volume dans un déploiement Kubernetes ?

Un volume permet de persister les données au-delà du cycle de vie d'un Pod. Sans volume, toutes les données stockées dans le conteneur seraient perdues lors de son redémarrage ou suppression.

### Que signifie la mention storageClassName dans un PVC, et que peut-elle impliquer côté cloud ?

La `storageClassName` définit le type de stockage à provisionner (SSD, HDD, performances, etc.). Côté cloud (Azure, AWS, GCP), cela déclenche automatiquement la création de ressources de stockage cloud (Azure Disk, EBS, Persistent Disk) avec les caractéristiques spécifiées (taille, IOPS, réplication).

### Que se passe-t-il si le pod MySQL disparaît ?

Grâce au PersistentVolumeClaim (PVC), les données sont préservées sur le volume persistant. Kubernetes recréera automatiquement un nouveau Pod MySQL qui se reconnectera au même volume, retrouvant ainsi toutes les données intactes.

### Qu'est-ce qui relie un PersistentVolumeClaim à un volume physique ?

Le PersistentVolume (PV) est la ressource physique de stockage. Kubernetes effectue un "binding" automatique entre le PVC (demande de stockage) et un PV disponible qui correspond aux critères demandés (taille, mode d'accès, classe de stockage).

### Comment le cluster gère-t-il la création ou la suppression du stockage sous-jacent ?

Le provisionnement dynamique utilise un StorageClass avec un "provisioner" qui crée automatiquement le PV et le stockage cloud associé lors de la création du PVC. À la suppression, la politique de récupération (`reclaimPolicy`: Delete/Retain) détermine si le stockage est supprimé ou conservé.

## Ingress et health probe

### À quoi sert un Ingress dans Kubernetes ?

L'Ingress expose les services HTTP/HTTPS à l'extérieur du cluster en définissant des règles de routage (basées sur le chemin, le host, etc.) et centralise la gestion du trafic entrant.

### Quelle différence y a-t-il entre un Ingress et un Ingress Controller ?

- **Ingress** : ressource Kubernetes (manifest YAML) qui déclare les règles de routage
- **Ingress Controller** : composant logiciel (NGINX, Traefik, HAProxy) qui lit ces règles et les implémente réellement en configurant un reverse proxy

### À quoi sert un health probe dans une architecture de déploiement ?

Les health probes permettent à Kubernetes de vérifier l'état de santé d'une application :
- **livenessProbe** : détecte si l'application est bloquée et doit être redémarrée
- **readinessProbe** : détermine si le Pod est prêt à recevoir du trafic

### Quelle est la relation entre le chemin défini dans l'annotation du probe et les routes réellement exposées par l'application ?

L'annotation `nginx.ingress.kubernetes.io/health-check-path` définit le chemin que l'Ingress Controller utilisera pour vérifier la santé du backend. Ce chemin doit correspondre à une route existante dans l'application (ex: `/beautiful_unicorn/health` doit être géré par l'API FastAPI).

### Comment mettre en place un chemin de préfixe (ex. /votre_namespace) dans l'Ingress, et quelle configuration doit être ajustée ?

**Côté Ingress (ingress.yaml)** :
```yaml
annotations:
  nginx.ingress.kubernetes.io/rewrite-target: /$2
  nginx.ingress.kubernetes.io/use-regex: "true"
spec:
  rules:
  - http:
      paths:
      - path: /beautiful_unicorn(/|$)(.*)
```

**Côté Application (api-configmap.yaml)** :
```yaml
data:
  ROOT_PATH: "/beautiful_unicorn"
```

L'annotation `rewrite-target` supprime le préfixe avant de transmettre la requête au service, tandis que `ROOT_PATH` informe FastAPI de son préfixe pour générer correctement les URLs.

### Comment le contrôleur d'ingress décide-t-il si un service est "sain" ou non ?

L'Ingress Controller envoie des requêtes HTTP périodiques au chemin défini dans `health-check-path`. Si la réponse retourne un code HTTP 2xx (200-299), le service est considéré comme sain. En cas d'échec répété, le backend est marqué comme indisponible et retiré du pool de routage.
