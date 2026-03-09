#!/usr/bin/env python3
import requests
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
from fpdf import FPDF
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

# ─────────────────────────────────────────────
#  BRANDING: PriViSecurity | Developed by Prince Ubebe
# ─────────────────────────────────────────────

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 13)
        self.set_fill_color(20, 20, 20)
        self.set_text_color(255, 255, 255)
        self.cell(0, 12, "  PRI-V-PHONE - ELITE INTELLIGENCE REPORT | PriViSecurity", ln=True, fill=True)
        self.set_text_color(0, 0, 0)
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Page {self.page_no()} | Developed by Prince Ubebe | PriViSecurity", align="C")

    def generate(self, intel, filename):
        self.add_page()
        self.set_font("Arial", "B", 12)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 9, "1. TARGET CORE DATA", ln=True, fill=True)
        self.set_font("Arial", "", 10)
        
        rows = [
            ("E164 Format",    intel["e164"]),
            ("Country",        intel.get("country", "Unknown")),
            ("Carrier",        intel["provider"] or "Unknown"),
            ("Line Type",      intel["line_type"]),
            ("Region/City",    intel.get("location", "Unknown")),
            ("Timezone(s)",    intel.get("tz", "Unknown")),
        ]
        for label, value in rows:
            self.set_font("Arial", "B", 10)
            self.cell(60, 8, f"  {label}:", border="B")
            self.set_font("Arial", "", 10)
            self.cell(0, 8, str(value), border="B", ln=True)

        self.ln(6)
        self.set_font("Arial", "B", 12)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 9, "2. BREACH & LEAK INTELLIGENCE", ln=True, fill=True)
        self.set_fill_color(255, 255, 255)
        self.set_font("Arial", "", 10)
        if intel.get("breach_found"):
            self.set_text_color(200, 0, 0)
            self.multi_cell(0, 7, "  [!] WARNING: NUMBER DETECTED IN PUBLIC DATA LEAKS.")
            self.set_text_color(0, 0, 0)
            self.multi_cell(0, 7, f"  Sources: {intel.get('breach_sources', 'Unknown')}")
        else:
            self.multi_cell(0, 7, "  [+] No direct matches found in DeHashed/Leak databases.")

        self.ln(6)
        self.set_font("Arial", "B", 12)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 9, "3. OSINT FOOTPRINT & SEARCH CORRELATION", ln=True, fill=True)
        self.set_fill_color(255, 255, 255)
        for platform, url in intel["social_results"].items():
            self.set_font("Arial", "B", 9)
            self.cell(35, 7, f"  {platform}:")
            self.set_font("Arial", "", 8)
            self.set_text_color(0, 0, 200)
            self.multi_cell(0, 7, url)
            self.set_text_color(0, 0, 0)

        self.output(filename)

class PriVPhone:
    def __init__(self):
        self.dehashed_key   = "YOUR_DEHASHED_KEY"
        self.dehashed_email = "YOUR_DEHASHED_EMAIL"
        self.banner = (
            f"\n{Fore.CYAN}  ██████╗ ██████╗ ██╗██╗   ██╗███████╗███████╗ ██████╗\n"
            f"{Fore.CYAN}  ██╔══██╗██╔══██╗██║██║   ██║██╔════╝██╔════╝██╔════╝\n"
            f"{Fore.CYAN}  ██████╔╝██████╔╝██║██║   ██║███████╗█████╗  ██║     \n"
            f"{Fore.CYAN}  ██╔═══╝ ██╔══██╗██║╚██╗ ██╔╝╚════██║██╔══╝  ██║     \n"
            f"{Fore.CYAN}  ██║     ██║  ██║██║ ╚████╔╝ ███████║███████╗╚██████╗\n"
            f"{Fore.RED}  PriViSecurity | Developed by Prince Ubebe\n"
            f"{Fore.YELLOW}  {'=' * 58}\n"
        )

    def deep_breach_check(self, target):
        if self.dehashed_key == "YOUR_DEHASHED_KEY":
            return False, "API Key Missing"
        try:
            url = f"https://api.dehashed.com/v2/search?query=phone:{target}"
            headers = {"Accept": "application/json"}
            r = requests.get(url, auth=(self.dehashed_email, self.dehashed_key), headers=headers, timeout=10)
            if r.status_code == 200:
                results = r.json()
                if results.get('total', 0) > 0:
                    sources = list(set(e.get('database_name', 'Unknown') for e in results.get('entries', [])))
                    return True, ", ".join(sources)
        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"    [-] Breach check failed: {e}")
        return False, "None"

    def scan(self, target):
        if not target.startswith("+"):
            print(Fore.RED + "[!] Error: Use international format (+...)")
            return None
        try:
            parsed = phonenumbers.parse(target, None)
        except phonenumbers.NumberParseException as e:
            print(Fore.RED + f"[!] Could not parse number: {e}")
            return None
        if not phonenumbers.is_valid_number(parsed):
            print(Fore.RED + "[!] Invalid number.")
            return None

        print(Fore.YELLOW + f"[*] Running PriViSecurity Deep Analysis on {target}...")
        type_map = {0: "Fixed Line", 1: "Mobile", 2: "Fixed/Mobile", 3: "Toll Free", 4: "Premium", 6: "VoIP", -1: "Unknown"}
        line_type = type_map.get(phonenumbers.number_type(parsed), "Unknown")
        stripped = target.lstrip("+")
        
        data = {
            "e164":     phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164),
            "country":  geocoder.description_for_number(parsed, "en"),
            "provider": carrier.name_for_number(parsed, "en"),
            "tz":       ", ".join(timezone.time_zones_for_number(parsed)),
            "line_type": line_type,
            "location": geocoder.description_for_number(parsed, "en") or "Unknown",
            "social_results": {
                "WhatsApp":   f"https://wa.me/{stripped}",
                "LinkedIn":   f"https://www.linkedin.com/search/results/all/?keywords={target}",
                "Google Dork": f"https://www.google.com/search?q=%22{target}%22",
                "File Dork":  f"https://www.google.com/search?q=filetype:pdf+OR+filetype:xls+%22{target}%22",
            }
        }
        found, sources = self.deep_breach_check(target)
        data["breach_found"], data["breach_sources"] = found, sources
        print(Fore.CYAN + f"    [+] Carrier   : {data['provider'] or 'Unknown'}\n    [+] Line Type : {line_type}\n    [+] Breach    : {'YES' if found else 'No'}")
        return data

def main():
    app = PriVPhone()
    print(app.banner)
    num = input(Fore.GREEN + "Enter Target Number: ").strip()
    if not num: return
    intel = app.scan(num)
    if intel:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"PriV_Elite_{num.lstrip('+')}_{ts}.pdf"
        PDFReport().generate(intel, fname)
        print(Fore.GREEN + f"\n[+] Success! Report saved as {fname}")

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print(Fore.YELLOW + "\n[!] Aborted.")
      
