import socket
import requests
import dns.resolver
from colorama import Fore, Style
import json
import time


def _whois_lookup(domain):
    """Perform WHOIS lookup using free API."""
    print(f"\n  {Fore.YELLOW}[*] WHOIS Lookup{Style.RESET_ALL}")
    print(f"  {'─'*50}")
    
    try:
        # Use free whois API
        resp = requests.get(f"https://api.api-ninjas.com/v1/whois?domain={domain}", 
                          headers={"User-Agent": "PhantomOSINT/1.0"}, timeout=15)
        
        if resp.status_code == 200:
            data = resp.json()
            if data:
                for key, value in data.items():
                    if value and key not in ["raw"]:
                        if isinstance(value, list):
                            value = ", ".join(str(v) for v in value)
                        print(f"    {Fore.WHITE}{key:<25}: {Fore.GREEN}{value}{Style.RESET_ALL}")
            else:
                print(f"    {Fore.RED}No WHOIS data returned.{Style.RESET_ALL}")
        else:
            # Fallback: try python-whois
            _whois_fallback(domain)
    except Exception as e:
        _whois_fallback(domain)


def _whois_fallback(domain):
    """Fallback WHOIS using python-whois library."""
    try:
        import whois
        w = whois.whois(domain)
        fields = {
            "Domain Name": w.domain_name,
            "Registrar": w.registrar,
            "Creation Date": w.creation_date,
            "Expiration Date": w.expiration_date,
            "Updated Date": w.updated_date,
            "Name Servers": w.name_servers,
            "Status": w.status,
            "Org": w.org,
            "Country": w.country,
            "State": w.state,
            "City": w.city,
        }
        for key, value in fields.items():
            if value:
                if isinstance(value, list):
                    value = ", ".join(str(v) for v in value[:5])
                print(f"    {Fore.WHITE}{key:<25}: {Fore.GREEN}{value}{Style.RESET_ALL}")
    except Exception as e:
        print(f"    {Fore.RED}WHOIS lookup failed: {e}{Style.RESET_ALL}")


def _dns_enum(domain):
    """Enumerate DNS records."""
    print(f"\n  {Fore.YELLOW}[*] DNS Records{Style.RESET_ALL}")
    print(f"  {'─'*50}")
    
    record_types = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA", "SRV", "CAA"]
    
    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            for rdata in answers:
                print(f"    {Fore.WHITE}{rtype:<8} -> {Fore.GREEN}{rdata.to_text()}{Style.RESET_ALL}")
        except dns.resolver.NoAnswer:
            pass
        except dns.resolver.NXDOMAIN:
            print(f"    {Fore.RED}Domain does not exist!{Style.RESET_ALL}")
            return
        except dns.resolver.NoNameservers:
            pass
        except Exception:
            pass


