#!/usr/bin/env python3
"""
Script to check domain propagation status
"""
import socket
import time
import sys

def check_domain_resolution(domain):
    """Check if domain resolves"""
    try:
        ip = socket.gethostbyname(domain)
        return ip, True
    except socket.gaierror:
        return None, False

def main():
    domain = "pdf2csv.in"
    railway_ip = "66.33.22.66"
    
    print(f"🔍 Checking domain: {domain}")
    print(f"🎯 Expected Railway IP: {railway_ip}")
    print("=" * 60)
    
    max_attempts = 20
    attempt = 1
    
    while attempt <= max_attempts:
        print(f"\n⏰ Attempt {attempt}/{max_attempts} - {time.strftime('%H:%M:%S')}")
        
        ip, resolved = check_domain_resolution(domain)
        
        if resolved:
            print(f"✅ Domain resolved to: {ip}")
            if ip == railway_ip:
                print("🎉 SUCCESS! Domain is pointing to Railway!")
                print(f"🌐 Your HDFC PDF Converter is now live at: https://{domain}")
                break
            else:
                print(f"⚠️  Domain resolved but to different IP: {ip}")
                print(f"   Expected: {railway_ip}")
        else:
            print("⏳ Domain not yet resolved...")
        
        if attempt < max_attempts:
            print("   Waiting 30 seconds...")
            time.sleep(30)
        
        attempt += 1
    
    if attempt > max_attempts:
        print(f"\n⏰ Domain not ready after {max_attempts} attempts.")
        print("📋 Your DNS configuration looks correct:")
        print("   - A record: @ → 66.33.22.66")
        print("   - CNAME record: www → am9l4aga.up.railway.app")
        print("\n💡 DNS propagation can take up to 72 hours.")
        print("   Try checking again in a few hours.")

if __name__ == "__main__":
    main()
