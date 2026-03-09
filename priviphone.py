#!/usr/bin/env python3
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from colorama import Fore, Style, init
import urllib.parse
import folium
import os

init(autoreset=True)

# Manual Override Database for Nigerian Mobile Blocks
# This ensures 091/090 prefixes are identified even if the library is old.
NG_CARRIERS = {
    "911": "Airtel Nigeria", "912": "Airtel Nigeria", "901": "Airtel Nigeria", 
    "902": "Airtel Nigeria", "904": "Airtel Nigeria", "907": "Airtel Nigeria",
    "913": "MTN Nigeria", "916": "MTN Nigeria", "903": "MTN Nigeria", 
    "906": "MTN Nigeria", "803": "MTN Nigeria", "806": "MTN Nigeria",
    "909": "9mobile", "908": "9mobile", "809": "9mobile", "817": "9mobile",
    "905": "Globacom", "915": "Globacom", "805": "Globacom", "705": "Globacom"
}

class PriViElite:
    def __init__(self):
        self.banner = (
            f"\n{Fore.CYAN}  ██████╗ ██████╗ ██╗██╗   ██╗██╗███████╗███████╗ ██████╗\n"
            f"{Fore.CYAN}  ██╔══██╗██╔══██╗██║██║   ██║██║██╔════╝██╔════╝██╔════╝\n"
            f"{Fore.CYAN}  ██████╔╝██████╔╝██║██║   ██║██║███████╗█████╗  ██║     \n"
            f"{Fore.CYAN}  ██╔═══╝ ██╔══██╗██║╚██╗ ██╔╝ ██║╚════██║██╔══╝  ██║     \n"
            f"{Fore.CYAN}  ██║     ██║  ██║██║ ╚████╔╝  ██║███████║███████╗╚██████╗\n"
            f"{Fore.RED}  PriViSecurity 🛡️ | ELITE RECON v7.0 | Advanced OSINT Suite\n"
            f"{Fore.YELLOW}  {'=' * 65}\n"
        )

    def generate_intel_map(self, location_name, number):
        print(f"{Fore.YELLOW}[*] Generating Geospatial Intelligence Map...")
        try:
            # Regional Coordinates for Nigeria
            coords = [9.0820, 8.6753] # Default center
            if "Lagos" in location_name: coords = [6.5244, 3.3792]
            elif "Abuja" in location_name: coords = [9.0765, 7.3986]
            
            m = folium.Map(location=coords, zoom_start=10, control_scale=True)
            folium.Marker(
                coords, 
                popup=f"Target: {number}<br>Area: {location_name}", 
                icon=folium.Icon(color='red', icon='screenshot', prefix='fa')
            ).add_to(m)
            
            map_name = "privi_recon_map.html"
            m.save(map_name)
            print(f"{Fore.GREEN}[+] Mapping Complete: {os.path.abspath(map_name)}")
        except Exception as e:
            print(f"{Fore.RED}[!] Map Error: {e}")

    def scan(self, phone_number):
        try:
            parsed = phonenumbers.parse(phone_number, None)
            clean = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
            raw = clean.replace("+", "")
            
            print(self.banner)
            print(f"{Fore.GREEN}[+] DEEP ANALYSIS INITIALIZED: {phone_number}")
            print(f"{Fore.CYAN}{'=' * 45}")

            # 1. Network Intel
            provider = carrier.name_for_number(parsed, "en")
            if not provider and parsed.country_code == 234:
                prefix = str(parsed.national_number)[:3]
                provider = NG_CARRIERS.get(prefix, "Private/Internal Block")

            print(f"{Fore.WHITE}[-] Network Service : {Fore.YELLOW}{provider}")
            print(f"{Fore.WHITE}[-] Node Timezone    : {Fore.YELLOW}{timezone.time_zones_for_number(parsed)}")

            # 2. Digital Footprint (Social Recon)
            print(f"\n{Fore.CYAN}[*] SOCIAL & DIGITAL FOOTPRINT:")
            socials = {
                "WhatsApp": f"https://wa.me/{raw}",
                "LinkedIn": f"https://www.linkedin.com/search/results/all/?keywords={raw}",
                "TrueCaller": f"https://www.truecaller.com/search/global/{raw}",
                "Facebook": f"https://www.facebook.com/search/top/?q={raw}",
                "Instagram": f"https://www.instagram.com/search/?q={raw}",
                "Telegram": f"https://t.me/+{raw}"
            }
            for site, url in socials.items():
                print(f"{Fore.WHITE}{site.ljust(12)}: {Fore.BLUE}{url}")

            # 3. Advanced Dorking (The "Pinpointer")
            print(f"\n{Fore.RED}[!] FORUM RECON (Searching Nairaland/Jiji/LinkedIn):")
            query = f"site:nairaland.com OR site:jiji.ng OR site:linkedin.com \"{raw}\""
            dork_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
            print(f"{Fore.YELLOW}Intelligence Dork: {dork_url}")

            # 4. Map Generation
            location = geocoder.description_for_number(parsed, "en")
            self.generate_intel_map(location if location else "Nigeria", phone_number)

            # 5. Cell Tower Data (Estimated)
            print(f"\n{Fore.MAGENTA}[!] CELL TOWER INTEL (Estimated):")
            print(f"{Fore.WHITE}Primary MCC: {Fore.YELLOW}621 (Nigeria)")
            print(f"{Fore.WHITE}Network MNC: {Fore.YELLOW}Connected to local node")

        except Exception:
            print(f"{Fore.RED}[!] Use international format (e.g., +234...)")

def main():
    scanner = PriViElite()
    target = input(f"{Fore.WHITE}Enter Target Number: ").strip()
    if target: scanner.scan(target)

if __name__ == "__main__":
    main()
            