def _ip_geolocation(ip):
    """Get IP geolocation info."""
    print(f"\n  {Fore.YELLOW}[*] IP Geolocation: {ip}{Style.RESET_ALL}")
    print(f"  {'─'*50}")
    
    try:
        resp = requests.get(f"http://ip-api.com/json/{ip}?fields=66846719", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "success":
                fields = {
                    "Country": data.get("country"),
                    "Region": data.get("regionName"),
                    "City": data.get("city"),
                    "ZIP": data.get("zip"),
                    "Latitude": data.get("lat"),
                    "Longitude": data.get("lon"),
                    "Timezone": data.get("timezone"),
                    "ISP": data.get("isp"),
                    "Org": data.get("org"),
                    "AS": data.get("as"),
                    "Hosting": data.get("hosting"),
                    "Proxy": data.get("proxy"),
                    "Mobile": data.get("mobile"),
                }
                for key, value in fields.items():
                    if value is not None:
                        print(f"    {Fore.WHITE}{key:<15}: {Fore.GREEN}{value}{Style.RESET_ALL}")
            else:
                print(f"    {Fore.RED}Geolocation failed for {ip}{Style.RESET_ALL}")
    except Exception as e:
        print(f"    {Fore.RED}Geolocation error: {e}{Style.RESET_ALL}")


def _subdomain_enum(domain):
    """Enumerate subdomains using crt.sh (Certificate Transparency logs)."""
    print(f"\n  {Fore.YELLOW}[*] Subdomain Enumeration (crt.sh){Style.RESET_ALL}")
    print(f"  {'─'*50}")
    
    try:
        resp = requests.get(
            f"https://crt.sh/?q=%.{domain}&output=json",
            headers={"User-Agent": "PhantomOSINT/1.0"},
            timeout=20
        )
        
        if resp.status_code == 200:
            data = resp.json()
            subdomains = set()
            for entry in data:
                name = entry.get("name_value", "")
                for sub in name.split("\n"):
                    sub = sub.strip().lower()
                    if sub and "*" not in sub:
                        subdomains.add(sub)
            
            subdomains = sorted(subdomains)
            
            if subdomains:
                print(f"    {Fore.GREEN}Found {len(subdomains)} unique subdomains:{Style.RESET_ALL}")
                for i, sub in enumerate(subdomains, 1):
                    # Try to resolve the subdomain
                    try:
                        ip = socket.gethostbyname(sub)
                        print(f"    {Fore.WHITE}{i:>4}. {sub:<40} -> {Fore.GREEN}{ip}{Style.RESET_ALL}")
                    except socket.gaierror:
                        print(f"    {Fore.WHITE}{i:>4}. {sub:<40} -> {Fore.RED}(unresolved){Style.RESET_ALL}")
            else:
                print(f"    {Fore.RED}No subdomains found.{Style.RESET_ALL}")
        else:
            print(f"    {Fore.RED}crt.sh returned status {resp.status_code}{Style.RESET_ALL}")
    except Exception as e:
        print(f"    {Fore.RED}Subdomain enumeration error: {e}{Style.RESET_ALL}")


def _http_headers(domain):
    """Analyze HTTP headers for security misconfigurations."""
    print(f"\n  {Fore.YELLOW}[*] HTTP Header Analysis{Style.RESET_ALL}")
    print(f"  {'─'*50}")
    
    try:
        resp = requests.get(f"https://{domain}", 
                          headers={"User-Agent": "PhantomOSINT/1.0"}, 
                          timeout=10, allow_redirects=True)
        
        # Print interesting headers
        interesting = [
            "server", "x-powered-by", "x-frame-options", "x-xss-protection",
            "content-security-policy", "strict-transport-security",
            "x-content-type-options", "access-control-allow-origin",
            "set-cookie", "via", "x-cache", "cf-ray",
        ]
        
        print(f"    {Fore.WHITE}{'Status':<35}: {Fore.GREEN}{resp.status_code}{Style.RESET_ALL}")
        print(f"    {Fore.WHITE}{'Final URL':<35}: {Fore.GREEN}{resp.url}{Style.RESET_ALL}")
        
        for header, value in resp.headers.items():
            if header.lower() in interesting:
                print(f"    {Fore.WHITE}{header:<35}: {Fore.GREEN}{value[:80]}{Style.RESET_ALL}")
        
        # Security header checks
        security_headers = {
            "Strict-Transport-Security": "HSTS",
            "Content-Security-Policy": "CSP",
            "X-Frame-Options": "Clickjacking Protection",
            "X-Content-Type-Options": "MIME Sniffing Protection",
            "X-XSS-Protection": "XSS Filter",
        }
        
        print(f"\n    {Fore.YELLOW}Security Header Status:{Style.RESET_ALL}")
        for header, desc in security_headers.items():
            if header.lower() in [h.lower() for h in resp.headers]:
                print(f"    {Fore.GREEN}  [✓] {desc} ({header}){Style.RESET_ALL}")
            else:
                print(f"    {Fore.RED}  [✗] {desc} ({header}) - MISSING!{Style.RESET_ALL}")
                
    except requests.exceptions.SSLError:
        print(f"    {Fore.RED}SSL Error - Certificate might be invalid!{Style.RESET_ALL}")
    except Exception as e:
        print(f"    {Fore.RED}HTTP header analysis error: {e}{Style.RESET_ALL}")


def _tech_detect(domain):
    """Detect technologies using builtwith-like analysis."""
    print(f"\n  {Fore.YELLOW}[*] Technology Detection{Style.RESET_ALL}")
    print(f"  {'─'*50}")
    
    try:
        resp = requests.get(f"https://{domain}", 
                          headers={"User-Agent": "PhantomOSINT/1.0"},
                          timeout=10, allow_redirects=True)
        body = resp.text.lower()
        headers_lower = {k.lower(): v.lower() for k, v in resp.headers.items()}
        
        techs = []
        
        # Server-side
        server = headers_lower.get("server", "")
        if "nginx" in server: techs.append("Nginx")
        if "apache" in server: techs.append("Apache")
        if "cloudflare" in server or "cf-ray" in headers_lower: techs.append("Cloudflare")
        if "microsoft" in server or "iis" in server: techs.append("IIS")
        
        powered = headers_lower.get("x-powered-by", "")
        if "php" in powered: techs.append("PHP")
        if "asp.net" in powered: techs.append("ASP.NET")
        if "express" in powered: techs.append("Express.js")
        
        # Client-side from HTML
        if "react" in body or "reactdom" in body or "__next" in body: techs.append("React")
        if "vue" in body or "vue.js" in body: techs.append("Vue.js")
        if "angular" in body or "ng-" in body: techs.append("Angular")
        if "jquery" in body: techs.append("jQuery")
        if "bootstrap" in body: techs.append("Bootstrap")
        if "tailwind" in body: techs.append("TailwindCSS")
        if "wordpress" in body or "wp-content" in body: techs.append("WordPress")
        if "shopify" in body: techs.append("Shopify")
        if "wix" in body: techs.append("Wix")
        if "squarespace" in body: techs.append("Squarespace")
        if "next.js" in body or "__next" in body: techs.append("Next.js")
        if "nuxt" in body: techs.append("Nuxt.js")
        if "gatsby" in body: techs.append("Gatsby")
        if "laravel" in body: techs.append("Laravel")
        if "django" in body: techs.append("Django")
        if "google-analytics" in body or "gtag" in body: techs.append("Google Analytics")
        if "googletagmanager" in body: techs.append("Google Tag Manager")
        if "hotjar" in body: techs.append("Hotjar")
        if "recaptcha" in body: techs.append("reCAPTCHA")
        
        if techs:
            techs = sorted(set(techs))
            for tech in techs:
                print(f"    {Fore.GREEN}[+] {tech}{Style.RESET_ALL}")
        else:
            print(f"    {Fore.WHITE}No technologies detected from fingerprinting.{Style.RESET_ALL}")
            
    except Exception as e:
        print(f"    {Fore.RED}Tech detection error: {e}{Style.RESET_ALL}")


def domain_recon(target):
    """Full domain/IP reconnaissance."""
    
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"  DOMAIN / IP RECON: {target}")
    print(f"{'='*70}{Style.RESET_ALL}")
    
    start_time = time.time()
    
    # Resolve domain to IP
    ip = None
    try:
        ip = socket.gethostbyname(target)
        print(f"\n  {Fore.WHITE}Resolved IP: {Fore.GREEN}{ip}{Style.RESET_ALL}")
    except socket.gaierror:
        # Maybe it's an IP already
        try:
            socket.inet_aton(target)
            ip = target
            print(f"\n  {Fore.WHITE}Target is an IP: {Fore.GREEN}{ip}{Style.RESET_ALL}")
        except socket.error:
            print(f"\n  {Fore.RED}Cannot resolve target: {target}{Style.RESET_ALL}")
    
    # Run all recon modules
    _whois_lookup(target)
    _dns_enum(target)
    
    if ip:
        _ip_geolocation(ip)
    
    _subdomain_enum(target)
    _http_headers(target)
    _tech_detect(target)
    
    # Port scan (top ports)
    _port_scan(ip or target)
    
    elapsed = time.time() - start_time
    
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"  DOMAIN RECON COMPLETE - {elapsed:.2f}s")
    print(f"{'='*70}{Style.RESET_ALL}\n")


