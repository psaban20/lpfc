# Azure Deployment Guide

## Architecture Overview

- **Azure Container Registry (ACR)**: `lpfcregistry.azurecr.io`
- **Azure Container Apps**: Serverless container hosting
- **Azure SQL Database**: Shared between local dev and production
- **GitHub Actions**: CI/CD pipeline

## Prerequisites

- Azure CLI installed
- GitHub repository created
- Azure subscription: LPFC
- Resource Group: LPFC-Resource-Group

## Setup Steps Completed

### 1. Azure Container Registry (ACR)
✅ Created: `lpfcregistry.azurecr.io`
✅ Admin access enabled

### 2. Container Apps Environment
⏳ In progress: `lpfc-environment`

### 3. GitHub Actions Workflow
✅ Created: `.github/workflows/azure-deploy.yml`

## Remaining Steps

### Step 1: Create Azure Container Apps

Run these commands to create the backend and frontend container apps:

```bash
# Get ACR credentials
ACR_USERNAME=$(az acr credential show --name lpfcregistry --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name lpfcregistry --query passwords[0].value -o tsv)

# Create backend container app
az containerapp create \
  --name lpfc-backend-app \
  --resource-group LPFC-Resource-Group \
  --environment lpfc-environment \
  --image lpfcregistry.azurecr.io/lpfc-backend:latest \
  --target-port 8000 \
  --ingress external \
  --registry-server lpfcregistry.azurecr.io \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --env-vars \
    DB_SERVER=lpfc.database.windows.net \
    DB_DATABASE=lpfc \
    DB_USERNAME=appuser@lpfc.database.windows.net \
    DB_PASSWORD=secretref:db-password \
  --secrets db-password='!Jenn1980' \
  --cpu 0.5 \
  --memory 1Gi

# Get backend URL
BACKEND_URL=$(az containerapp show --name lpfc-backend-app --resource-group LPFC-Resource-Group --query properties.configuration.ingress.fqdn -o tsv)

# Create frontend container app
az containerapp create \
  --name lpfc-frontend-app \
  --resource-group LPFC-Resource-Group \
  --environment lpfc-environment \
  --image lpfcregistry.azurecr.io/lpfc-frontend:latest \
  --target-port 3000 \
  --ingress external \
  --registry-server lpfcregistry.azurecr.io \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --env-vars NEXT_PUBLIC_API_URL=https://$BACKEND_URL \
  --cpu 0.5 \
  --memory 1Gi
```

### Step 2: Set up GitHub Secrets

Create a service principal and configure GitHub secrets:

```bash
# Create service principal
az ad sp create-for-rbac \
  --name "lpfc-github-actions" \
  --role contributor \
  --scopes /subscriptions/f75d1a76-d114-4764-814c-c28fa5ab9eed/resourceGroups/LPFC-Resource-Group \
  --sdk-auth
```

Copy the entire JSON output and:
1. Go to GitHub repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `AZURE_CREDENTIALS`
4. Paste the JSON output
5. Click "Add secret"

### Step 3: Initial Docker Image Push

Build and push initial images manually:

```bash
# Login to ACR
az acr login --name lpfcregistry

# Build and push backend
docker build -t lpfcregistry.azurecr.io/lpfc-backend:latest ./backend
docker push lpfcregistry.azurecr.io/lpfc-backend:latest

# Build and push frontend
docker build -t lpfcregistry.azurecr.io/lpfc-frontend:latest ./frontend
docker push lpfcregistry.azurecr.io/lpfc-frontend:latest
```

### Step 4: Test the Pipeline

1. Commit and push changes to GitHub
2. GitHub Actions will automatically:
   - Run health checks
   - Build frontend
   - Build and push Docker images to ACR
   - Deploy to Azure Container Apps
3. Monitor the workflow at: https://github.com/psaban20/lpfc/actions

## CI/CD Pipeline Flow

```
Push to GitHub (master/main branch)
  ↓
Build and Test Job
  - Install dependencies
  - Run health checks
  - Build frontend
  ↓
Deploy Job (only on push to master/main)
  - Login to Azure
  - Build Docker images
  - Push to ACR
  - Update Container Apps
```

## Testing Before Deploy

The pipeline includes a `build-and-test` job that:
- ✅ Validates Python dependencies
- ✅ Checks backend models load correctly
- ✅ Validates Node.js dependencies
- ✅ Builds frontend (catches TypeScript errors)

Only if all tests pass will the deploy job run.

## Database Configuration

The production containers connect to the same Azure SQL Database as your local development:
- **Server**: lpfc.database.windows.net
- **Database**: lpfc
- **Username**: appuser@lpfc.database.windows.net
- **Password**: Stored as Azure Container App secret

## Monitoring and Logs

View logs:
```bash
# Backend logs
az containerapp logs show --name lpfc-backend-app --resource-group LPFC-Resource-Group --follow

# Frontend logs
az containerapp logs show --name lpfc-frontend-app --resource-group LPFC-Resource-Group --follow
```

## VS Code Extensions (Optional)

While not required, these extensions make Azure management easier:
- **Azure Account** - Sign in to Azure
- **Azure Resources** - View and manage Azure resources
- **Docker** - Build and manage Docker images

However, everything can be done via Azure CLI and GitHub Actions.

## Cost Optimization

- Container Apps use consumption-based pricing (pay per use)
- Apps scale to zero when not in use
- Basic ACR tier is sufficient for this project
- Estimated cost: ~$20-30/month for small traffic

## Troubleshooting

**If deployment fails:**
1. Check GitHub Actions logs
2. Verify Azure credentials secret is set correctly
3. Check Container App logs
4. Ensure database firewall allows Azure services

**If app doesn't load:**
1. Check Container App ingress settings
2. Verify environment variables are set
3. Check database connection from Azure

## URLs After Deployment

Once deployed, you'll have:
- **Frontend**: https://lpfc-frontend-app.{random-suffix}.eastus.azurecontainerapps.io
- **Backend**: https://lpfc-backend-app.{random-suffix}.eastus.azurecontainerapps.io
