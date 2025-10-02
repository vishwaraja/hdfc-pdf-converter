# Troubleshooting Guide

## Common Issues and Solutions

### 400 Bad Request Errors

#### Symptoms
- Getting 400 errors when accessing the API
- File upload fails with 400 status
- API returns "No file uploaded" or similar messages

#### Root Causes

The Flask application returns 400 errors in these specific cases:

1. **No file uploaded** (`backend.py:93`)
   ```python
   return jsonify({'error': 'No file uploaded'}), 400
   ```

2. **No file selected** (`backend.py:97`)
   ```python
   return jsonify({'error': 'No file selected'}), 400
   ```

3. **Invalid file type** (`backend.py:100`)
   ```python
   return jsonify({'error': 'Only PDF files are allowed'}), 400
   ```

#### Solutions

1. **Check Request Format**
   - Use `Content-Type: multipart/form-data`
   - Include file in the `file` field
   - Ensure filename is present

   Example with curl:
   ```bash
   curl -X POST https://pdf2csv.in/upload \
     -F "file=@your_statement.pdf"
   ```

2. **Verify File Type**
   - Only PDF files are accepted
   - File must have `.pdf` extension
   - File size must be under 50MB

3. **Check File Field Name**
   The backend expects the file field to be named `file`:
   ```javascript
   const formData = new FormData();
   formData.append('file', pdfFile);  // Must be 'file'
   ```

### Kong/Kubernetes Related Issues

#### Issue: "Kong Helm chart v2.52.0 doesn't support ConfigMap mounting"

**Resolution:** This project **does not use Kong or Kubernetes**. It is deployed on Railway with direct Flask application exposure.

If you see references to Kong issues:
- They do not apply to this project
- The project uses Railway for deployment
- No API gateway layer is currently in use
- See [DEPLOYMENT.md](DEPLOYMENT.md) for architecture details

#### Issue: "Old pod serving traffic without declarative configuration"

**Resolution:** This is not applicable to this project because:
- No Kubernetes pods are used
- Railway handles deployment and traffic routing
- No declarative Kong configuration exists
- Configuration is done through `railway.json` and environment variables

### Converter Not Available Errors

#### Symptoms
- Error: "PDF processing not available"
- Converter shows as unavailable in `/debug` endpoint
- Health check shows `converter_available: false`

#### Solutions

1. **Check Dependencies**
   ```bash
   # Verify all dependencies are installed
   pip install -r web-ui/requirements.txt
   
   # Check specific libraries
   python -c "import camelot; print('Camelot OK')"
   python -c "import pandas; print('Pandas OK')"
   ```

2. **System Dependencies**
   If running locally, ensure system dependencies are installed:
   ```bash
   # On Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install ghostscript libgs-dev
   
   # On macOS
   brew install ghostscript
   ```

3. **Check Debug Endpoint**
   ```bash
   curl https://pdf2csv.in/debug
   ```
   
   Expected response:
   ```json
   {
     "converter_available": true,
     "pandas_available": true,
     "camelot_available": true
   }
   ```

4. **Fallback to Simple Converter**
   If full converter fails, the app falls back to `SimpleHDFCConverter`:
   - Check logs for "Using SimpleHDFCConverter fallback"
   - Simple converter has limited functionality
   - May not extract all transaction details

### Deployment Issues

#### Railway Deployment Fails

**Check Health Endpoint:**
```bash
curl https://pdf2csv.in/health
```

Expected response:
```json
{
  "status": "healthy",
  "converter_available": true,
  "full_converter_available": true,
  "simple_converter_available": true
}
```

**Common Causes:**
1. **Build Failures**
   - Check Railway build logs
   - Verify Dockerfile is correct
   - Ensure all dependencies are in requirements.txt

2. **Health Check Timeout**
   - Railway health check timeout is 100 seconds
   - Large dependencies may take time to load
   - Increase timeout in `railway.json` if needed

3. **Memory Issues**
   - Camelot requires significant memory
   - Check Railway service memory limits
   - Consider upgrading Railway plan if needed

#### Domain Not Working

