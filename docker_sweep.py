#!/usr/bin/env python3
"""
docker-sweep
Smart, interactive Docker disk cleaner and reclaimable space analyzer.
Reclaim gigabytes of wasted disk space from build cache, dangling images, and stopped containers.
"""

import sys
import subprocess
import argparse
import json
import re

# ANSI Color Codes
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def run_cmd(command, capture=True):
    """Run a shell command and return stdout/stderr."""
    try:
        res = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE if capture else None,
            stderr=subprocess.PIPE if capture else None,
            text=True
        )
        return res.stdout.strip() if capture else ""
    except subprocess.CalledProcessError as e:
        if capture:
            return None
        raise e


def check_docker_available():
    """Verify Docker daemon is installed and running."""
    res = run_cmd("docker info --format '{{.ServerVersion}}'")
    if not res:
        print(f"{RED}[!] Error: Cannot connect to Docker daemon.{RESET}")
        print("Please make sure Docker is installed and running.")
        sys.exit(1)
    return res


def get_docker_disk_usage():
    """Parse `docker system df` output into structured data."""
    output = run_cmd("docker system df --format '{{json .}}'")
    if not output:
        # Fallback to plain text parsing
        return None
        
    items = []
    for line in output.splitlines():
        try:
            items.append(json.loads(line))
        except Exception:
            pass
    return items


def print_banner(version):
    print(f"\n{BOLD}{CYAN}======================================================={RESET}")
    print(f"{BOLD}{CYAN}   🧹 docker-sweep: Docker Disk Space Analyzer         {RESET}")
    print(f"{BOLD}{CYAN}======================================================={RESET}")
    print(f"{DIM}Docker Engine Version: {version}{RESET}\n")


def display_space_summary(items):
    """Render a clean summary table of Docker disk consumption."""
    if not items:
        # If JSON format fails, display native docker system df
        raw = run_cmd("docker system df")
        print(raw)
        return

    print(f"{BOLD}{'TYPE':<16} | {'TOTAL':<8} | {'ACTIVE':<8} | {'SIZE':<12} | {'RECLAIMABLE'}{RESET}")
    print("-" * 65)

    for item in items:
        t = item.get("Type", "Unknown")
        total = item.get("TotalCount", "0")
        active = item.get("ActiveCount", "0")
        size = item.get("Size", "0B")
        reclaim = item.get("Reclaimable", "0B")

        # Highlight significant reclaimable space
        reclaim_colored = f"{YELLOW}{reclaim}{RESET}" if "GB" in reclaim or "MB" in reclaim else reclaim
        print(f"{CYAN}{t:<16}{RESET} | {total:<8} | {active:<8} | {size:<12} | {reclaim_colored}")

    print("-" * 65 + "\n")


def clean_build_cache(dry_run=False):
    """Prune unused Docker build caches."""
    print(f"{BOLD}▶ Cleaning Docker Build Cache...{RESET}")
    if dry_run:
        print(f"{YELLOW}[Dry Run] Would execute: docker builder prune -f{RESET}")
        return
    out = run_cmd("docker builder prune -f")
    print(f"{GREEN}[✓] Build cache pruned.{RESET}")
    if out:
        for line in out.splitlines()[-2:]:
            print(f"    {line}")


def clean_dangling_images(dry_run=False):
    """Remove untagged <none> images."""
    print(f"{BOLD}▶ Removing Dangling / Untagged Images...{RESET}")
    if dry_run:
        print(f"{YELLOW}[Dry Run] Would execute: docker image prune -f{RESET}")
        return
    out = run_cmd("docker image prune -f")
    print(f"{GREEN}[✓] Dangling images removed.{RESET}")
    if out:
        for line in out.splitlines()[-2:]:
            print(f"    {line}")


def clean_stopped_containers(dry_run=False):
    """Remove stopped containers."""
    print(f"{BOLD}▶ Removing Stopped Containers...{RESET}")
    if dry_run:
        print(f"{YELLOW}[Dry Run] Would execute: docker container prune -f{RESET}")
        return
    out = run_cmd("docker container prune -f")
    print(f"{GREEN}[✓] Stopped containers removed.{RESET}")
    if out:
        for line in out.splitlines()[-2:]:
            print(f"    {line}")


def clean_all(dry_run=False, force=False):
    """Perform a full system cleanup."""
    if not force and not dry_run:
        confirm = input(f"{YELLOW}Are you sure you want to prune build cache, stopped containers, and unused networks? [y/N]: {RESET}").strip().lower()
        if confirm != 'y':
            print(f"{CYAN}[*] Operation cancelled.{RESET}")
            return

    clean_build_cache(dry_run)
    clean_stopped_containers(dry_run)
    clean_dangling_images(dry_run)

    print(f"\n{BOLD}{GREEN}✨ Cleanup complete! Run `docker-sweep --status` to view updated space.{RESET}\n")


def main():
    parser = argparse.ArgumentParser(
        description="docker-sweep: Smart, interactive Docker disk cleaner and reclaimable space analyzer."
    )
    parser.add_argument("-s", "--status", action="store_true", help="Display Docker disk usage summary table")
    parser.add_argument("-c", "--cache", action="store_true", help="Clean unused build cache only")
    parser.add_argument("-d", "--dangling", action="store_true", help="Remove untagged / dangling images only")
    parser.add_argument("-a", "--all", action="store_true", help="Clean build cache, stopped containers, and dangling images")
    parser.add_argument("-n", "--dry-run", action="store_true", help="Show what would be cleaned without executing")
    parser.add_argument("-f", "--force", action="store_true", help="Do not prompt for confirmation")

    args = parser.parse_args()

    # If no flags passed, default to --status
    if not any([args.status, args.cache, args.dangling, args.all]):
        args.status = True

    version = check_docker_available()
    print_banner(version)

    items = get_docker_disk_usage()
    display_space_summary(items)

    if args.cache:
        clean_build_cache(dry_run=args.dry_run)
    elif args.dangling:
        clean_dangling_images(dry_run=args.dry_run)
    elif args.all:
        clean_all(dry_run=args.dry_run, force=args.force)


if __name__ == "__main__":
    main()
