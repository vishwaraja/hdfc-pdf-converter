# Deployment Architecture

## Current Deployment

This project is deployed on **Railway**, a modern cloud platform that provides:
- Automatic deployments from Git
- Built-in health checks
- SSL/TLS termination
- CDN integration
- Simple environment variable management

### Deployment Configuration

The deployment is configured through:
- `railway.json` - Railway-specific configuration
- `Dockerfile` - Container build configuration
- `Procfile` - Process startup configuration

### Railway Configuration

```json
{
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "startCommand": "python web-ui/app.py",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

## API Gateway Considerations

### Kong API Gateway

**Note:** This project does NOT use Kong or Kubernetes at this time. The Kong Helm chart v2.52.0 ConfigMap mounting issues mentioned in some discussions do not apply to this project.

If you're experiencing 400 errors:
1. Check the Flask application logs in Railway dashboard
2. Verify the request format matches API expectations
3. Ensure file uploads don't exceed the 50MB limit

### Current API Architecture

- **Direct Access**: The Flask application is directly exposed via Railway
- **SSL/TLS**: Provided by Railway automatically
- **Domain**: Custom domain `pdf2csv.in` configured in Railway
- **Rate Limiting**: Not currently implemented (could be added if needed)

## Alternative Deployment Options

### If You Need an API Gateway

If you want to add an API gateway layer, consider these alternatives to Kong with Kubernetes:

#### 1. Railway Native Features
- Railway provides SSL, health checks, and automatic scaling
- No additional API gateway needed for most use cases

#### 2. Cloudflare Workers
- Add rate limiting and caching at the edge
- Minimal configuration required
- Works well with Railway backend

#### 3. AWS API Gateway + Railway
- Deploy backend on Railway
- Use AWS API Gateway for advanced features
- No Kubernetes required

#### 4. Kong on Docker (Not Helm)
If you specifically need Kong but want to avoid Kubernetes/Helm issues:
```bash
# Run Kong directly with Docker Compose
docker-compose.yml with Kong and the application
```

### Kubernetes/Helm Deployment

If you want to move to Kubernetes with Kong, you would need to:

1. **Create Kubernetes manifests** (currently not in repository)
2. **Choose a Kong chart version** that properly supports declarative config
3. **Use alternatives to ConfigMap mounting**:
   - Use Kong DB mode instead of DB-less mode
   - Store configuration in Kong's database
   - Use Kong's Admin API to configure routes
   - Consider Kong Gateway Enterprise with RBAC

**Known Issue with Kong Helm Chart v2.52.0:**
- `secretVolumes` - Looks for Secrets, not ConfigMaps
- `extraVolumes/extraVolumeMounts` - Not applied properly
- `customVolumes/customVolumeMounts` - Not applied properly  
- `declarativeConfig` - Not working as expected

**Recommended Solutions if using Kong:**
1. Use Kong Helm chart v2.7+ or v3.x with proper declarativeConfig support
2. Use Kong in DB mode with PostgreSQL instead of DB-less mode
3. Use Kong Ingress Controller instead of declarative config
4. Configure routes via Kong Admin API after deployment

## Health Check Endpoints

The application provides these health check endpoints:

- `GET /health` - Basic health check (returns 200 if app is running)
- `GET /` - API root (returns API status message)
- `GET /debug` - Debug endpoint showing converter availability

## Monitoring and Logs

### Railway Dashboard
- View logs in real-time
- Monitor resource usage
- Check deployment history
- View metrics and analytics

### Application Logs
The Flask application logs:
- Converter availability
- File processing status
- Error details
- Request handling

## Troubleshooting

### 400 Errors

If you're getting 400 errors, check:

1. **File Upload Issues**
   ```python
   # Backend returns 400 if:
   - No file uploaded
   - No file selected
   - File is not a PDF
   - File exceeds 50MB limit
   ```

2. **Request Format**
   - Ensure you're using `multipart/form-data`
   - File field must be named `file`
   - File must have a filename

3. **Railway Logs**
   ```bash
   railway logs --service web
   ```

### Health Check Failures

If health checks fail:
1. Check if converters are loading properly
2. Verify system dependencies in Dockerfile
3. Check memory limits in Railway

## Future Considerations

If the project grows and requires:
- **Advanced Rate Limiting**: Consider Cloudflare or Kong
- **Multiple Microservices**: Consider Kubernetes
- **Geographic Distribution**: Consider multi-region Railway deployments
- **Complex Routing**: Consider API Gateway solutions

For now, Railway provides all the necessary features for this application's requirements.
