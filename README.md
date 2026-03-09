# 🛡️ PriVi_EliteScanner v2.0
### Advanced OSINT Phone Reconnaissance Framework
**Developed by [Prince Ubebe](https://github.com/YOUR_GITHUB_USERNAME) | PriViSecurity**



**PriVi_EliteScanner** is a tactical Python-based intelligence tool designed for cybersecurity professionals and OSINT (Open Source Intelligence) investigators. It moves beyond basic metadata by correlating phone numbers with historical data breaches and deep-web document dorks.

---

## 🚀 Key Features

* **Deep Metadata Extraction:** Identifies Country, Carrier, and exact Timezone.
* **Line-Type Intelligence:** Automatically distinguishes between **Mobile, Fixed Line, VoIP, Pager, and Toll-Free** numbers using the `phonenumbers` library.
* **Breach Detection:** Integrated with the **DeHashed API** to identify if a target number has appeared in public data leaks.
* **Social & Web Footprinting:** Automated search correlation for:
    * **WhatsApp:** Direct link generation for profile verification.
    * **LinkedIn:** Search correlation for professional identity.
    * **Google Dorking:** Precise identification of the number in public web spaces.
    * **File Dorking:** Scans the web for `.pdf` or `.xls` files containing the target number.
* **Forensic PDF Reporting:** Generates an automated, clean **Intelligence Dossier** with a timestamp for every scan.

---

## 🛠️ Installation & Setup



### 1. Prerequisites
Ensure you have Python 3.8+ installed on your system.

### 2. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/PriVi_EliteScanner.git](https://github.com/YOUR_USERNAME/PriVi_EliteScanner.git)
cd PriVi_EliteScanner

# PriVi_EliteScanner
Advanced OSINT Phone Reconnaissance Framework by PriViSecurity.
