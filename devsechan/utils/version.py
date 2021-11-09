import subprocess
import platform
from typing import Optional


def gnuify(x: str) -> str:
    return 'GNU/Linux' if x.lower() == 'linux' else x


def git_tag() -> Optional[str]:
    cmd = ['git', 'describe', '--exact-match', '--abbrev=0']
    try:
        res = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        return res.decode('ascii').strip()
    except subprocess.CalledProcessError:
        return None


def git_commit() -> Optional[str]:
    cmd = ['git', 'rev-parse', '--short', 'HEAD']
    try:
        res = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        return res.decode('ascii').strip()
    except subprocess.CalledProcessError:
        return None


def version() -> str:
    tag = git_tag() or ""
    commit = git_commit()
    commit = f"({commit})" if commit else ""

    os_name = gnuify(platform.system())

    return f"DevSE-Chan {tag}{commit} on {os_name}"
