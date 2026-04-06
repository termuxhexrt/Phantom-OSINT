<h1 align="center">
  <br>
  Phantom OSINT
  <br>
</h1>

<h4 align="center">The Ultimate Open Source Intelligence Framework</h4>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License MIT">
  <img src="https://img.shields.io/badge/Maintained%3F-Yes-orange.svg" alt="Maintained">
  <img src="https://img.shields.io/github/stars/termuxhexrt/Phantom-OSINT?style=flat-square" alt="Stars">
  <img src="https://img.shields.io/badge/OSINT-Framework-red.svg" alt="OSINT">
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#disclaimer">Disclaimer</a>
</p>

---

## 🕵️‍♂️ Overview

**Phantom OSINT** is a fast, stealthy, and modular Information Gathering and Reconnaissance framework designed for Red Teamers, Pentesters, and Cybersecurity Researchers. It passively collects intelligent data from various public sources without tipping off the target.

Zero complex setups, no API keys necessary—just pure, ruthless OSINT.

## 🔥 Features

- **👤 Username Hunter (`-u`)**: Concurrently scans over 100+ social media platforms and websites (GitHub, Twitter, Reddit, Steam, etc.) to hunt down digital footprints.
- **🌐 Domain & IP Recon (`-d`)**: Performs WHOIS lookups, DNS enumeration, IP Geolocation, Certificate Transparency subdomain scanning, HTTP security header analysis, technology fingerprinting, and quick top-25 port scans. 
- **📧 Email Forensics (`-e`)**: Validates email structures, analyzes MX records, checks Gravatar profiles, and generates targeted Google Dorks.
- **📱 Phone Intel (`-p`)**: Decodes phone numbers locally and internationally, identifies carriers, extracts geographical locations, determines timezones, and number types (VoIP vs. Mobile).
- **📂 Metadata Extractor (`-m`)**: Strips EXIF data from images and PDFs, pinpointing hidden GPS coordinates and generating instant Google Maps links.

## 🛠️ Installation

**1. Clone the repository**
```bash
git clone https://github.com/termuxhexrt/Phantom-OSINT.git
cd Phantom-OSINT
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```
*(Dependencies: `requests`, `beautifulsoup4`, `dnspython`, `phonenumbers`, `colorama`, `Pillow`, `python-whois`, `PyPDF2`)*

## 🚀 Usage

Basic Help Menu:
```bash
python main.py -h
```

### Examples
Hunt down a target username:
```bash
python main.py -u johndoe
```

Recon a target domain:
```bash
python main.py -d example.com
```

Analyze an email address:
```bash
python main.py -e target@gmail.com
```

Investigate a phone number (Always use the country code):
```bash
python main.py -p "+14155552671"
```

Extract hidden geolocation data from an image:
```bash
python main.py -m target_photo.jpg
```

**Execute the Ultimate Combo Scan:**
```bash
python main.py -u johndoe -d example.com -e john@gmail.com -p "+14155552671"
```

## ⚠️ Disclaimer

This tool was designed strictly for **educational purposes, responsible research, and authorized penetration testing**. 
The creator and contributors are not responsible for any misuse, illegal activities, or damages caused by this tool. By using Phantom OSINT, you agree that you are using it against systems and targets you have explicit permission to audit. 

**Hack Responsibly.**

---
<p align="center">Made with ❤️ by <a href="https://github.com/termuxhexrt">termuxhexrt</a> </p>
