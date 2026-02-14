# Advanced Claude Code Tools Setup

A comprehensive guide to advanced Claude Code features and a full "BioClaude" setup
for biological research. Covers hooks, skills, custom agents, MCP servers for life
sciences, and future-proofing strategies.

**Who this is for**: Researchers (especially in biology/genomics) who want to turn
Claude Code into a full-powered research workstation connected to biological databases,
bioinformatics tools, and lab platforms.

**Author**: Robert Chen (Fowler Lab, UW)
**Last updated**: 2026-02-14

---

## Table of Contents

1. [Advanced Claude Code Features](#1-advanced-claude-code-features)
   - [Hooks](#hooks)
   - [Skills (Custom Slash Commands)](#skills-custom-slash-commands)
   - [Custom Agents (Subagents)](#custom-agents-subagents)
   - [Extended Thinking](#extended-thinking)
   - [Permissions Whitelisting](#permissions-whitelisting)
2. [MCP (Model Context Protocol) Overview](#2-mcp-model-context-protocol-overview)
3. [BioClaude: Full Bio Research Setup](#3-bioclaude-full-bio-research-setup)
   - [Quick Start (5 minutes)](#quick-start-5-minutes)
   - [Tier 1: Core Bio Databases](#tier-1-core-bio-databases)
   - [Tier 2: Lab Platforms](#tier-2-lab-platforms)
   - [Tier 3: Bioinformatics CLI Tools](#tier-3-bioinformatics-cli-tools)
   - [Tier 4: Literature & Enrichment](#tier-4-literature--enrichment)
4. [MCP Server Reference Table](#4-mcp-server-reference-table)
5. [Future-Proofing: Stay Up to Date](#5-future-proofing-stay-up-to-date)
6. [Recommended Project Structure](#6-recommended-project-structure)
7. [Troubleshooting](#7-troubleshooting)

---

## 1. Advanced Claude Code Features

These are built-in Claude Code capabilities that don't require MCP. Set them up by
creating a `.claude/` directory in your project root.

```bash
mkdir -p .claude/skills .claude/agents
```

### Hooks

Hooks are shell commands that fire automatically at lifecycle events. They live in
`.claude/settings.json`.

**Available hook events:**

| Event | When It Fires | Use Case |
|-------|---------------|----------|
| `SessionStart` | When a session begins | Print reminders, load environment |
| `PreToolUse` | Before a tool executes | Block dangerous operations, enforce rules |
| `PostToolUse` | After a tool succeeds | Auto-run tests, lint, format |
| `Stop` | When Claude finishes responding | Summary logging, notifications |

**Example: Auto-run tests after every file edit**

```json
// .claude/settings.json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "cd $CLAUDE_PROJECT_DIR && python -m pytest test_calculator.py -q 2>&1 | tail -5"
          }
        ]
      }
    ]
  }
}
```

**Example: Block edits to production config files**

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "echo $CLAUDE_TOOL_INPUT | grep -q 'production.yml' && exit 2 || exit 0"
          }
        ]
      }
    ]
  }
}
```

Exit code `2` from a `PreToolUse` hook **blocks** the operation. Exit code `0` allows it.

**Example: Session start reminder**

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo '** Remember: run tests before committing. Check CLAUDE.md for project rules. **'"
          }
        ]
      }
    ]
  }
}
```

---

### Skills (Custom Slash Commands)

Skills are reusable prompt templates you invoke with `/skill-name`. They live in
`.claude/skills/<name>/SKILL.md`.

**Creating a skill:**

```bash
mkdir -p .claude/skills/fix-bug
```

Then create `.claude/skills/fix-bug/SKILL.md`:

```yaml
---
name: fix-bug
description: Fix a bug in the calculator with full test coverage
argument-hint: "[function-name]"
---

Fix the bug in $ARGUMENTS in calculator.py:
1. Write a failing test that reproduces the bug
2. Fix the implementation
3. Run the full test suite to verify nothing broke
4. Commit with message: "fix: handle edge case in [function-name]"
```

**Usage:** `/fix-bug divide`

**Dynamic context injection** — inject shell command output into the prompt:

```yaml
---
name: review
description: Review recent changes with test coverage info
---

Review the following changes and suggest improvements:

!`git diff HEAD~1`!

Current test coverage:
!`python -m pytest --cov=calculator --cov-report=term-missing -q 2>&1 | tail -20`!
```

**More skill ideas for a bio research project:**

| Skill | What It Does |
|-------|-------------|
| `/run-tests` | Run pytest with coverage report |
| `/lint` | Run linting and type checking |
| `/search-lit [topic]` | Search PubMed via MCP for a topic |
| `/lookup-protein [id]` | Query UniProt + AlphaFold for a protein |
| `/enrichment [gene-list]` | Run Enrichr enrichment analysis |

---

### Custom Agents (Subagents)

Custom agents are specialized Claude instances with their own tools, models, and
instructions. They live in `.claude/agents/<name>.md`.

**Example: Test runner agent**

Create `.claude/agents/test-runner.md`:

```yaml
---
name: test-runner
description: Run tests and diagnose failures
tools: Bash, Read
model: haiku
---

Run the full test suite. For any failures:
1. Read the failing test and the function under test
2. Identify the root cause
3. Suggest a specific fix with code
4. Do NOT modify any files — only report findings
```

**Example: Literature search agent**

Create `.claude/agents/lit-search.md`:

```yaml
---
name: lit-search
description: Search biological literature across PubMed and preprint servers
tools: Bash, Read, WebSearch, WebFetch
model: sonnet
---

Search for papers related to the user's query. For each relevant paper:
1. Provide title, authors, journal, year
2. Write a 2-3 sentence summary of the key findings
3. Note any methodological relevance to deep mutational scanning or functional genomics
4. Provide the DOI or URL

Search PubMed, bioRxiv, and medRxiv. Prioritize recent papers (last 2 years).
```

**Invoking agents:**
- Use `/agents` to list available agents
- Agents are invoked automatically when Claude determines they're relevant, or you can
  reference them explicitly in your prompts

---

### Extended Thinking

For complex analysis, you can trigger deeper reasoning by phrasing your prompts:

| Phrase | Effect |
|--------|--------|
| "think step by step" | Standard chain-of-thought |
| "think deeply about this" | Extended thinking mode |
| "ultrathink" | Maximum reasoning depth |

Useful for: debugging complex pipelines, analyzing experimental designs, planning
multi-step bioinformatics workflows.

---

### Permissions Whitelisting

Reduce permission prompts for tools you trust by configuring allowed tools in
`.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(pytest:*)",
      "Bash(python:*)",
      "Bash(git:*)",
      "Bash(conda:*)",
      "Bash(pip:*)"
    ]
  }
}
```

This lets Claude run `pytest`, `python`, `git`, `conda`, and `pip` commands without
asking for permission each time.

---

## 2. MCP (Model Context Protocol) Overview

MCP is an open protocol that connects Claude to external tools and data sources. Think
of it like USB-C for AI — a standard way to plug in any tool.

**How it works:**

```
Claude Code  <-->  MCP Client  <-->  MCP Server  <-->  External Tool/Database
```

**Two transport types:**

| Type | How It Works | When to Use |
|------|-------------|-------------|
| `http` (remote) | Connects to a hosted server via URL | Cloud-hosted databases (UniProt, PubMed, etc.) |
| `stdio` (local) | Runs a local process that Claude communicates with via stdin/stdout | CLI tools (BLAST, SAMtools), local APIs |

**Adding an MCP server:**

```bash
# Remote (HTTP) server
claude mcp add --transport http <name> <url>

# Local (stdio) server
claude mcp add --transport stdio <name> <command> [args...]

# List configured servers
claude mcp list

# Remove a server
claude mcp remove <name>
```

MCP configuration is stored in `.claude/settings.json` under the `mcpServers` key.

---

## 3. BioClaude: Full Bio Research Setup

A step-by-step guide to building a Claude Code environment optimized for biological
research — from protein databases to bioinformatics pipelines.

### Quick Start (5 minutes)

Get the most value with the least setup. These three commands give you access to 20+
biological databases, scientific figure search, and literature search.

```bash
# Step 1: BioContextAI — unified access to UniProt, AlphaFold, Ensembl,
# KEGG, Gene Ontology, Europe PMC, ClinicalTrials.gov, and more
# Published in Nature Biotechnology (2025). One server, 20+ databases.
claude mcp add --transport http biocontext https://mcp.biocontext.ai/mcp/

# Step 2: BioRender — search 50,000+ scientifically accurate icons and templates
# Official Anthropic partnership. Requires free BioRender account.
claude mcp add --transport http biorender https://mcp.services.biorender.com/mcp

# Step 3: BioMCP — PubMed + ClinicalTrials.gov + genomic variants (21 tools)
pip install biomcp-python
claude mcp add --transport stdio biomcp -- biomcp run

# Verify everything is connected
claude mcp list
```

**Test it out:**
```
> Search UniProt for human BRCA1 and show me the protein domains

> Find recent papers on deep mutational scanning of BRCA1

> Search BioRender for a CRISPR illustration
```

That's it. You now have a research-connected Claude. The sections below go deeper.

---

### Tier 1: Core Bio Databases

These MCP servers connect Claude directly to the major biological databases.

#### BioContextAI (Recommended Starting Point)

A unified MCP gateway to 20+ biomedical databases. Published in
[Nature Biotechnology](https://www.nature.com/articles/s41587-025-02900-9) by
researchers at EMBL-EBI, Helmholtz Munich, and Open Targets.

```bash
# Remote hosted server (for testing and moderate use — subject to fair use)
claude mcp add --transport http biocontext https://mcp.biocontext.ai/mcp/

# OR: Run locally for heavier use
pip install biocontext-kb
claude mcp add --transport stdio biocontext-local -- uvx biocontext_kb@latest
```

**Databases accessible through BioContextAI:**

| Database | What It Provides |
|----------|-----------------|
| UniProt | Protein sequences, functions, annotations |
| AlphaFold DB | Predicted 3D protein structures |
| Ensembl | Gene sequences, coordinates, variants |
| KEGG | Metabolic and signaling pathways |
| Gene Ontology | Functional annotations (GO terms) |
| Europe PMC | Biomedical literature (like PubMed but broader) |
| ClinicalTrials.gov | Clinical trial records |
| ChEMBL | Bioactive drug-like molecules |
| Open Targets | Drug target evidence and associations |
| Reactome | Curated biological pathways |

- **GitHub**: [biocontext-ai/knowledgebase-mcp](https://github.com/biocontext-ai/knowledgebase-mcp)
- **Registry**: [biocontext.ai/registry](https://biocontext.ai/registry)

#### Individual Database Servers (Augmented Nature Suite)

If you need deeper access to specific databases beyond what BioContextAI provides:

```bash
# UniProt — 26 tools: protein search, sequence retrieval, feature analysis, homologs
# GitHub: Augmented-Nature/Augmented-Nature-UniProt-MCP-Server
git clone https://github.com/Augmented-Nature/Augmented-Nature-UniProt-MCP-Server.git
cd Augmented-Nature-UniProt-MCP-Server && pip install -r requirements.txt
claude mcp add --transport stdio uniprot -- python server.py

# AlphaFold — structure retrieval, confidence analysis, multi-format downloads
# GitHub: Augmented-Nature/AlphaFold-MCP-Server
git clone https://github.com/Augmented-Nature/AlphaFold-MCP-Server.git
cd AlphaFold-MCP-Server && pip install -r requirements.txt
claude mcp add --transport stdio alphafold -- python server.py

# PDB — experimental structures, quality metrics, cross-references
# GitHub: Augmented-Nature/PDB-MCP-Server
git clone https://github.com/Augmented-Nature/PDB-MCP-Server.git
cd PDB-MCP-Server && pip install -r requirements.txt
claude mcp add --transport stdio pdb -- python server.py

# Reactome — pathway search, gene-to-pathways, disease pathways (8 tools)
# GitHub: Augmented-Nature/Reactome-MCP-Server
git clone https://github.com/Augmented-Nature/Reactome-MCP-Server.git
cd Reactome-MCP-Server && pip install -r requirements.txt
claude mcp add --transport stdio reactome -- python server.py
```

---

### Tier 2: Lab Platforms

#### BioRender

Official Anthropic partnership. Search 50,000+ scientifically accurate icons and
templates for figures, posters, graphical abstracts.

```bash
claude mcp add --transport http biorender https://mcp.services.biorender.com/mcp
```

- Requires a free BioRender account (premium features need paid plan)
- [BioRender MCP Docs](https://help.biorender.com/hc/en-gb/articles/30870978672157-How-to-use-the-BioRender-MCP-connector)

#### Benchling

Official MCP server for querying your lab's ELN (electronic lab notebook), sample
registry, and inventory.

```bash
# Replace <tenant> with your Benchling tenant name
claude mcp add --transport http benchling https://<tenant>.mcp.benchling.com/mcp
```

**Prerequisites:**
- Your Benchling admin must enable the V3 API and MCP access
- Benchling AI (Deep Research) module must be active on your tenant
- Queries inherit your Benchling permissions and are fully audited

**What you can do:**
- Search across experimental results and notebook entries
- Query the sample registry and inventory
- Find protocols and templates
- Cross-reference data across experiments

- [Benchling MCP Docs](https://help.benchling.com/hc/en-us/articles/40342713479437-Benchling-MCP)
- Community alternative: `pip install benchling-mcp` (unofficial)

#### Protocols.io

Search, retrieve, and manage scientific protocols.

```bash
# Check for latest install instructions:
# https://glama.ai/mcp/servers/@hqn21/protocols-io-mcp-server
git clone https://github.com/hqn21/protocols-io-mcp-server.git
cd protocols-io-mcp-server && npm install
claude mcp add --transport stdio protocols -- node index.js
```

---

### Tier 3: Bioinformatics CLI Tools

The [bio-mcp](https://github.com/bio-mcp) project wraps standard bioinformatics
command-line tools as MCP servers. This lets you say things like "BLAST this sequence
against nr" and Claude orchestrates the entire pipeline.

**Prerequisites:** Install the underlying tools first.

```bash
# Install bioinformatics tools via conda/mamba
conda install -c bioconda blast samtools bwa seqkit fastqc multiqc
```

**Available bio-mcp servers:**

| Server | Tool | What It Does |
|--------|------|-------------|
| `bio-mcp-blast` | NCBI BLAST | Sequence similarity search, custom DB creation |
| `bio-mcp-samtools` | SAMtools | BAM/SAM manipulation, sorting, indexing, flagstat |
| `bio-mcp-bwa` | BWA | Read alignment to reference genomes |
| `bio-mcp-seqkit` | SeqKit | Sequence stats, format conversion, filtering |
| `bio-mcp-fastqc` | FastQC/MultiQC | Sequencing data quality control |

```bash
# Example: Install and configure bio-mcp-blast
pip install bio-mcp-blast
claude mcp add --transport stdio blast -- bio-mcp-blast

# Example: Install and configure bio-mcp-samtools
pip install bio-mcp-samtools
claude mcp add --transport stdio samtools -- bio-mcp-samtools
```

**Example conversation after setup:**
```
> I have a FASTA file at data/unknown_sequences.fasta.
> BLAST these against the nr database and summarize the top hits.

> Align the FASTQ files in data/reads/ to the hg38 reference genome,
> sort the output, and give me alignment statistics.
```

---

### Tier 4: Literature & Enrichment

#### PubMed MCP Server

```bash
# Option A: Dedicated PubMed server (cyanheads)
# GitHub: cyanheads/pubmed-mcp-server
git clone https://github.com/cyanheads/pubmed-mcp-server.git
cd pubmed-mcp-server && npm install
claude mcp add --transport stdio pubmed -- node dist/index.js

# Option B: Multi-source paper search (arXiv + PubMed + bioRxiv + medRxiv)
# GitHub: openags/paper-search-mcp
pip install paper-search-mcp
claude mcp add --transport stdio papers -- paper-search-mcp
```

#### BioMCP (GenomOncology)

A comprehensive server combining literature, clinical trials, and genomic variants.

```bash
pip install biomcp-python
claude mcp add --transport stdio biomcp -- biomcp run
```

**21 tools including:**
- PubMed article search and retrieval
- ClinicalTrials.gov query
- MyVariant.info genomic variant lookup
- Cross-referencing between all three

- [GitHub: genomoncology/biomcp](https://github.com/genomoncology/biomcp)

#### Enrichr MCP Server

Gene set enrichment analysis across GO, KEGG, Reactome, WikiPathways, and more.

```bash
# GitHub: tianqitang1/enrichr-mcp-server
git clone https://github.com/tianqitang1/enrichr-mcp-server.git
cd enrichr-mcp-server && pip install -r requirements.txt
claude mcp add --transport stdio enrichr -- python server.py
```

**Example:**
```
> Run enrichment analysis on this gene list: BRCA1, TP53, ATM, CHEK2, PALB2
> Show me the top GO Biological Process and KEGG pathway terms.
```

#### Holy Bio MCP (Longevity/Aging Research + gget)

Aggregates multiple bio sub-servers including `gget` (popular Python genomics library).

```bash
# Wraps gget for Ensembl, NCBI, UniProt queries
# Plus OpenGenes (aging/longevity) and BioThings APIs
# See: https://lobehub.com/mcp/longevity-genie-holy-bio-mcp
pip install holy-bio-mcp
claude mcp add --transport stdio holybio -- holy-bio-mcp
```

---

## 4. MCP Server Reference Table

Complete reference of all biological MCP servers discussed in this guide.

| Server | Transport | Databases/Tools | Install Complexity | Best For |
|--------|-----------|----------------|-------------------|----------|
| **BioContextAI** | HTTP | 20+ databases (UniProt, AlphaFold, Ensembl, KEGG, GO, etc.) | One command | General bio research (start here) |
| **BioRender** | HTTP | 50k+ scientific icons/templates | One command | Figures, posters, graphical abstracts |
| **Benchling** | HTTP | Your lab's ELN, registry, inventory | Admin setup required | Labs using Benchling |
| **BioMCP** | stdio | PubMed, ClinicalTrials.gov, genomic variants | pip install | Literature + clinical + variants |
| **UniProt MCP** | stdio | UniProt (26 tools) | git clone + pip | Deep protein research |
| **AlphaFold MCP** | stdio | AlphaFold DB | git clone + pip | Predicted structures |
| **PDB MCP** | stdio | Protein Data Bank | git clone + pip | Experimental structures |
| **Reactome MCP** | stdio | Reactome pathways | git clone + pip | Pathway analysis |
| **Enrichr MCP** | stdio | GO, KEGG, Reactome, WikiPathways, MSigDB | git clone + pip | Gene set enrichment |
| **PubMed MCP** | stdio | PubMed/NCBI | git clone + npm | Literature search |
| **Paper Search** | stdio | arXiv + PubMed + bioRxiv + medRxiv | pip install | Multi-source lit search |
| **bio-mcp-blast** | stdio | NCBI BLAST | pip + conda | Sequence similarity |
| **bio-mcp-samtools** | stdio | SAMtools | pip + conda | BAM/SAM processing |
| **bio-mcp-bwa** | stdio | BWA | pip + conda | Read alignment |
| **bio-mcp-seqkit** | stdio | SeqKit | pip + conda | Sequence utilities |
| **bio-mcp-fastqc** | stdio | FastQC/MultiQC | pip + conda | Sequencing QC |
| **Holy Bio MCP** | stdio | gget, OpenGenes, BioThings | pip install | Genomics + aging research |
| **Protocols.io** | stdio | Protocols.io | git clone + npm | Protocol management |

---

## 5. Future-Proofing: Stay Up to Date

The MCP ecosystem for biology is growing fast. Here's how to keep your setup current.

### Automated Discovery: Check for New Servers

Create a skill that checks for new MCP servers. Save as
`.claude/skills/check-bio-mcp/SKILL.md`:

```yaml
---
name: check-bio-mcp
description: Check for new biological MCP servers and updates
---

Search the web for new MCP servers relevant to biological research:

1. Check these registries for new entries:
   - https://biocontext.ai/registry
   - https://mcpmed.org
   - https://github.com/punkpeye/awesome-mcp-servers
   - https://github.com/anthropics/life-sciences
   - https://glama.ai/mcp/servers (filter: biology/science)

2. Search GitHub for recent repos:
   - "mcp server" biology created:>2026-01-01
   - "mcp server" bioinformatics created:>2026-01-01
   - "mcp server" genomics created:>2026-01-01

3. Compare findings against our currently installed servers (run `claude mcp list`)

4. For any NEW servers found:
   - Summarize what they do
   - Note install complexity
   - Rate relevance to functional genomics / deep mutational scanning
   - Provide the install command

5. Check for updates to servers we already use:
   - BioContextAI: check GitHub releases
   - BioMCP: check PyPI for new version
   - bio-mcp suite: check for new tool wrappers
```

**Usage:** `/check-bio-mcp` — run this monthly to stay current.

### Key Registries to Watch

| Registry | URL | What It Tracks |
|----------|-----|---------------|
| **BioContextAI Registry** | [biocontext.ai/registry](https://biocontext.ai/registry) | Curated bio database MCP servers |
| **MCPMed Hub** | [mcpmed.org](https://mcpmed.org/) | Expert-validated bioinformatics MCPs |
| **Awesome MCP Servers** | [GitHub: punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) | Community-curated list of all MCP servers |
| **Anthropic Life Sciences** | [GitHub: anthropics/life-sciences](https://github.com/anthropics/life-sciences) | Official Anthropic plugins for science |
| **Glama MCP Directory** | [glama.ai/mcp/servers](https://glama.ai/mcp/servers) | Searchable MCP server directory |
| **bio-mcp GitHub Org** | [github.com/bio-mcp](https://github.com/bio-mcp) | Bioinformatics CLI tool wrappers |

### Emerging Projects to Watch

#### Science Context Protocol (SCP)

An extension of MCP specifically designed for multi-lab scientific workflows. Adds:
- Richer experiment metadata
- Centralized hub (vs. MCP's peer-to-peer model)
- Workflow orchestration through an experiment flow API
- Lab device integration with standardized drivers

Their Internal Discovery Platform currently provides 1,600+ interoperable tools,
with biology making up 45.9% of them. Not yet publicly available but worth tracking.

#### BioinfoMCP (Automated Tool Conversion)

An academic project ([arXiv: 2510.02139](https://arxiv.org/html/2510.02139v1)) that
**automatically converts** bioinformatics CLI tools into MCP servers by analyzing
their documentation and CLI interfaces. They've converted 38 tools with 94.7%
success rate. If this matures, it could make every bioinformatics tool instantly
MCP-compatible.

#### CZI / CZ Biohub

No public MCP integration as of February 2026. CZI tools like CZ ID (metagenomic
pathogen detection) and cellxgene (single-cell data explorer) are good candidates
for future MCP wrappers. Worth checking periodically.

### GitHub Watch Commands

Set up notifications for key repositories:

```bash
# Watch for new releases from key MCP projects
gh repo set-default biocontext-ai/knowledgebase-mcp
gh api repos/biocontext-ai/knowledgebase-mcp/subscription -f subscribed=true

# Star and watch the bio-mcp organization repos
gh api repos/bio-mcp/bio-mcp-blast/subscription -f subscribed=true

# Watch the awesome-mcp-servers list for new additions
gh api repos/punkpeye/awesome-mcp-servers/subscription -f subscribed=true
```

---

## 6. Recommended Project Structure

Here's the complete `.claude/` directory structure for a bio research project:

```
your-project/
├── .claude/
│   ├── settings.json          # Hooks, permissions, MCP config
│   ├── skills/
│   │   ├── fix-bug/
│   │   │   └── SKILL.md       # /fix-bug [function]
│   │   ├── run-tests/
│   │   │   └── SKILL.md       # /run-tests
│   │   ├── search-lit/
│   │   │   └── SKILL.md       # /search-lit [topic]
│   │   ├── lookup-protein/
│   │   │   └── SKILL.md       # /lookup-protein [uniprot-id]
│   │   ├── enrichment/
│   │   │   └── SKILL.md       # /enrichment [gene-list]
│   │   └── check-bio-mcp/
│   │       └── SKILL.md       # /check-bio-mcp (future-proofing)
│   └── agents/
│       ├── test-runner.md      # Run tests, diagnose failures
│       └── lit-search.md       # Search bio literature
├── CLAUDE.md                   # Project context and rules
├── calculator.py
├── test_calculator.py
└── ...
```

### Example settings.json (Full BioClaude Config)

```json
{
  "permissions": {
    "allow": [
      "Bash(pytest:*)",
      "Bash(python:*)",
      "Bash(git:*)",
      "Bash(conda:*)",
      "Bash(pip:*)"
    ]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "cd $CLAUDE_PROJECT_DIR && python -m pytest -q 2>&1 | tail -5"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo 'BioClaude active. MCP servers:' && claude mcp list 2>/dev/null || echo '(run claude mcp list to check)'"
          }
        ]
      }
    ]
  },
  "mcpServers": {
    "biocontext": {
      "transport": "http",
      "url": "https://mcp.biocontext.ai/mcp/"
    },
    "biorender": {
      "transport": "http",
      "url": "https://mcp.services.biorender.com/mcp"
    },
    "biomcp": {
      "transport": "stdio",
      "command": "biomcp",
      "args": ["run"]
    }
  }
}
```

---

## 7. Troubleshooting

### MCP server won't connect

```bash
# Check if the server is configured
claude mcp list

# Test a remote server URL directly
curl -s https://mcp.biocontext.ai/mcp/ | head -20

# For stdio servers, test the command runs
biomcp run --help

# Remove and re-add a server
claude mcp remove biocontext
claude mcp add --transport http biocontext https://mcp.biocontext.ai/mcp/
```

### "Tool not found" errors

MCP tools only appear after the server successfully connects. If tools aren't showing:
1. Restart Claude Code (`/exit` then `claude`)
2. Check server logs: `claude mcp logs <server-name>`
3. Verify the server process is running (for stdio servers)

### Hooks not firing

1. Verify `.claude/settings.json` is valid JSON (use `python -m json.tool`)
2. Check the `matcher` regex matches the tool name exactly
3. Test the hook command manually in your terminal
4. Check that the hook script is executable

### Permission errors with bio tools

```bash
# Ensure conda environment is activated before starting Claude
conda activate biotools
claude

# Or add conda activation to your session start hook
```

### Rate limiting on remote MCP servers

BioContextAI's hosted server is subject to fair use limits. For heavy use:

```bash
# Switch to local installation
pip install biocontext-kb
claude mcp remove biocontext
claude mcp add --transport stdio biocontext-local -- uvx biocontext_kb@latest
```

---

## Further Reading

- [MCP Specification](https://modelcontextprotocol.io/) — the official protocol docs
- [BioContextAI Paper (Nature Biotechnology)](https://www.nature.com/articles/s41587-025-02900-9)
- [EMBL: Connecting AI to Biology via MCP](https://www.embl.org/news/people-perspectives/connecting-ai-to-biology-model-context-protocol/)
- [MCPMed Paper (arXiv)](https://arxiv.org/abs/2507.08055)
- [BioinfoMCP Paper (arXiv)](https://arxiv.org/html/2510.02139v1)
- [Anthropic: Claude for Life Sciences](https://www.anthropic.com/news/claude-for-life-sciences)
- [BioRender + Anthropic Partnership](https://finance.yahoo.com/news/biorender-anthropic-partner-bring-scientific-204400573.html)
- [Science Context Protocol](https://the-decoder.com/science-context-protocol-aims-to-let-ai-agents-collaborate-across-labs-and-institutions-worldwide/)
