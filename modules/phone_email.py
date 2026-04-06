import requests
import re
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from colorama import Fore, Style


def check_email(email):
    """Perform reconnaissance on an email address."""
    
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"  EMAIL RECON: {email}")
    print(f"{'='*70}{Style.RESET_ALL}")
    
    # Validate format
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        print(f"\n  {Fore.RED}[!] Invalid email format!{Style.RESET_ALL}")
        return
    
    print(f"\n  {Fore.GREEN}[+] Email format: Valid{Style.RESET_ALL}")
    
    # Extract info from email
    username, domain = email.split("@")
    print(f"  {Fore.WHITE}    Username  : {Fore.GREEN}{username}{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}    Domain    : {Fore.GREEN}{domain}{Style.RESET_ALL}")
    
    # Check MX records
    _check_mx(domain)
    
    # Gravatar check
    _check_gravatar(email)
    
    # Check if email registered on common platforms
    _email_platform_check(email)
    
    # Google dorking suggestions
    _google_dorks_email(email)
    
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"  EMAIL RECON COMPLETE")
    print(f"{'='*70}{Style.RESET_ALL}\n")


def _check_mx(domain):
    """Check MX records for the email domain."""
    print(f"\n  {Fore.YELLOW}[*] MX Record Check{Style.RESET_ALL}")
    print(f"  {'─'*50}")
    
    try:
        import dns.resolver
        answers = dns.resolver.resolve(domain, "MX")
        for rdata in answers:
            print(f"    {Fore.WHITE}MX -> {Fore.GREEN}{rdata.exchange} (Priority: {rdata.preference}){Style.RESET_ALL}")
            
        # Identify email provider
        mx_str = str(answers[0].exchange).lower()
        providers = {
            "google": "Google Workspace / Gmail",
            "outlook": "Microsoft 365 / Outlook",
            "zoho": "Zoho Mail",
            "protonmail": "ProtonMail",
            "icloud": "Apple iCloud",
            "yahoo": "Yahoo Mail",
            "yandex": "Yandex Mail",
            "mailgun": "Mailgun (Transactional)",
            "sendgrid": "SendGrid (Transactional)",
        }
        for key, provider in providers.items():
            if key in mx_str:
                print(f"    {Fore.MAGENTA}    Provider: {provider}{Style.RESET_ALL}")
                break
    except Exception as e:
        print(f"    {Fore.RED}MX lookup failed: {e}{Style.RESET_ALL}")


