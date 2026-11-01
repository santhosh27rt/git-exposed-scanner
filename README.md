# git-exposed-scanner

> Detect publicly exposed `.git` directories on web servers.

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

A web server that exposes its `.git/` directory can leak source code, configuration, and
secrets. This tool checks a single target or a list of targets for an exposed Git repository
and reports which hosts are affected.

---

## ✨ Features

- Scan a **single target** or a **bulk list** from a file
- Concurrent scanning with a configurable thread count
- Clear, color-coded terminal output
- Export results to **JSON** for reporting or pipelines

## 📦 Installation

```bash
git clone https://github.com/santhosh27rt/git-exposed-scanner.git
cd git-exposed-scanner
pip install -r requirements.txt
```

## 🚀 Usage

```bash
# Single target
python3 git_scanner.py -t https://example.com

# Bulk scan from a file (one target per line)
python3 git_scanner.py -l targets.txt

# Save results to JSON
python3 git_scanner.py -l targets.txt -o results.json

# Adjust threads and timeout
python3 git_scanner.py -l targets.txt --threads 10 --timeout 15 -v
```

### Options

| Flag | Description | Default |
|---|---|---|
| `-t, --target` | Single target URL | — |
| `-l, --list` | File with a list of targets | — |
| `-o, --output` | Write results to a JSON file | — |
| `--timeout` | Request timeout (seconds) | `10` |
| `--threads` | Concurrent threads | `5` |
| `-v, --verbose` | Verbose output | off |

### Input format (`targets.txt`)

```text
https://example.com
http://192.168.1.10
example.org
# Lines starting with # are ignored
```

## 📄 Example output

```text
[*] Loading targets from: targets.txt
[i] Loaded: 3 targets

[🎯] Target: https://example.com
  🔴 Git repository exposed

Secured: 2   Exposed: 1   Duration: 4.12s
```

## ⚠️ Legal & responsible use

This tool is provided for **authorized security testing and educational purposes only**.
Scan only systems for which you have **explicit written permission**. The author assumes no
liability for misuse or for any damage caused by this software.

## 📝 License

Released under the [MIT License](LICENSE).

---

**Author:** Santhosh Manoj Kumar
