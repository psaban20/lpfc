# Complete Azure Deployment Steps

## What We've Done So Far ✅

1. ✅ Created Azure Container Registry: `lpfcregistry.azurecr.io`
2. ✅ Created GitHub Actions CI/CD workflow
3. ✅ Installed Azure CLI Container Apps extension
4. ⏳ Creating Container Apps Environment: `lpfc-environment`

## What You Need to Do Next

### Step 1: Wait for Environment Creation

The Container Apps environment is currently being created. This takes 3-5 minutes.

### Step 2: Build and Push Initial Docker Images

```bash
# Login to your Azure Container Registry
az acr login --name lpfcregistry

# Build and push backend image
docker build -t lpfcregistry.azurecr.io/lpfc-backend:latest ./backend
docker push lpfcregistry.azurecr.io/lpfc-backend:latest

# Build and push frontend image  
docker build -t lpfcregistry.azurecr.io/lpfc-frontend:latest ./frontend
docker push lpfcregistry.azurecr.io/lpfc-frontend:latest
```

### Step 3: Create Container Apps

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

# Get the backend URL
BACKEND_URL=$(az containerapp show --name lpfc-backend-app --resource-group LPFC-Resource-Group --query properties.configuration.ingress.fqdn -o tsv)
echo "Backend URL: https://$BACKEND_URL"

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

# Get the frontend URL
FRONTEND_URL=$(az containerapp show --name lpfc-frontend-app --resource-group LPFC-Resource-Group --query properties.configuration.ingress.fqdn -o tsv)
echo "Frontend URL: https://$FRONTEND_URL"
```

### Step 4: Set up GitHub Actions Secret

Create a service principal for GitHub Actions:

```bash
az ad sp create-for-rbac \
  --name "lpfc-github-actions" \
  --role contributor \
  --scopes /subscriptions/f75d1a76-d114-4764-814c-c28fa5ab9eed/resourceGroups/LPFC-Resource-Group \
  --sdk-auth
```

The output will be JSON like this:
```json
{
  "clientId": "...",
  "clientSecret": "...",
  "subscriptionId": "...",
  "tenantId": "...",
  ...
}
```

**Add to GitHub:**
1. Go to https://github.com/psaban20/lpfc/settings/secrets/actions
2. Click "New repository secret"
3. Name: `AZURE_CREDENTIALS`
4. Value: Paste the entire JSON output
5. Click "Add secret"

### Step 5: Commit and Push

```bash
git add .
git commit -m "Add Azure deployment configuration"
git push origin master
```

### Step 6: Monitor Deployment

1. Go to https://github.com/psaban20/lpfc/actions
2. Watch the workflow run
3. If tests pass, it will deploy automatically

## How the CI/CD Pipeline Works

### On Every Push to GitHub:

1. **Build and Test Job** runs:
   - Installs Python dependencies
   - Checks backend models load correctly
   - Installs Node.js dependencies
   - Builds frontend (catches TypeScript/compilation errors)

2. **Deploy Job** runs (only if tests pass and on master/main branch):
   - Logs into Azure
   - Builds Docker images
   - Pushes images to ACR
   - Updates Container Apps with new images

### Test Requirements:

**Yes, tests run before deployment!**
- Backend: Validates Python imports and models
- Frontend: Full TypeScript build check

If either fails, deployment is cancelled.

## Database Configuration

Your production containers will use the same database as local dev:
- **Server**: lpfc.database.windows.net
- **Database**: lpfc
- **User**: appuser@lpfc.database.windows.net
- **Password**: Stored securely as Azure Container App secret

## VS Code Extensions (Optional - NOT Required)

Everything can be done via Azure CLI and GitHub Actions. VS Code extensions are optional but helpful:

- **Azure Account**: Sign in to Azure from VS Code
- **Azure Resources**: View/manage Azure resources
- **Docker**: Build and inspect Docker images

You can install these from VS Code Extensions marketplace if desired.

## Monitoring Your Apps

### View Logs:
```bash
# Backend logs
az containerapp logs show --name lpfc-backend-app --resource-group LPFC-Resource-Group --follow

# Frontend logs
az containerapp logs show --name lpfc-frontend-app --resource-group LPFC-Resource-Group --follow
```

### Restart Apps:
```bash
az containerapp revision restart --name lpfc-backend-app --resource-group LPFC-Resource-Group
az containerapp revision restart --name lpfc-frontend-app --resource-group LPFC-Resource-Group
```

### Scale Apps:
```bash
# Set min/max replicas
az containerapp update --name lpfc-backend-app --resource-group LPFC-Resource-Group --min-replicas 1 --max-replicas 3
```

## Cost Estimate

- **ACR (Basic)**: ~$5/month
- **Container Apps**: ~$15-25/month (scales to zero when not used)
- **Total**: ~$20-30/month

Apps scale to zero when not in use, so you only pay for active time.

## Troubleshooting

### If deployment fails:
1. Check GitHub Actions logs for error messages
2. Verify `AZURE_CREDENTIALS` secret is set correctly
3. Check Container App logs: `az containerapp logs show`

### If app shows 503 error:
1. Check logs for startup errors
2. Verify environment variables are set
3. Test database connectivity from Azure

### If database connection fails:
1. Check Azure SQL firewall rules
2. Ensure "Allow Azure services" is enabled
3. Verify credentials are correct

## Quick Reference Commands

```bash
# Check if environment is ready
az containerapp env list --resource-group LPFC-Resource-Group -o table

# View all container apps
az containerapp list --resource-group LPFC-Resource-Group -o table

# Get app URLs
az containerapp show --name lpfc-frontend-app --resource-group LPFC-Resource-Group --query properties.configuration.ingress.fqdn -o tsv
az containerapp show --name lpfc-backend-app --resource-group LPFC-Resource-Group --query properties.configuration.ingress.fqdn -o tsv

# View recent deployments
az containerapp revision list --name lpfc-backend-app --resource-group LPFC-Resource-Group -o table
```

## Summary

**You need VS Code extensions?** NO - everything works via CLI and GitHub Actions.

**Do tests run before deployment?** YES - backend import checks and frontend build.

**Same database for dev and prod?** YES - both connect to lpfc.database.windows.net.

**How does GitHub → Azure work?** Push to GitHub → GitHub Actions builds → Pushes to ACR → Updates Container Apps.

**Next Steps:**
1. Wait for environment creation to complete
2. Run the commands in Step 2 to push images
3. Run the commands in Step 3 to create apps
4. Run Step 4 to configure GitHub Actions
5. Push code and watch it deploy!