def _check_gravatar(email):
    """Check if a Gravatar profile exists for this email."""
    print(f"\n  {Fore.YELLOW}[*] Gravatar Check{Style.RESET_ALL}")
    print(f"  {'─'*50}")
    
    import hashlib
    email_hash = hashlib.md5(email.strip().lower().encode()).hexdigest()
    gravatar_url = f"https://www.gravatar.com/{email_hash}.json"
    
    try:
        resp = requests.get(gravatar_url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            entry = data.get("entry", [{}])[0]
            print(f"    {Fore.GREEN}[+] Gravatar profile FOUND!{Style.RESET_ALL}")
            
            if entry.get("displayName"):
                print(f"    {Fore.WHITE}    Display Name : {Fore.GREEN}{entry['displayName']}{Style.RESET_ALL}")
            if entry.get("preferredUsername"):
                print(f"    {Fore.WHITE}    Username     : {Fore.GREEN}{entry['preferredUsername']}{Style.RESET_ALL}")
            if entry.get("aboutMe"):
                print(f"    {Fore.WHITE}    About        : {Fore.GREEN}{entry['aboutMe'][:100]}{Style.RESET_ALL}")
            if entry.get("currentLocation"):
                print(f"    {Fore.WHITE}    Location     : {Fore.GREEN}{entry['currentLocation']}{Style.RESET_ALL}")
                
            # Social accounts
            accounts = entry.get("accounts", [])
            if accounts:
                print(f"    {Fore.YELLOW}    Linked Accounts:{Style.RESET_ALL}")
                for acc in accounts:
                    print(f"      {Fore.GREEN}-> {acc.get('shortname', 'Unknown')}: {acc.get('url', 'N/A')}{Style.RESET_ALL}")
            
            avatar_url = f"https://www.gravatar.com/avatar/{email_hash}?s=400"
            print(f"    {Fore.WHITE}    Avatar URL   : {Fore.CYAN}{avatar_url}{Style.RESET_ALL}")
        else:
            print(f"    {Fore.RED}[-] No Gravatar profile found.{Style.RESET_ALL}")
    except Exception as e:
        print(f"    {Fore.RED}Gravatar check error: {e}{Style.RESET_ALL}")


def _email_platform_check(email):
    """Check common platform registration endpoints."""
    print(f"\n  {Fore.YELLOW}[*] Platform Registration Check{Style.RESET_ALL}")
    print(f"  {'─'*50}")
    
    # These are common endpoints that may reveal if an email is registered
    checks = {
        "GitHub": f"https://api.github.com/search/users?q={email}+in:email",
    }
    
    headers = {"User-Agent": "PhantomOSINT/1.0"}
    
    for platform, url in checks.items():
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("total_count", 0) > 0:
                    items = data.get("items", [])
                    for item in items:
                        print(f"    {Fore.GREEN}[+] {platform}: {item.get('login', 'Unknown')} -> {item.get('html_url', '')}{Style.RESET_ALL}")
                else:
                    print(f"    {Fore.RED}[-] {platform}: Not found{Style.RESET_ALL}")
        except Exception:
            print(f"    {Fore.RED}[-] {platform}: Check failed{Style.RESET_ALL}")


def _google_dorks_email(email):
    """Generate Google dork queries for email OSINT."""
    print(f"\n  {Fore.YELLOW}[*] Google Dork Suggestions{Style.RESET_ALL}")
    print(f"  {'─'*50}")
    
    dorks = [
        f'"{email}"',
        f'"{email}" site:linkedin.com',
        f'"{email}" site:facebook.com',
        f'"{email}" site:twitter.com',
        f'"{email}" filetype:pdf',
        f'"{email}" filetype:doc OR filetype:docx',
        f'"{email}" site:pastebin.com',
        f'"{email}" inurl:contact OR inurl:about',
        f'intext:"{email}" -site:gmail.com',
    ]
    
    for i, dork in enumerate(dorks, 1):
        encoded = requests.utils.requote_uri(dork)
        url = f"https://www.google.com/search?q={encoded}"
        print(f"    {Fore.WHITE}{i}. {Fore.CYAN}{dork}{Style.RESET_ALL}")


def check_phone(phone):
    """Perform reconnaissance on a phone number."""
    
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"  PHONE NUMBER RECON: {phone}")
    print(f"{'='*70}{Style.RESET_ALL}")
    
    try:
        parsed = phonenumbers.parse(phone, None)
    except phonenumbers.NumberParseException as e:
        print(f"\n  {Fore.RED}[!] Invalid phone number: {e}{Style.RESET_ALL}")
        print(f"  {Fore.YELLOW}[*] Make sure to include country code (e.g., +91 for India){Style.RESET_ALL}")
        return
    
    # Validate
    is_valid = phonenumbers.is_valid_number(parsed)
    is_possible = phonenumbers.is_possible_number(parsed)
    
    print(f"\n  {Fore.YELLOW}[*] Phone Number Analysis{Style.RESET_ALL}")
    print(f"  {'─'*50}")
    
    # Format in different formats
    e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    international = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    national = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
    
    print(f"    {Fore.WHITE}{'Valid':<25}: {Fore.GREEN if is_valid else Fore.RED}{is_valid}{Style.RESET_ALL}")
    print(f"    {Fore.WHITE}{'Possible':<25}: {Fore.GREEN if is_possible else Fore.RED}{is_possible}{Style.RESET_ALL}")
    print(f"    {Fore.WHITE}{'E164 Format':<25}: {Fore.GREEN}{e164}{Style.RESET_ALL}")
    print(f"    {Fore.WHITE}{'International':<25}: {Fore.GREEN}{international}{Style.RESET_ALL}")
    print(f"    {Fore.WHITE}{'National':<25}: {Fore.GREEN}{national}{Style.RESET_ALL}")
    print(f"    {Fore.WHITE}{'Country Code':<25}: {Fore.GREEN}+{parsed.country_code}{Style.RESET_ALL}")
    print(f"    {Fore.WHITE}{'National Number':<25}: {Fore.GREEN}{parsed.national_number}{Style.RESET_ALL}")
    
    # Number type
    number_type = phonenumbers.number_type(parsed)
    type_map = {
        0: "Fixed Line",
        1: "Mobile",
        2: "Fixed Line or Mobile",
        3: "Toll Free",
        4: "Premium Rate",
        5: "Shared Cost",
        6: "VoIP",
        7: "Personal Number",
        8: "Pager",
        9: "UAN",
        10: "Voicemail",
        27: "Emergency",
        28: "Short Code",
        29: "Standard Rate",
    }
    type_str = type_map.get(number_type, "Unknown")
    print(f"    {Fore.WHITE}{'Number Type':<25}: {Fore.GREEN}{type_str}{Style.RESET_ALL}")
    
    # Carrier
    carrier_name = carrier.name_for_number(parsed, "en")
    if carrier_name:
        print(f"    {Fore.WHITE}{'Carrier':<25}: {Fore.GREEN}{carrier_name}{Style.RESET_ALL}")
    
    # Geolocation
    location = geocoder.description_for_number(parsed, "en")
    if location:
        print(f"    {Fore.WHITE}{'Location':<25}: {Fore.GREEN}{location}{Style.RESET_ALL}")
    
    # Timezone
    tz_list = timezone.time_zones_for_number(parsed)
    if tz_list:
        print(f"    {Fore.WHITE}{'Timezone(s)':<25}: {Fore.GREEN}{', '.join(tz_list)}{Style.RESET_ALL}")
    
    # Google dorks for phone
    print(f"\n  {Fore.YELLOW}[*] Google Dork Suggestions{Style.RESET_ALL}")
    print(f"  {'─'*50}")
    
    dorks = [
        f'"{phone}"',
        f'"{national}"',
        f'"{phone}" site:facebook.com',
        f'"{phone}" site:linkedin.com',
        f'"{phone}" site:truecaller.com',
        f'intext:"{phone}"',
    ]
    
    for i, dork in enumerate(dorks, 1):
        print(f"    {Fore.WHITE}{i}. {Fore.CYAN}{dork}{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"  PHONE RECON COMPLETE")
    print(f"{'='*70}{Style.RESET_ALL}\n")
