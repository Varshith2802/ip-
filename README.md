\# IP Reputation Checker (Microservices on Kubernetes)



\*\*Author:\*\* ntvs28  

\*\*Stack:\*\* FastAPI (API), Express (Analysis), FastAPI (Auth), NGINX (Frontend), MongoDB (DB)



\## What it does

A tiny app where users can register/login and look up an IP’s “reputation”. The API calls an analysis microservice, which returns normalized reputation info. Results are shown via a static frontend served by NGINX. MongoDB stores users.



\## Microservices

\- \*\*frontend-web\*\*: NGINX serving `index.html`; proxies `/api/\*` to `api-service` and `/auth/\*` to `auth-service`.

\- \*\*api-service\*\* (FastAPI @ :8000): `/api/health`, `/api/check-ip/{ip}` (calls analysis-service), error handling.

\- \*\*analysis-service\*\* (Express @ :8002): `/check-ip?ip=…` returns mock reputation JSON (no `/health`).

\- \*\*auth-service\*\* (FastAPI @ :8001): `/auth/register`, `/auth/login` against MongoDB.

\- \*\*mongodb\*\*: backing store with \*\*persistent volume\*\* via PVC.



\## Why it’s “cloudy”

\- Deployable on \*\*Kubernetes\*\*.

\- \*\*At least two\*\* independent microservices + \*\*database\*\* ✅

\- All have \*\*REST APIs\*\* ✅

\- App reachable from outside via \*\*NodePort 30080\*\* (browser/curl) ✅

\- \*\*Independent horizontal scaling\*\* of each Deployment ✅

\- Images pushed to Docker Hub so K8s can pull:

&nbsp; - `docker.io/ntvs28/ip-reputation-checker-frontend-web:v1`

&nbsp; - `docker.io/ntvs28/ip-reputation-checker-api-service:v1`

&nbsp; - `docker.io/ntvs28/ip-reputation-checker-analysis-service:v1`

&nbsp; - `docker.io/ntvs28/ip-reputation-checker-auth-service:v1`

\- \*\*MongoDB uses PVC\*\* (StorageClass `hostpath` on Docker Desktop) ✅



\## Run on Kubernetes



```bash

\# Use docker-desktop context

kubectl config use-context docker-desktop



\# Apply manifests (namespace, PVC, Deployments, Services)

kubectl apply -R -f kubernetes/



\# Watch

kubectl -n ip-reputation get all



\# Access UI via NodePort

\# Browser: http://127.0.0.1:30080/

\# Health:

curl -i http://127.0.0.1:30080/api/health



