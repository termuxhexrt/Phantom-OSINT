import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style
import time

# 100+ sites for username enumeration
SITES = {
    "GitHub": "https://github.com/{}",
    "Twitter/X": "https://x.com/{}",
    "Instagram": "https://www.instagram.com/{}/",
    "Facebook": "https://www.facebook.com/{}",
    "Reddit": "https://www.reddit.com/user/{}/",
    "YouTube": "https://www.youtube.com/@{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "Pinterest": "https://www.pinterest.com/{}/",
    "LinkedIn": "https://www.linkedin.com/in/{}/",
    "Tumblr": "https://{}.tumblr.com",
    "Flickr": "https://www.flickr.com/people/{}/",
    "SoundCloud": "https://soundcloud.com/{}",
    "Spotify": "https://open.spotify.com/user/{}",
    "Medium": "https://medium.com/@{}",
    "DeviantArt": "https://www.deviantart.com/{}",
    "Steam": "https://steamcommunity.com/id/{}/",
    "Twitch": "https://www.twitch.tv/{}",
    "VK": "https://vk.com/{}",
    "About.me": "https://about.me/{}",
    "Keybase": "https://keybase.io/{}",
    "HackerOne": "https://hackerone.com/{}",
    "BugCrowd": "https://bugcrowd.com/{}",
    "GitLab": "https://gitlab.com/{}",
    "Bitbucket": "https://bitbucket.org/{}/",
    "Docker Hub": "https://hub.docker.com/u/{}/",
    "NPM": "https://www.npmjs.com/~{}",
    "PyPI": "https://pypi.org/user/{}/",
    "RubyGems": "https://rubygems.org/profiles/{}",
    "Gravatar": "https://en.gravatar.com/{}",
    "Patreon": "https://www.patreon.com/{}",
    "Ko-fi": "https://ko-fi.com/{}",
    "Buy Me a Coffee": "https://buymeacoffee.com/{}",
    "Dribbble": "https://dribbble.com/{}",
    "Behance": "https://www.behance.net/{}",
    "500px": "https://500px.com/p/{}",
    "Unsplash": "https://unsplash.com/@{}",
    "Pexels": "https://www.pexels.com/@{}/",
    "Vimeo": "https://vimeo.com/{}",
    "Dailymotion": "https://www.dailymotion.com/{}",
    "Mixcloud": "https://www.mixcloud.com/{}/",
    "Bandcamp": "https://{}.bandcamp.com",
    "Last.fm": "https://www.last.fm/user/{}",
    "Goodreads": "https://www.goodreads.com/{}",
    "Letterboxd": "https://letterboxd.com/{}/",
    "MyAnimeList": "https://myanimelist.net/profile/{}",
    "AniList": "https://anilist.co/user/{}/",
    "Roblox": "https://www.roblox.com/user.aspx?username={}",
    "Minecraft": "https://namemc.com/profile/{}",
    "Chess.com": "https://www.chess.com/member/{}",
    "Lichess": "https://lichess.org/@/{}",
    "Replit": "https://replit.com/@{}",
    "CodePen": "https://codepen.io/{}",
    "StackOverflow": "https://stackoverflow.com/users/?tab=Accounts&SearchText={}",
    "HackerRank": "https://www.hackerrank.com/{}",
    "LeetCode": "https://leetcode.com/{}/",
    "Codeforces": "https://codeforces.com/profile/{}",
    "Kaggle": "https://www.kaggle.com/{}",
    "Trello": "https://trello.com/{}",
    "Slack": "https://{}.slack.com",
    "Telegram": "https://t.me/{}",
    "Snapchat": "https://www.snapchat.com/add/{}",
    "Clubhouse": "https://www.clubhouse.com/@{}",
    "Mastodon": "https://mastodon.social/@{}",
    "Threads": "https://www.threads.net/@{}",
    "Quora": "https://www.quora.com/profile/{}",
    "ProductHunt": "https://www.producthunt.com/@{}",
    "HackerNews": "https://news.ycombinator.com/user?id={}",
    "Imgur": "https://imgur.com/user/{}",
    "9GAG": "https://9gag.com/u/{}",
    "DevTo": "https://dev.to/{}",
    "Hashnode": "https://hashnode.com/@{}",
    "Substack": "https://{}.substack.com",
    "WordPress": "https://{}.wordpress.com",
    "Blogger": "https://{}.blogspot.com",
    "Wattpad": "https://www.wattpad.com/user/{}",
    "Archive.org": "https://archive.org/details/@{}",
    "WikiData": "https://www.wikidata.org/wiki/User:{}",
    "Wikipedia": "https://en.wikipedia.org/wiki/User:{}",
    "Fiverr": "https://www.fiverr.com/{}",
    "Freelancer": "https://www.freelancer.com/u/{}",
    "Upwork": "https://www.upwork.com/freelancers/~{}",
    "Etsy": "https://www.etsy.com/shop/{}",
    "Shopify": "https://{}.myshopify.com",
    "eBay": "https://www.ebay.com/usr/{}",
    "CashApp": "https://cash.app/${}",
    "Venmo": "https://venmo.com/{}",
    "Linktree": "https://linktr.ee/{}",
    "Carrd": "https://{}.carrd.co",
    "Notion": "https://notion.so/{}",
    "Gist (GitHub)": "https://gist.github.com/{}",
    "Xbox Gamertag": "https://xboxgamertag.com/search/{}",
    "Duolingo": "https://www.duolingo.com/profile/{}",
    "Scribd": "https://www.scribd.com/{}",
    "SlideShare": "https://www.slideshare.net/{}",
    "Issuu": "https://issuu.com/{}",
    "Disqus": "https://disqus.com/by/{}/",
    "Giphy": "https://giphy.com/{}",
    "IFTTT": "https://ifttt.com/p/{}",
    "Instructables": "https://www.instructables.com/member/{}/",
    "Ask.fm": "https://ask.fm/{}",
    "Foursquare": "https://foursquare.com/{}",
    "Trip Advisor": "https://www.tripadvisor.com/members/{}",
}


