# Deployment

## Environments

| Environment | Trigger                        | URL                          |
|-------------|--------------------------------|------------------------------|
| preview     | PR opened / push to feature branch | `https://pr-{n}.example.dev` |
| staging     | Merge to `main`                | `https://staging.example.com`|
| production  | Tag `v*.*.*`                   | `https://example.com`        |

## Container layout

Each service ships as its own Docker image. Images are built via multi-stage Dockerfiles and pushed to a private container registry.

```
registry.example.com/
  next-app:sha-<commit>
  users-api:sha-<commit>
  items-api:sha-<commit>
  notif-api:sha-<commit>
```

## Kubernetes resources (per service)

- `Deployment` — rolling update, 2 replicas minimum in production
- `Service` — ClusterIP; only the Next.js app is exposed via an Ingress
- `HorizontalPodAutoscaler` — scale on CPU > 70%
- `ConfigMap` — non-secret environment variables
- `ExternalSecret` — syncs secrets from AWS Secrets Manager

## CI/CD pipeline

```
Push → GitHub Actions
  lint + typecheck
  unit tests
  build Docker image
  push to registry
  helm upgrade --install (via ArgoCD sync)
```

## Environment variables

Never bake secrets into images. Inject at runtime via Kubernetes secrets:

| Variable              | Consumer        | Description                    |
|-----------------------|-----------------|--------------------------------|
| `DATABASE_URL`        | microservices   | PostgreSQL connection string   |
| `NEXTAUTH_SECRET`     | next-app        | JWT signing key                |
| `USERS_API_URL`       | next-app        | Internal service URL           |
| `ITEMS_API_URL`       | next-app        | Internal service URL           |
| `NOTIF_API_URL`       | next-app        | Internal service URL           |