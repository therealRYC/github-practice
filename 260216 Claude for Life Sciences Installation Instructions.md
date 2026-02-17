# 260216 Claude for Life Sciences Installation Instructions

Complete guide to installing and configuring MCP (Model Context Protocol) servers for life sciences research in Claude Code. This setup provides Claude with access to 23 biomedical databases, literature search engines, and bioinformatics tools.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Architecture Overview](#2-architecture-overview)
3. [Tier 1: Remote HTTP Servers (No Auth)](#3-tier-1-remote-http-servers-no-auth)
4. [Tier 2: Remote HTTP Servers (Auth Required)](#4-tier-2-remote-http-servers-auth-required)
5. [Tier 3: Augmented Nature Servers (Node.js / stdio)](#5-tier-3-augmented-nature-servers-nodejs--stdio)
6. [Tier 4: Python-based Community Servers](#6-tier-4-python-based-community-servers)
7. [Tier 5: Holy Bio MCP Servers (uvx)](#7-tier-5-holy-bio-mcp-servers-uvx)
8. [Tier 6: npm-based Community Servers](#8-tier-6-npm-based-community-servers)
9. [Literature Search Strategy](#9-literature-search-strategy)
10. [Accessing Paywalled Papers](#10-accessing-paywalled-papers)
11. [Verification](#11-verification)
12. [Troubleshooting](#12-troubleshooting)
13. [Server Reference Table](#13-server-reference-table)
14. [Changelog](#14-changelog)

---

## 1. Prerequisites

### System Requirements
- **Claude Code** v2.1.42+ installed (`claude --version`)
- **Node.js** v20+ (`node --version`)
- **Python** 3.12+ (`python3 --version`)
- **uv/uvx** package manager (`uvx --version`) — install via `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **npm/npx** (comes with Node.js)
- **pip** (comes with Python)

### Important Notes
- All `claude mcp add` commands must be run **outside** of a Claude Code session (you cannot nest Claude inside Claude). If you get "Error: Claude Code cannot be launched inside another Claude Code session", prefix with `CLAUDECODE= ` to bypass.
- All servers are added to the **project-scoped** config for `~/` (your home directory). When you launch Claude Code from `~`, all servers are available.
- Config is stored in `~/.claude.json` under `projects["/home/<user>"].mcpServers`.
- There is **no** `anthropics/life-sciences` plugin marketplace. The official plugin marketplace (`anthropics/claude-plugins-official`) contains dev tools only (LSP servers, code review, etc.). All life sciences MCP servers use the `claude mcp add` approach described here.

---

## 2. Architecture Overview

MCP servers come in two transport types:

- **HTTP** — Remote servers hosted by third parties. Claude Code connects over HTTPS. Some require OAuth authentication (currently broken in Claude Code — see Section 4).
- **stdio** — Local servers that run as subprocesses. Claude Code launches the process and communicates over stdin/stdout. These are the most reliable and should be preferred when available.

```
Claude Code
├── HTTP Servers (remote)
│   ├── DeepSense.ai → biorxiv, chembl, clinical-trials
│   ├── Anthropic → pubmed (unreliable — see Section 9)
│   ├── BioContextAI → biocontext (FastMCP)
│   ├── BioRender → biorender (OAuth broken)
│   ├── Synapse.org → synapse (OAuth broken)
│   ├── Scholar Gateway → scholar-gateway (OAuth broken)
│   ├── Owkin → owkin (OAuth broken)
│   └── Medidata → medidata (OAuth broken)
├── stdio Servers (local) — MOST RELIABLE
│   ├── Python/uvx → biocontext-local, biomcp, tooluniverse, paper-search, protocols-io
│   ├── Node.js → uniprot, alphafold, pdb, reactome-an
│   ├── uvx (holy-bio-mcp) → biothings, gget, opengenes, synergy-age
│   └── npx → enrichr
```

---

## 3. Tier 1: Remote HTTP Servers (No Auth)

These are hosted MCP endpoints that require no authentication. Claude Code connects directly.

### BioRxiv / medRxiv (DeepSense.ai)
Preprint search and metadata from bioRxiv and medRxiv.
```bash
claude mcp add --transport http biorxiv https://mcp.deepsense.ai/biorxiv/mcp
```

### ChEMBL (DeepSense.ai)
Bioactive molecules database — compound search, bioactivity, drug mechanisms.
```bash
claude mcp add --transport http chembl https://mcp.deepsense.ai/chembl/mcp
```

### ClinicalTrials.gov (DeepSense.ai)
Clinical trial registry — search trials, sponsors, investigators, endpoints.
```bash
claude mcp add --transport http clinical-trials https://mcp.deepsense.ai/clinical_trials/mcp
```

### PubMed (Anthropic-hosted)
PubMed literature search.
```bash
claude mcp add --transport http pubmed https://pubmed.mcp.claude.com/mcp
```
> **Warning:** This Anthropic-hosted endpoint is frequently rate-limited (HTTP 429) or fails to connect entirely. **Do not rely on this as your only PubMed/literature search tool.** See [Section 9: Literature Search Strategy](#9-literature-search-strategy) for reliable alternatives that are already installed. See [Section 10: Accessing Paywalled Papers](#10-accessing-paywalled-papers) for full-text access options.

### BioContext Remote (FastMCP)
BioContextAI knowledge base — remote version of biocontext-local.
```bash
claude mcp add --transport http biocontext https://biocontext-kb.fastmcp.app/mcp/
```
> **Note:** The original URL `mcp.biocontext.ai/mcp/` redirects to `biocontext-kb.fastmcp.app/mcp/`. Use the direct URL above. If you have the old URL configured, update it (see Troubleshooting).

---

## 4. Tier 2: Remote HTTP Servers (Auth Required)

These servers require OAuth authentication. All 5 servers correctly advertise OAuth support via `WWW-Authenticate` headers per the MCP spec (RFC 9728). However, **Claude Code has known bugs that prevent the OAuth flow from triggering:**

- [Issue #11814](https://github.com/anthropics/claude-code/issues/11814) — OAuth discovery fails with infinite `about:blank` loop
- [Issue #7290](https://github.com/anthropics/claude-code/issues/7290) — HTTP transport ignores authentication headers
- [Issue #2831](https://github.com/anthropics/claude-code/issues/2831) — Authentication header regression

**Status (as of 2026-02-17):** These servers are configured correctly but non-functional until Anthropic fixes the OAuth implementation. They will show "Needs authentication" or "Failed to connect" in `claude mcp list`. Keep them configured so they start working automatically once the bug is resolved.

### BioRender
Scientific illustration platform.
```bash
claude mcp add --transport http biorender https://mcp.services.biorender.com/mcp
```
> Requires a free BioRender account. OAuth is currently broken in Claude Code.

### Synapse.org
Sage Bionetworks data sharing platform.
```bash
claude mcp add --transport http synapse https://mcp.synapse.org/mcp
```
> Requires a free Synapse.org account. OAuth is currently broken in Claude Code.

### Scholar Gateway (Wiley)
Academic literature access via Wiley.
```bash
claude mcp add --transport http scholar-gateway https://connector.scholargateway.ai/mcp
```
> Requires a free Scholar Gateway account. OAuth is currently broken in Claude Code.

### Owkin
Pathology AI and multimodal research platform.
```bash
claude mcp add --transport http owkin https://mcp.k.owkin.com/mcp
```
> Requires Owkin account. OAuth is currently broken in Claude Code. When working, expired tokens require a fresh session to re-authenticate.

### Medidata
Clinical data management platform (Medidata Rave).
```bash
claude mcp add --transport http medidata https://mcp.imedidata.com/mcp
```
> Requires Medidata account. OAuth is currently broken in Claude Code.

---

## 5. Tier 3: Augmented Nature Servers (Node.js / stdio)

These are locally-run Node.js MCP servers from [Augmented Nature](https://augmentednature.ai). They must be cloned from GitHub and built from TypeScript source.

### Setup (all four servers)

```bash
# Create directory for MCP servers
mkdir -p ~/mcp-servers && cd ~/mcp-servers

# Clone all four repositories
git clone https://github.com/augmented-nature/augmented-nature-uniprot-mcp-server.git Augmented-Nature-UniProt-MCP-Server
git clone https://github.com/augmented-nature/alphafold-mcp-server.git AlphaFold-MCP-Server
git clone https://github.com/augmented-nature/pdb-mcp-server.git PDB-MCP-Server
git clone https://github.com/augmented-nature/reactome-mcp-server.git Reactome-MCP-Server

# Install dependencies and build each server
for dir in Augmented-Nature-UniProt-MCP-Server AlphaFold-MCP-Server PDB-MCP-Server Reactome-MCP-Server; do
  cd ~/mcp-servers/$dir
  npm install
  npx tsc
  chmod 755 build/index.js
done
```

### Register each server

```bash
# UniProt — protein sequences, functions, domains, interactions
claude mcp add --transport stdio uniprot -- node ~/mcp-servers/Augmented-Nature-UniProt-MCP-Server/build/index.js

# AlphaFold — predicted protein structures
claude mcp add --transport stdio alphafold -- node ~/mcp-servers/AlphaFold-MCP-Server/build/index.js

# PDB — experimental protein/nucleic acid structures
claude mcp add --transport stdio pdb -- node ~/mcp-servers/PDB-MCP-Server/build/index.js

# Reactome — biological pathways and reactions
claude mcp add --transport stdio reactome-an -- node ~/mcp-servers/Reactome-MCP-Server/build/index.js
```

### Troubleshooting: "Failed to connect" for Reactome (or others)
If any of these servers fail, the most common cause is a missing `build/` directory. The repos ship without pre-built JavaScript — you must compile the TypeScript:
```bash
cd ~/mcp-servers/Reactome-MCP-Server  # (or whichever server)
npm install   # ensure dependencies are present
npx tsc       # compile TypeScript → build/index.js
chmod 755 build/index.js
```
Then restart Claude Code. This was the exact fix applied to `reactome-an` on 2026-02-16.

---

## 6. Tier 4: Python-based Community Servers

### BioContext Local (uvx)
Full BioContextAI knowledge base running locally. Provides access to UniProt, STRING, Human Protein Atlas, Ensembl, OpenTargets, KEGG, and many more.
```bash
claude mcp add --transport stdio biocontext-local -e UV_PYTHON=3.12 -- uvx biocontext_kb@latest
```
> Uses `uvx` to run the latest version automatically. The `UV_PYTHON=3.12` env var ensures Python 3.12 compatibility.

### BioMCP (GenomOncology)
Biomedical MCP server — PubMed article search, genes, diseases, drugs, variants, clinical trials, FDA data. **This is one of the most reliable ways to search PubMed** since it runs locally via stdio (see Section 9).
```bash
pip install biomcp-python
claude mcp add --transport stdio biomcp -- biomcp run
```

### ToolUniverse
Massive collection of 1400+ bioinformatics tools via a single MCP interface.
```bash
pip install tooluniverse
claude mcp add --transport stdio tooluniverse -- tooluniverse-smcp-stdio --compact-mode
```
> Some tools require additional API keys (HF_TOKEN, OMIM_API_KEY, etc.). The server will warn about missing keys on startup but works without them for most tools.

### Paper Search
Multi-platform academic paper search — arXiv, PubMed, bioRxiv, medRxiv, Google Scholar. **This is the best general-purpose literature search tool** because it queries multiple platforms simultaneously (see Section 9).
```bash
pip install paper-search-mcp
claude mcp add --transport stdio paper-search -- python3 -c "from paper_search_mcp.server import mcp; mcp.run()"
```

### Protocols.io
Search and access laboratory protocols from protocols.io.
```bash
pip install protocols-io-mcp
claude mcp add -e PROTOCOLS_IO_CLIENT_ACCESS_TOKEN=your_token_here --transport stdio protocols-io -- protocols-io-mcp
```
> **Requires a Client Access Token** (not the client ID or client secret — those are only for the HTTP/SSE transport mode).
> 1. Create a free account at [protocols.io](https://www.protocols.io)
> 2. Go to https://www.protocols.io/developers
> 3. Navigate to "API Clients" and create a new application
> 4. Copy the generated **Client Access Token**
> 5. Use it in the `-e` flag above when adding the server
>
> If you already added it without the token:
> ```bash
> claude mcp remove protocols-io
> claude mcp add -e PROTOCOLS_IO_CLIENT_ACCESS_TOKEN=your_token_here --transport stdio protocols-io -- protocols-io-mcp
> ```

---

## 7. Tier 5: Holy Bio MCP Servers (uvx)

These come from the [holy-bio-mcp](https://github.com/longevity-genie/holy-bio-mcp) project — a collection of bioinformatics MCP servers from the Bio x AI Hackathon 2025. All use `uvx` for zero-install execution.

### BioThings
Access to MyGene.info, MyVariant.info, MyChem.info APIs — gene annotations, variant data, chemical/drug info.
```bash
claude mcp add --transport stdio biothings -- uvx --from biothings-mcp stdio
```

### gget
Genomics toolkit — gene/transcript info, sequences, BLAST, enrichment analysis, protein structures.
```bash
claude mcp add --transport stdio gget -- uvx gget-mcp stdio
```

### OpenGenes
Longevity and aging genetics database — genes associated with aging, lifespan data.
```bash
claude mcp add -e MCP_TRANSPORT=stdio --transport stdio opengenes -- uvx opengenes-mcp
```

### SynergyAge
Database of drug synergies and combinations in aging research.
```bash
claude mcp add -e MCP_TRANSPORT=stdio --transport stdio synergy-age -- uvx synergy-age-mcp
```

### Pharmacology (NOT INSTALLED — upstream bug)
```bash
# DO NOT INSTALL — has a bug in _lifespan attribute as of 2026-02-16
# claude mcp add --transport stdio pharmacology -- uvx --from pharmacology-mcp stdio
```
> This server crashes on startup due to a bug in the upstream code (`AttributeError: 'str' object has no attribute '_lifespan'`). Monitor the [holy-bio-mcp repository](https://github.com/longevity-genie/holy-bio-mcp) for fixes.

---

## 8. Tier 6: npm-based Community Servers

### Enrichr
Gene set enrichment analysis using Enrichr libraries (Ma'ayan Lab).
```bash
claude mcp add --transport stdio enrichr -- npx enrichr-mcp-server -l pop
```
> The `-l pop` flag loads a curated set of popular Enrichr gene set libraries. First run will download the npm package (~30 seconds).

---

## 9. Literature Search Strategy

The Anthropic-hosted PubMed connector (`pubmed.mcp.claude.com`) is **unreliable** — it frequently returns HTTP 429 (rate limit) or fails to connect entirely. Do not depend on it as your sole literature search tool.

### Redundant coverage: 6 ways to search the literature

Even when PubMed is down, you have **5 other working connectors** that provide overlapping literature search coverage:

| Tool | Searches | Transport | Reliability |
|------|----------|-----------|-------------|
| **`paper-search`** | arXiv, PubMed, bioRxiv, medRxiv, Google Scholar | stdio (local) | **Best overall** — queries 5 platforms simultaneously |
| **`biomcp`** | PubMed (via `article_searcher` / `article_getter`) | stdio (local) | **Best for PubMed specifically** — reliable local client with full abstract retrieval |
| **`biorxiv`** | bioRxiv, medRxiv preprints | HTTP | Stable (DeepSense.ai hosted) |
| **`biocontext-local`** | Europe PMC (via `bc_get_europepmc_articles` / `bc_get_europepmc_fulltext`) | stdio (local) | Reliable — also provides full-text access |
| **`pubmed`** | PubMed | HTTP (Anthropic) | **Unreliable** — frequently rate-limited or down |
| Claude's built-in `WebSearch` | Google/web results | Built-in | Always available as a fallback |

### Recommended approach for literature searches

1. **Use `paper-search` first** — it's the most versatile, searching arXiv, PubMed, bioRxiv, medRxiv, and Google Scholar in one query. Key tools:
   - `search_arxiv` — arXiv papers
   - `search_pubmed` — PubMed articles
   - `search_biorxiv` — bioRxiv preprints
   - `search_medrxiv` — medRxiv preprints
   - `search_google_scholar` — Google Scholar results

2. **Use `biomcp` for deep PubMed queries** — it has the most robust PubMed integration with full article metadata. Key tools:
   - `article_searcher` — search PubMed with structured queries
   - `article_getter` — fetch full article details by PMID/DOI

3. **Use `biocontext-local` for Europe PMC** — provides access to European literature including full-text where available. Key tools:
   - `bc_get_europepmc_articles` — search Europe PMC
   - `bc_get_europepmc_fulltext` — retrieve full text
   - `bc_search_google_scholar_publications` — Google Scholar via BioContext

4. **Use `biorxiv` for preprints** — dedicated preprint search with metadata. Key tools:
   - `search_preprints` — search by keyword, author, date
   - `get_preprint` — get full preprint details by DOI
   - `search_published_preprints` — find preprints that have been peer-reviewed

5. **Fall back to `WebSearch`** — Claude's built-in web search always works and can find papers, though with less structured metadata.

### The PubMed connector is optional

Given the coverage above, the `pubmed` HTTP connector is effectively redundant. If it continues to fail, you can safely remove it:
```bash
claude mcp remove pubmed
```
You will still have PubMed access through `paper-search` (`search_pubmed`), `biomcp` (`article_searcher`), and `biocontext-local` (`bc_get_europepmc_articles`).

---

## 10. Accessing Paywalled Papers

The tools in Section 9 can **search** for papers and retrieve abstracts, but most cannot access full-text content behind journal paywalls. This section covers options for getting full-text access, including tools that work with institutional subscriptions (e.g., University of Washington).

### Current limitation

No MCP server natively supports institutional proxy authentication (EZproxy, Shibboleth/SAML, OpenAthens). This is a significant gap in the ecosystem as of 2026-02-17. The workarounds below range from easy (open-access only) to comprehensive (full institutional access).

### What already works: open-access full text

These installed servers can retrieve full text for **open-access** papers without any additional setup:

| Server | Tool | What it accesses |
|--------|------|-----------------|
| `paper-search` | `download_arxiv`, `read_arxiv_paper` | arXiv PDFs (always open access) |
| `paper-search` | `download_biorxiv`, `read_biorxiv_paper` | bioRxiv PDFs (always open access) |
| `paper-search` | `download_medrxiv`, `read_medrxiv_paper` | medRxiv PDFs (always open access) |
| `biocontext-local` | `bc_get_europepmc_fulltext` | Europe PMC open-access full text |

> **Note:** `download_pubmed` and `read_pubmed_paper` are stubs — they return a message saying direct download is not supported. PubMed papers must be accessed through other means.

### Option 1: Unpaywall MCP (NOT INSTALLED — easy setup)

[unpaywall-mcp](https://github.com/ElliotPadfield/unpaywall-mcp) finds free, legal open-access versions of paywalled papers using the Unpaywall database. Covers ~30-40% of the scholarly literature through green and gold open access routes.

```bash
pip install unpaywall-mcp  # or: npm install unpaywall-mcp
claude mcp add --transport stdio unpaywall -e UNPAYWALL_EMAIL=robchen@uw.edu -- npx unpaywall-mcp
```

**Tools provided:**
- `unpaywall_search_titles` — search for articles by title
- `unpaywall_get_by_doi` — look up open-access status by DOI
- `unpaywall_get_fulltext_links` — get the best open-access PDF URL
- `unpaywall_fetch_pdf_text` — download and extract text from the OA PDF

**Limitations:** Only finds open-access versions. If no OA version exists, it can't help. 20,000 character default text truncation.

### Option 2: Zotero MCP (NOT INSTALLED — best for institutional access)

[zotero-mcp](https://github.com/54yyyu/zotero-mcp) connects Claude to your Zotero library. This is the **best current path for accessing paywalled papers** through institutional subscriptions because Zotero natively supports EZproxy and institutional proxy authentication.

**Workflow:**
1. Configure your university proxy in Zotero (Preferences > Advanced > Proxies > add `proxy.lib.uw.edu`)
2. Save papers to Zotero through your browser — Zotero downloads the PDF using your UW institutional access
3. Zotero MCP gives Claude access to search, read, and analyze all papers in your library

```bash
pip install zotero-mcp
claude mcp add --transport stdio zotero -- uvx zotero-mcp
```

**Tools provided:**
- Semantic search across your entire Zotero library
- PDF annotation extraction
- Full-text access to any paper you've saved

**Requirements:** Zotero desktop app installed, Zotero account with API key (Settings > Feeds/API > create key).

**Why this is the best option:** Zotero handles the authentication with your UW library subscriptions. Claude then reads the locally-stored PDFs through the MCP server. This is a two-step process but gives full access to anything your institution subscribes to.

### Option 3: Browser automation MCP (NOT INSTALLED — most powerful, most complex)

[BrowserMCP](https://github.com/BrowserMCP/mcp) uses your actual Chrome browser session, including any active logins. You authenticate to UW Libraries once, and Claude can fetch pages through your authenticated session.

**How it works:**
1. Install the BrowserMCP Chrome extension and MCP server
2. Log into UW Libraries / EZproxy in Chrome
3. Claude can access any page your browser session can access, including paywalled journals

**Trade-offs:** Most powerful approach (full access to anything you're logged into), but heavier setup, requires Chrome running, and sessions expire.

### Option 4: Additional paper search servers (NOT INSTALLED)

These provide broader search coverage and may find open-access full text through multi-source fallback:

- **[Scientific-Papers-MCP](https://github.com/benedict2310/Scientific-Papers-MCP)** — searches 200M+ papers across arXiv, OpenAlex, PMC, Europe PMC, bioRxiv, and CORE with full-text extraction for open-access content
- **[paper-search-mcp-nodejs](https://github.com/Dianel555/paper-search-mcp-nodejs)** — supports 14 platforms including Web of Science and Scopus (requires API keys: `WOS_API_KEY`, `SPRINGER_API_KEY`, etc.)
- **[OpenAlex MCP servers](https://github.com/oksure/openalex-research-mcp)** — 240M+ scholarly works, fully open, no API key required
- **[Semantic Scholar MCP](https://github.com/JackKuo666/semanticscholar-MCP-Server)** — paper search with citation analysis, optional API key for higher rate limits

### Recommended approach for paywalled papers

Until an MCP server supports institutional SSO natively, the practical workflow is:

1. **Claude searches** for papers using `paper-search`, `biomcp`, or `biorxiv`
2. **You download** the PDFs yourself through UW Libraries (using your SSO at lib.uw.edu or publisher sites)
3. **Drop the PDF into the conversation** (drag-and-drop or paste the file path) and Claude reads and analyzes it

Installing **Unpaywall MCP** (Option 1) and **Zotero MCP** (Option 2) automates much of this — Unpaywall finds free versions automatically, and Zotero gives Claude access to your full institutional library.

---

## 11. Verification

### Check all server health
```bash
claude mcp list
```
This runs a fresh health check against every configured server and reports:
- `Connected` — working
- `Needs authentication` — OAuth required (currently blocked by Claude Code bugs — see Section 4)
- `Failed to connect` — broken (see Section 12 Troubleshooting)

### Expected output (as of 2026-02-17)
```
biocontext-local:  ✓ Connected
biorender:         ! Needs authentication    ← OAuth bug
biomcp:            ✓ Connected
pubmed:            ✗ Failed to connect       ← rate-limited (see Section 9)
biorxiv:           ✓ Connected
chembl:            ✓ Connected
clinical-trials:   ✓ Connected
synapse:           ! Needs authentication    ← OAuth bug
scholar-gateway:   ! Needs authentication    ← OAuth bug
owkin:             ✗ Failed to connect       ← OAuth bug (expired token)
medidata:          ! Needs authentication    ← OAuth bug
tooluniverse:      ✓ Connected
uniprot:           ✓ Connected
alphafold:         ✓ Connected
pdb:               ✓ Connected
reactome-an:       ✓ Connected
biocontext:        ✓ Connected
paper-search:      ✓ Connected
enrichr:           ✓ Connected
biothings:         ✓ Connected
gget:              ✓ Connected
opengenes:         ✓ Connected
synergy-age:       ✓ Connected
protocols-io:      ✓ Connected
```

**18 Connected, 4 Needs authentication (OAuth bug), 2 Failed (rate-limit / expired token)**

### Test a specific stdio server manually
```bash
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}}}' | timeout 10 <command>
```
Replace `<command>` with the server command (e.g., `node ~/mcp-servers/PDB-MCP-Server/build/index.js` or `biomcp run`). A successful response includes `"result":{"protocolVersion":"2024-11-05",...}`.

### Test an HTTP server manually
```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}}}' \
  https://biocontext-kb.fastmcp.app/mcp/
```

---

## 12. Troubleshooting

### "Failed to connect" on a Node.js server (Augmented Nature)
The `build/` directory is missing or stale. The repos ship TypeScript source only — you must compile:
```bash
cd ~/mcp-servers/<ServerName>
npm install
npx tsc
chmod 755 build/index.js
```
Then restart Claude Code. This was the exact fix applied to `reactome-an` on 2026-02-16.

### "Needs authentication" on HTTP servers (biorender, synapse, scholar-gateway, owkin, medidata)
As of 2026-02-17, Claude Code has known bugs preventing OAuth from triggering for HTTP MCP servers:
- [Issue #11814](https://github.com/anthropics/claude-code/issues/11814) — OAuth discovery fails with infinite `about:blank` loop
- [Issue #7290](https://github.com/anthropics/claude-code/issues/7290) — HTTP transport ignores authentication headers
- [Issue #2831](https://github.com/anthropics/claude-code/issues/2831) — Authentication header regression

All 5 servers correctly advertise OAuth via `WWW-Authenticate` headers per RFC 9728. The servers are configured correctly — they will start working once Anthropic fixes the OAuth implementation. Keep them in your config and monitor Claude Code release notes for a fix. Starting a new Claude Code session does **not** trigger the OAuth flow (confirmed 2026-02-17).

### "Failed to connect" on pubmed
The Anthropic-hosted PubMed endpoint (`pubmed.mcp.claude.com`) is frequently rate-limited (HTTP 429) or completely down. This is **not** a configuration issue — the endpoint itself is unreliable. See [Section 9: Literature Search Strategy](#9-literature-search-strategy) for 5 alternative ways to search PubMed and the broader literature. See [Section 10: Accessing Paywalled Papers](#10-accessing-paywalled-papers) for full-text access options. You can safely remove this server if desired:
```bash
claude mcp remove pubmed
```

### "Failed to connect" on owkin
The OAuth token has expired. Error message says: "Authentication failed. The provided bearer token is invalid, expired, or no longer recognized." This is blocked by the same OAuth bugs as the other Tier 2 servers.

### biocontext HTTP URL redirect
The original URL `https://mcp.biocontext.ai/mcp/` now redirects (HTTP 301) to `https://biocontext-kb.fastmcp.app/mcp/`. Claude Code doesn't follow MCP redirects properly, so use the direct URL:
```bash
claude mcp remove biocontext
claude mcp add --transport http biocontext https://biocontext-kb.fastmcp.app/mcp/
```

### ToolUniverse missing API keys
ToolUniverse warns about missing keys on startup. This is normal — most of the 1400+ tools work without them. To add keys for specific tools:
```bash
claude mcp remove tooluniverse
claude mcp add -e HF_TOKEN=your_token -e OMIM_API_KEY=your_key --transport stdio tooluniverse -- tooluniverse-smcp-stdio --compact-mode
```

### protocols-io-mcp token error
```
ValueError: Missing required environment variable: PROTOCOLS_IO_CLIENT_ACCESS_TOKEN
```
This requires a **Client Access Token** (not client ID or client secret — those are for HTTP/SSE transport only):
1. Go to https://www.protocols.io/developers
2. Navigate to "API Clients" > create a new application
3. Copy the **Client Access Token** (the long hex string, not the shorter client_id or client_secret)
4. Reconfigure:
```bash
claude mcp remove protocols-io
claude mcp add -e PROTOCOLS_IO_CLIENT_ACCESS_TOKEN=your_token --transport stdio protocols-io -- protocols-io-mcp
```

### pharmacology-mcp crash on startup
```
AttributeError: 'str' object has no attribute '_lifespan'
```
This is an upstream bug in the holy-bio-mcp pharmacology server. Do not install. Monitor the [repository](https://github.com/longevity-genie/holy-bio-mcp) for a fix.

### General: removing and re-adding a server
```bash
claude mcp remove <server-name>
claude mcp add --transport <http|stdio> <server-name> <command-or-url> [args...]
```

### Running `claude mcp` from inside a Claude Code session
You'll get: `Error: Claude Code cannot be launched inside another Claude Code session`. Prefix with `CLAUDECODE= `:
```bash
CLAUDECODE= claude mcp list
CLAUDECODE= claude mcp add --transport stdio <name> -- <command>
```

---

## 13. Server Reference Table

| # | Server | Transport | Source | What It Does | Status (2026-02-17) |
|---|--------|-----------|--------|-------------|--------|
| 1 | `biocontext-local` | stdio (uvx) | BioContextAI | UniProt, STRING, HPA, Ensembl, KEGG, OpenTargets, GO, Europe PMC, and more | Connected |
| 2 | `biocontext` | HTTP | BioContextAI | Same as above, remote version | Connected |
| 3 | `biomcp` | stdio (pip) | GenomOncology | PubMed, genes, diseases, drugs, variants, clinical trials, FDA | Connected |
| 4 | `biorxiv` | HTTP | DeepSense.ai | bioRxiv/medRxiv preprint search and metadata | Connected |
| 5 | `chembl` | HTTP | DeepSense.ai | Bioactive molecules, compounds, targets, mechanisms | Connected |
| 6 | `clinical-trials` | HTTP | DeepSense.ai | ClinicalTrials.gov search, trial details, endpoints | Connected |
| 7 | `pubmed` | HTTP | Anthropic | PubMed literature search | Unreliable (rate-limited) |
| 8 | `tooluniverse` | stdio (pip) | ToolUniverse | 1400+ bioinformatics tools | Connected |
| 9 | `uniprot` | stdio (node) | Augmented Nature | Deep UniProt protein data, features, variants, pathways | Connected |
| 10 | `alphafold` | stdio (node) | Augmented Nature | AlphaFold predicted structures, confidence scores | Connected |
| 11 | `pdb` | stdio (node) | Augmented Nature | PDB experimental structures, quality metrics | Connected |
| 12 | `reactome-an` | stdio (node) | Augmented Nature | Reactome pathways, reactions, species data | Connected |
| 13 | `paper-search` | stdio (pip) | Community | Multi-platform paper search (arXiv, PubMed, bioRxiv, medRxiv, Google Scholar) | Connected |
| 14 | `enrichr` | stdio (npx) | Community | Gene set enrichment analysis | Connected |
| 15 | `biothings` | stdio (uvx) | Holy Bio MCP | MyGene, MyVariant, MyChem APIs | Connected |
| 16 | `gget` | stdio (uvx) | Holy Bio MCP | Genomics toolkit (BLAST, enrichment, sequences) | Connected |
| 17 | `opengenes` | stdio (uvx) | Holy Bio MCP | Longevity/aging genetics database | Connected |
| 18 | `synergy-age` | stdio (uvx) | Holy Bio MCP | Drug synergy database for aging research | Connected |
| 19 | `protocols-io` | stdio (pip) | Community | Laboratory protocols database | Connected |
| 20 | `biorender` | HTTP | BioRender | Scientific illustration platform | OAuth broken |
| 21 | `synapse` | HTTP | Sage Bionetworks | Data sharing platform | OAuth broken |
| 22 | `scholar-gateway` | HTTP | Wiley | Academic literature access | OAuth broken |
| 23 | `owkin` | HTTP | Owkin | Pathology AI platform | OAuth broken |
| 24 | `medidata` | HTTP | Medidata | Clinical data management | OAuth broken |

**Summary: 19 Connected, 5 blocked by Claude Code OAuth bugs, 1 unreliable (pubmed rate limiting)**

---

## Quick Install Script

For a fresh system, run these commands in order (outside of Claude Code):

```bash
# --- Prerequisites ---
curl -LsSf https://astral.sh/uv/install.sh | sh  # install uv/uvx
pip install biomcp-python tooluniverse paper-search-mcp protocols-io-mcp

# --- Tier 1: HTTP (No Auth) ---
claude mcp add --transport http biorxiv https://mcp.deepsense.ai/biorxiv/mcp
claude mcp add --transport http chembl https://mcp.deepsense.ai/chembl/mcp
claude mcp add --transport http clinical-trials https://mcp.deepsense.ai/clinical_trials/mcp
claude mcp add --transport http pubmed https://pubmed.mcp.claude.com/mcp
claude mcp add --transport http biocontext https://biocontext-kb.fastmcp.app/mcp/

# --- Tier 2: HTTP (Auth Required — currently broken, keep for future) ---
claude mcp add --transport http biorender https://mcp.services.biorender.com/mcp
claude mcp add --transport http synapse https://mcp.synapse.org/mcp
claude mcp add --transport http scholar-gateway https://connector.scholargateway.ai/mcp
claude mcp add --transport http owkin https://mcp.k.owkin.com/mcp
claude mcp add --transport http medidata https://mcp.imedidata.com/mcp

# --- Tier 3: Augmented Nature (Node.js) ---
mkdir -p ~/mcp-servers && cd ~/mcp-servers
for repo in augmented-nature-uniprot-mcp-server alphafold-mcp-server pdb-mcp-server reactome-mcp-server; do
  git clone https://github.com/augmented-nature/$repo.git
done
# Rename for consistency
mv augmented-nature-uniprot-mcp-server Augmented-Nature-UniProt-MCP-Server
mv alphafold-mcp-server AlphaFold-MCP-Server
mv pdb-mcp-server PDB-MCP-Server
mv reactome-mcp-server Reactome-MCP-Server
for dir in Augmented-Nature-UniProt-MCP-Server AlphaFold-MCP-Server PDB-MCP-Server Reactome-MCP-Server; do
  cd ~/mcp-servers/$dir && npm install && npx tsc && chmod 755 build/index.js
done
claude mcp add --transport stdio uniprot -- node ~/mcp-servers/Augmented-Nature-UniProt-MCP-Server/build/index.js
claude mcp add --transport stdio alphafold -- node ~/mcp-servers/AlphaFold-MCP-Server/build/index.js
claude mcp add --transport stdio pdb -- node ~/mcp-servers/PDB-MCP-Server/build/index.js
claude mcp add --transport stdio reactome-an -- node ~/mcp-servers/Reactome-MCP-Server/build/index.js

# --- Tier 4: Python-based ---
claude mcp add --transport stdio biocontext-local -e UV_PYTHON=3.12 -- uvx biocontext_kb@latest
claude mcp add --transport stdio biomcp -- biomcp run
claude mcp add --transport stdio tooluniverse -- tooluniverse-smcp-stdio --compact-mode
claude mcp add --transport stdio paper-search -- python3 -c "from paper_search_mcp.server import mcp; mcp.run()"
# protocols-io: replace YOUR_TOKEN with your Client Access Token from protocols.io/developers
claude mcp add -e PROTOCOLS_IO_CLIENT_ACCESS_TOKEN=YOUR_TOKEN --transport stdio protocols-io -- protocols-io-mcp

# --- Tier 5: Holy Bio MCP (uvx) ---
claude mcp add --transport stdio biothings -- uvx --from biothings-mcp stdio
claude mcp add --transport stdio gget -- uvx gget-mcp stdio
claude mcp add -e MCP_TRANSPORT=stdio --transport stdio opengenes -- uvx opengenes-mcp
claude mcp add -e MCP_TRANSPORT=stdio --transport stdio synergy-age -- uvx synergy-age-mcp

# --- Tier 6: npm-based ---
claude mcp add --transport stdio enrichr -- npx enrichr-mcp-server -l pop

# --- Verify ---
claude mcp list
```

---

## 14. Changelog

### 2026-02-17 (update 2)
- **Added Section 10 (Accessing Paywalled Papers)**: Documents the limitation that no MCP server supports institutional proxy auth (EZproxy/Shibboleth). Covers 4 options: Unpaywall MCP (open-access discovery), Zotero MCP (best for UW institutional access), BrowserMCP (browser session passthrough), and additional paper search servers. Includes recommended workflow for paywalled content.
- **Added NCBI API credentials**: Configured `ENTREZ_EMAIL` and `NCBI_API_KEY` in `~/.bashrc` for NCBI E-utilities access (used by `paper-search`, `biomcp`, and `biothings`).

### 2026-02-17
- **Confirmed OAuth bug**: Starting a new Claude Code session does NOT trigger OAuth for biorender, synapse, scholar-gateway, owkin, or medidata. Root cause is Claude Code issues #11814, #7290, #2831. All 5 servers advertise OAuth correctly per RFC 9728.
- **Clarified protocols.io token**: The `PROTOCOLS_IO_CLIENT_ACCESS_TOKEN` is a **Client Access Token** obtained from the developer portal, not the OAuth client_id or client_secret.
- **Added Section 9 (Literature Search Strategy)**: Documents 6 redundant ways to search the literature, ensuring PubMed access even when the Anthropic-hosted connector fails.
- Updated server reference table: protocols-io now Connected (token configured), pubmed status changed to "Unreliable".

### 2026-02-16
- **Initial installation** of 17 MCP servers via `claude mcp add`.
- **Fixed `biocontext` HTTP URL**: `mcp.biocontext.ai/mcp/` → `biocontext-kb.fastmcp.app/mcp/` (original redirects, Claude Code doesn't follow MCP redirects).
- **Fixed `reactome-an`**: Built TypeScript source (`npx tsc`) — the repo had no `build/` directory.
- **Added 7 new servers**: paper-search, protocols-io, enrichr, biothings, gget, opengenes, synergy-age.
- **Removed `pharmacology-mcp`**: Upstream bug (`AttributeError: 'str' object has no attribute '_lifespan'`).
- Total: 24 servers configured, 18 connected on first check.

---

*Last updated: 2026-02-17*
*Configuration file: `~/.claude.json`*
