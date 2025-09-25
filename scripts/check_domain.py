#!/usr/bin/env python3
"""
Script to check if the custom domain is properly configured
"""
import socket
import time
import sys

def check_domain(domain):
    """Check if domain resolves to Railway"""
    try:
        # Get the IP address
        ip = socket.gethostbyname(domain)
        print(f"✅ Domain {domain} resolves to: {ip}")
        
        # Check if it's a Railway IP (Railway uses specific IP ranges)
        if ip.startswith('76.76.') or ip.startswith('76.223.'):
            print("✅ This appears to be a Railway IP address")
            return True
        else:
            print("⚠️  This doesn't appear to be a Railway IP address")
            return False
            
    except socket.gaierror as e:
        print(f"❌ Domain {domain} not yet configured: {e}")
        return False

def main():
    domain = "pdf2csv.in"
    print(f"Checking domain: {domain}")
    print("=" * 50)
    
    max_attempts = 10
    attempt = 1
    
    while attempt <= max_attempts:
        print(f"\nAttempt {attempt}/{max_attempts}")
        if check_domain(domain):
            print("\n🎉 Domain is ready!")
            print(f"Your HDFC PDF Converter is now available at: https://{domain}")
            break
        else:
            if attempt < max_attempts:
                print("⏳ Waiting 30 seconds before next check...")
                time.sleep(30)
            attempt += 1
    
    if attempt > max_attempts:
        print(f"\n⏰ Domain not ready after {max_attempts} attempts.")
        print("DNS changes can take up to 72 hours to propagate.")
        print("Please check your DNS configuration in GoDaddy.")

if __name__ == "__main__":
    main()
