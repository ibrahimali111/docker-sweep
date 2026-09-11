# 🧹 docker-sweep

<p align="center">
  <a href="https://github.com/ibrahimali111/docker-sweep/actions/workflows/ci.yml">
    <img src="https://github.com/ibrahimali111/docker-sweep/actions/workflows/ci.yml/badge.svg" alt="CI Status" />
  </a>
  <a href="https://github.com/ibrahimali111/docker-sweep/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT" />
  </a>
  <img src="https://img.shields.io/badge/python-3.8+-3776AB?logo=python&logoColor=white" alt="Python 3.8+" />
  <img src="https://img.shields.io/badge/platform-Linux%20%7C%20macOS-lightgrey" alt="Platform" />
  <img src="https://img.shields.io/badge/zero-dependencies-brightgreen" alt="Zero Dependencies" />
</p>

A smart, safe, interactive CLI utility to analyze Docker disk space and reclaim gigabytes of wasted storage from build cache, dangling images, and dead containers.

---

## ⚡ Why docker-sweep?

Running `docker system prune -a` is dangerous: it deletes running caches, untagged images, and build layers blindly. 

Meanwhile, Docker build caches silently hoard **10GB to 50GB+** of storage on developer machines without you realizing it.

**`docker-sweep`** provides:
- 📊 **Instant Breakdown**: Clear, colorized summary of images, containers, volumes, and build cache.
- 🎯 **Targeted Cleaning**: Clean **only** build cache, **only** dangling images, or everything.
- 🛡️ **Safe Dry-Run Mode**: Preview what would be deleted and how many megabytes/gigabytes will be reclaimed before touching anything.
- ⚡ **Zero Dependencies**: Pure standard library Python. No heavy pip packages required.

---

## 🖥️ Terminal Preview

```text
=======================================================
   🧹 docker-sweep: Docker Disk Space Analyzer         
=======================================================
Docker Engine Version: 29.1.3

TYPE             | TOTAL    | ACTIVE   | SIZE         | RECLAIMABLE
-----------------------------------------------------------------
Images           | 8        | 3        | 4.12GB       | 2.85GB (69%)
Containers       | 4        | 1        | 512MB        | 380MB
Local Volumes    | 6        | 2        | 1.80GB       | 1.10GB
Build Cache      | 34       | 0        | 12.45GB      | 12.45GB (100%)
-----------------------------------------------------------------
```

---

## 🚀 Installation & Quick Start

### Option 1: Run Directly (No Install Needed)
```bash
# Clone the repository
git clone https://github.com/ibrahimali111/docker-sweep.git
cd docker-sweep

# Run immediately
./docker_sweep.py --status
```

### Option 2: Install as a Global CLI Tool
```bash
pip install .
# Now you can use `docker-sweep` anywhere in your terminal!
docker-sweep --status
```

---

## 📖 Command Reference

| Command | Action |
|---|---|
| `docker-sweep` or `docker-sweep -s` | Display Docker disk consumption table |
| `docker-sweep -c` | Prune build cache only *(safest space saver)* |
| `docker-sweep -d` | Remove dangling (untagged) images only |
| `docker-sweep -a` | Interactive full cleanup with confirmation |
| `docker-sweep -c -n` | **Dry run**: Preview what will be pruned without executing |
| `docker-sweep -a -f` | Force clean without confirmation prompts (great for CI/CD) |

---

## 🛡️ License

Distributed under the [MIT License](LICENSE).
