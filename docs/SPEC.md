# awesome-ai-gateway — Project Spec

## Goal

A curated, pain-point-oriented list of AI gateways / LLM proxies that becomes the
default "which AI gateway should I use" reference. Success metric: 400+ GitHub stars,
then listing in `sindresorhus/awesome` (eligible after day 30).

## Principles

1. **Pain-point first, not vendor first.** Sections answer a user need
   (cheapest access, compliance, self-hosting, China ecosystem, MCP/agents),
   not a vendor taxonomy.
2. **The shareable asset is the comparison table + decision tree**, not the link list.
3. **Every automated commit must change real content** (star counts, new releases).
   No timestamp-only commits.
4. **Accuracy over completeness.** Stars are approximate and refreshed daily by CI.
   Dead/stale projects are labeled, not silently kept.

## Repository contract

| Path | Purpose |
|---|---|
| `README.md` | English main list. Star cells wrapped in `<!--s:owner/repo-->…<!--/s-->` markers. |
| `README.zh-CN.md` | Simplified-Chinese mirror, same markers. |
| `data/projects.json` | Repos tracked for the auto-updated "Recent releases" section. |
| `data/releases.json` | Machine-readable output of the last refresh (for agents/consumers). |
| `scripts/update_readme.py` | Stdlib-only updater: refreshes star markers in both READMEs and rewrites the block between `<!-- RELEASES:START -->` / `<!-- RELEASES:END -->`. |
| `scripts/test_update_readme.py` | Unit tests for all pure functions of the updater (required by project rule: interfaces ship with tests). |
| `.github/workflows/daily-update.yml` | Daily cron (02:23 UTC); commits only when content changed. |
| `.github/workflows/ci.yml` | Unit tests (blocking) + awesome-lint (advisory). |

## Update cadence

- **Daily (automated):** star counts, recent releases block, `data/releases.json`.
- **Weekly (human):** new projects, "What's new" curated news, category adjustments.

## Out of scope

- Pricing scraping (link to source pages instead; avoid stale-price liability).
- Gray-area reverse-engineered "free-api" relays (ToS risk — excluded by policy).
