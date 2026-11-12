# waybackparams

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)
![Category](https://img.shields.io/badge/recon-passive-orange)

**Passive** URL and parameter harvesting from the Wayback Machine. Pull every URL a domain has ever exposed, extract the unique **parameter names** for fuzzing, or surface only the **interesting files** (`.js`, `.bak`, `.sql`, `.env`, …). The target is never contacted — all data comes from public archives.

## Features
- Wayback CDX harvest with de-duplication
- `--params` → unique parameter names, ranked by frequency
- `--interesting` → only juicy extensions (backups, configs, dumps)
- Frequency summary of top parameters
- Zero dependencies, pipe-friendly

## Install
```bash
git clone https://github.com/anvarsadathk/waybackparams.git
cd waybackparams
python3 waybackparams.py --help
```

## Usage
```bash
# All archived URLs
python3 waybackparams.py example.com -o urls.txt

# Unique params, ready for a fuzzer
python3 waybackparams.py example.com --params -o params.txt

# Hunt for exposed backups / configs
python3 waybackparams.py example.com --interesting
```

Feeds nicely into [reflectx](https://github.com/anvarsadathk/reflectx):
```bash
python3 waybackparams.py example.com -o urls.txt
python3 ../reflectx/reflectx.py -l urls.txt --yes-authorized
```

## ⚠️ Responsible use
Passive recon is low-risk, but act only on domains you own or are authorized to assess, and handle any exposed data responsibly.

## License
MIT © Anvar Sadath K.