def _check_site(site_name, url, username, timeout=10):
    """Check a single site for the username."""
    target_url = url.format(username)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    try:
        resp = requests.get(target_url, headers=headers, timeout=timeout, allow_redirects=True)
        
        # Check for "not found" indicators in the response
        not_found_indicators = [
            "page not found", "404", "not found", "does not exist",
            "user not found", "no user", "doesn't exist", "unavailable",
            "sorry, this page", "this account doesn't exist",
        ]
        
        body_lower = resp.text[:5000].lower() if resp.text else ""
        
        if resp.status_code == 200:
            # Double check - some sites return 200 but with "not found" page
            if any(indicator in body_lower for indicator in not_found_indicators):
                return (site_name, target_url, False)
            return (site_name, target_url, True)
        elif resp.status_code in [301, 302]:
            return (site_name, target_url, True)
        else:
            return (site_name, target_url, False)
            
    except requests.exceptions.Timeout:
        return (site_name, target_url, None)  # None = timeout
    except requests.exceptions.ConnectionError:
        return (site_name, target_url, None)
    except Exception:
        return (site_name, target_url, None)


def check_username(username):
    """Hunt a username across 100+ social media and web platforms."""
    
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"  USERNAME RECON: @{username}")
    print(f"  Scanning {len(SITES)} platforms...")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    found = []
    not_found = []
    errors = []
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=30) as executor:
        futures = {
            executor.submit(_check_site, site, url, username): site
            for site, url in SITES.items()
        }
        
        for future in as_completed(futures):
            site_name, target_url, status = future.result()
            
            if status is True:
                found.append((site_name, target_url))
                print(f"  {Fore.GREEN}[+] FOUND{Style.RESET_ALL}  {site_name}: {target_url}")
            elif status is False:
                not_found.append(site_name)
                # Don't print not found for cleaner output
            else:
                errors.append(site_name)
    
    elapsed = time.time() - start_time
    
    # Summary
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"  SCAN COMPLETE")
    print(f"{'='*70}{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}[+] Found    : {len(found)}{Style.RESET_ALL}")
    print(f"  {Fore.RED}[-] Not Found: {len(not_found)}{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}[?] Errors   : {len(errors)}{Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}[*] Time     : {elapsed:.2f}s{Style.RESET_ALL}")
    
    if found:
        print(f"\n{Fore.YELLOW}  --- FOUND PROFILES ---{Style.RESET_ALL}")
        for i, (site, url) in enumerate(found, 1):
            print(f"  {Fore.WHITE}{i:>3}. {site:<20} -> {url}{Style.RESET_ALL}")
    
    print()
    return found
