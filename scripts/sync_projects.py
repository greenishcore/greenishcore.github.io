#!/usr/bin/env python3
"""Sync the owner's original GitHub repositories into projects.html.

Runs in the Pages deploy workflow before the site is uploaded, so the
project list is plain HTML on the published site and needs no API call
from the visitor's browser.

"Original" means: owned by the user, not a fork, not archived, not the
Pages repository itself, not generated from a template, and not listed in
EXCLUDE below. The generated block sits between the two marker comments in
projects.html; everything outside the markers is left alone.

If the GitHub API cannot be reached the script leaves projects.html as it
is and exits 0, so a network hiccup never blocks a deploy.

Usage:
  python3 scripts/sync_projects.py                  # fetch from the API
  python3 scripts/sync_projects.py --input repos.json   # offline, for testing
"""

import argparse
import datetime
import html
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request

OWNER = "greenishcore"
PAGES_REPO = f"{OWNER}.github.io"

# Repositories that are not original work although GitHub does not mark
# them as forks. Add a name here to hide it from the site.
EXCLUDE = {
    "github-slideshow",   # GitHub Learning Lab training repository
    "Online-Workshop",    # imported history, pushed before it was created
}

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "projects.html"
START = "<!-- projects:start -->"
END = "<!-- projects:end -->"
INDENT = "      "


def api(url):
    request = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{OWNER}-pages-sync",
    })
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def fetch_repos():
    repos, page = [], 1
    while True:
        batch = api(f"https://api.github.com/users/{OWNER}/repos"
                    f"?type=owner&sort=pushed&per_page=100&page={page}")
        if not isinstance(batch, list):
            raise ValueError(batch.get("message", "unexpected API response"))
        repos.extend(batch)
        if len(batch) < 100:
            return repos
        page += 1


def from_template(repo):
    """The list endpoint omits template_repository, so ask per repository."""
    try:
        detail = api(f"https://api.github.com/repos/{repo['full_name']}")
    except (urllib.error.URLError, TimeoutError, ValueError):
        return False
    return bool(detail.get("template_repository"))


def is_original(repo, check_template):
    return not (
        repo.get("fork")
        or repo.get("archived")
        or repo.get("private")
        or repo["name"] == PAGES_REPO
        or repo["name"] in EXCLUDE
        or (check_template and from_template(repo))
    )


def render(repos, synced):
    e = html.escape
    out = [START, f'{INDENT}<p class="meta">共 {len(repos)} 个项目，'
           f'同步于 <time datetime="{synced}">{synced}</time>。</p>',
           f'{INDENT}<div class="grid">']
    for repo in repos:
        meta = [e(repo["language"])] if repo.get("language") else []
        if repo.get("stargazers_count"):
            meta.append(f"&#9733; {repo['stargazers_count']}")
        if (repo.get("license") or {}).get("spdx_id") not in (None, "NOASSERTION"):
            meta.append(e(repo["license"]["spdx_id"]))
        pushed = repo["pushed_at"][:10]
        meta.append(f'更新于 <time datetime="{pushed}">{pushed}</time>')
        description = e(repo.get("description") or "暂无简介。")
        out += [
            f"{INDENT}  <article class=\"card\">",
            f"{INDENT}    <h3><a href=\"{e(repo['html_url'])}\">{e(repo['name'])}</a></h3>",
            f"{INDENT}    <p>{description}</p>",
            f"{INDENT}    <p class=\"meta\">{' &middot; '.join(meta)}</p>",
            f"{INDENT}  </article>",
        ]
    out += [f"{INDENT}</div>", f"{INDENT}{END}"]
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", help="read repositories from a JSON file")
    args = parser.parse_args()

    try:
        if args.input:
            repos = json.loads(pathlib.Path(args.input).read_text("utf-8"))
        else:
            repos = fetch_repos()
    except (urllib.error.URLError, TimeoutError, ValueError) as error:
        print(f"sync_projects: GitHub API unavailable ({error}); "
              "keeping the existing project list", file=sys.stderr)
        return 0

    originals = [r for r in repos if is_original(r, check_template=not args.input)]
    originals.sort(key=lambda r: r["pushed_at"], reverse=True)

    page = PAGE.read_text("utf-8")
    if START not in page or END not in page:
        print(f"sync_projects: markers missing in {PAGE.name}", file=sys.stderr)
        return 1
    head, _, rest = page.partition(START)
    _, _, tail = rest.partition(END)

    synced = datetime.date.today().isoformat()
    PAGE.write_text(head + render(originals, synced) + tail, "utf-8")
    print(f"sync_projects: {len(originals)} projects written to {PAGE.name}: "
          + ", ".join(r["name"] for r in originals))
    return 0


if __name__ == "__main__":
    sys.exit(main())