def _port_scan(target, ports=None):
    """Quick scan of common ports."""
    print(f"\n  {Fore.YELLOW}[*] Port Scan (Top 25 Ports){Style.RESET_ALL}")
    print(f"  {'─'*50}")
    
    if ports is None:
        ports = [
            21, 22, 23, 25, 53, 80, 110, 111, 135, 139,
            143, 443, 445, 993, 995, 1723, 3306, 3389,
            5432, 5900, 8080, 8443, 8888, 9090, 27017
        ]
    
    service_map = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
        53: "DNS", 80: "HTTP", 110: "POP3", 111: "RPC",
        135: "MSRPC", 139: "NetBIOS", 143: "IMAP", 443: "HTTPS",
        445: "SMB", 993: "IMAPS", 995: "POP3S", 1723: "PPTP",
        3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
        5900: "VNC", 8080: "HTTP-Alt", 8443: "HTTPS-Alt",
        8888: "HTTP-Alt2", 9090: "WebSocket", 27017: "MongoDB"
    }
    
    open_ports = []
    
    def scan_port(port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1.5)
            result = sock.connect_ex((target, port))
            sock.close()
            return port, result == 0
        except Exception:
            return port, False
    
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    with ThreadPoolExecutor(max_workers=25) as executor:
        futures = {executor.submit(scan_port, p): p for p in ports}
        for future in as_completed(futures):
            port, is_open = future.result()
            if is_open:
                service = service_map.get(port, "Unknown")
                open_ports.append((port, service))
                print(f"    {Fore.GREEN}[OPEN] Port {port:<6} -> {service}{Style.RESET_ALL}")
    
    if not open_ports:
        print(f"    {Fore.RED}No open ports found (all filtered/closed).{Style.RESET_ALL}")
    else:
        print(f"\n    {Fore.WHITE}Total open ports: {Fore.GREEN}{len(open_ports)}{Style.RESET_ALL}")
