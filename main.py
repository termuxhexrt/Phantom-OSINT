import argparse
from colorama import init, Fore, Style
import sys

# Import modules
from modules.username import check_username
from modules.domain import domain_recon
from modules.phone_email import check_email, check_phone
from modules.metadata import extract_metadata

# Initialize colorama
init(autoreset=True)

def print_banner():
    banner = f"""
{Fore.RED}{Style.BRIGHT}
  _____  _                 _                    ____   _____ _____ _   _ _______ 
 |  __ \| |               | |                  / __ \ / ____|_   _| \ | |__   __|
 | |__) | |__   __ _ _ __ | |_ ___  _ __ ___  | |  | | (___   | | |  \| |  | |   
 |  ___/| '_ \ / _` | '_ \| __/ _ \| '_ ` _ \ | |  | |\___ \  | | | . ` |  | |   
 | |    | | | | (_| | | | | || (_) | | | | | || |__| |____) |_| |_| |\  |  | |   
 |_|    |_| |_|\__,_|_| |_|\__\___/|_| |_| |_| \____/|_____/|_____|_| \_|  |_|   
{Style.RESET_ALL}
{Fore.YELLOW}  >> The Ultimate Open Source Intelligence Framework v1.0 <<
{Style.RESET_ALL}
"""
    print(banner)

def main():
    print_banner()
    
    parser = argparse.ArgumentParser(description="Phantom OSINT - Open Source Intelligence Tool")
    
    parser.add_argument("-u", "--username", help="Target username to hunt across internet")
    parser.add_argument("-d", "--domain", help="Target domain/IP for recon (e.g. example.com)")
    parser.add_argument("-e", "--email", help="Target email address to check")
    parser.add_argument("-p", "--phone", help="Target phone number with country code (e.g. +919000000000)")
    parser.add_argument("-m", "--metadata", help="Path to image/document for metadata extraction")
    
    args = parser.parse_args()

    # If no arguments passed, print help
    if not any(vars(args).values()):
        parser.print_help()
        sys.exit(0)

    try:
        if args.username:
            print(f"\n{Fore.GREEN}[+] Starting Username Recon for: {args.username}{Style.RESET_ALL}")
            check_username(args.username)
            
        if args.domain:
            print(f"\n{Fore.GREEN}[+] Starting Domain Recon for: {args.domain}{Style.RESET_ALL}")
            domain_recon(args.domain)
            
        if args.email:
            print(f"\n{Fore.GREEN}[+] Starting Email Checking for: {args.email}{Style.RESET_ALL}")
            check_email(args.email)
            
        if args.phone:
            print(f"\n{Fore.GREEN}[+] Starting Phone Number Recon for: {args.phone}{Style.RESET_ALL}")
            check_phone(args.phone)
            
        if args.metadata:
            print(f"\n{Fore.GREEN}[+] Starting Metadata Extraction for: {args.metadata}{Style.RESET_ALL}")
            extract_metadata(args.metadata)
            
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Process interrupted by user. Exiting...{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}[!] An error occurred: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