**Check DNS Configuration:**
```bash
dig pdf2csv.in
nslookup pdf2csv.in
```

**Verify Railway Domain Settings:**
1. Go to Railway dashboard
2. Check custom domain configuration
3. Ensure SSL certificate is active
4. Verify domain is properly linked

### File Processing Errors

#### PDF Extraction Fails

**Symptoms:**
- Upload succeeds but processing fails
- Error: "PDF processing failed"
- Empty or incomplete CSV output

**Solutions:**

1. **Verify PDF Format**
   - Ensure it's an HDFC Bank statement
   - Check if PDF is password-protected
   - Verify PDF is not corrupted

2. **Check PDF Structure**
   ```bash
   # Test locally first
   python src/hdfc_converter.py your_statement.pdf --verbose
   ```

3. **Review Logs**
   - Check Railway logs for detailed errors
   - Look for Camelot extraction errors
   - Verify all pages are processed

#### Large PDF Files

**Issue:** File upload fails or times out

**Solutions:**

1. **Check File Size**
   - Maximum file size: 50MB
   - Configured in `backend.py`: `app.config['MAX_CONTENT_LENGTH']`

2. **Increase Timeout**
   - Local development: Adjust Flask timeout
   - Railway: Processing timeout is handled automatically

3. **Split Large PDFs**
   - If PDF is very large, consider splitting it
   - Process in smaller chunks
   - Combine results afterwards

### Local Development Issues

#### Port Already in Use

**Error:** `Address already in use: 5000`

**Solution:**
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or use a different port
PORT=5001 python web-ui/app.py
```

#### Import Errors

**Error:** `ModuleNotFoundError: No module named 'hdfc_converter'`

**Solution:**
```bash
# Set PYTHONPATH
export PYTHONPATH=/path/to/hdfc-pdf-converter/src:$PYTHONPATH

# Or install as package
pip install -e .
```

### API Gateway / Kong Questions

**Q: Can I add Kong API Gateway to this project?**

**A:** Yes, but it's not necessary for most use cases. Railway provides:
- SSL/TLS termination
- Health checks
- Automatic deployments
- Custom domains

If you need Kong features (rate limiting, advanced routing, etc.):
1. See [DEPLOYMENT.md](DEPLOYMENT.md) for alternatives
2. Consider using Kong with Docker Compose (not Helm)
3. Or use Cloudflare Workers for edge features

**Q: Why aren't you using Kubernetes?**

**A:** Railway provides:
- Simpler deployment process
- Built-in CI/CD
- Automatic SSL
- Lower operational overhead
- Perfect for single-service applications

Kubernetes is excellent for complex, multi-service applications but adds unnecessary complexity for this use case.

**Q: What about the Kong Helm chart v2.52.0 ConfigMap issues?**

**A:** Those issues don't apply to this project because:
- We don't use Kubernetes
- We don't use Helm
- We don't use Kong
- Our deployment is via Railway with direct Flask exposure

If you're trying to deploy this project on Kubernetes with Kong, see the [DEPLOYMENT.md](DEPLOYMENT.md) guide for recommended approaches.

## Getting Help

If you're still experiencing issues:

1. **Check Existing Issues**: [GitHub Issues](https://github.com/vishwaraja/hdfc-pdf-converter/issues)
2. **Create New Issue**: Include:
   - Error message
   - Steps to reproduce
   - Environment (local/Railway)
   - Browser/OS details (for web UI issues)
3. **Email Support**: vishwaraja.pathi@adiyogitech.com
4. **Review Documentation**:
   - [Installation Guide](INSTALLATION.md)
   - [Usage Guide](USAGE.md)
   - [Deployment Guide](DEPLOYMENT.md)
   - [CI/CD Guide](CI_CD_SETUP.md)

## Debug Checklist

When reporting issues, please include:

- [ ] Output of `/debug` endpoint
- [ ] Output of `/health` endpoint
- [ ] Railway logs (if deployed)
- [ ] Browser console errors (for web UI)
- [ ] File size and format
- [ ] Steps to reproduce
- [ ] Expected vs actual behavior
- [ ] Environment details (OS, Python version, etc.)
