<!-- Created: 2026-02-23 -->
<!-- Last updated: 2026-02-23 — Initial creation -->

# Conversation Summary — 2026-02-23 ~20:19

## Objective

Research the recently announced CellType CLI tool — understand what it is, how the codebase works, its architecture, and whether it requires paid API access.

## What We Learned

### CellType CLI (`ct`) Overview

CellType CLI is an **autonomous AI agent for drug discovery research** — described as "Claude Code, but for biology." Built by CellType Inc. (YC W26 startup, founded by David van Dijk from Yale and Ivan Vrkic, ex-CERN). MIT licensed, open source at `github.com/celltype/cli`.

You ask natural language drug discovery questions, and it plans multi-step analyses, calls tools, executes code, self-corrects, and returns data-backed conclusions. Claims **90% accuracy** on BixBench-Verified-50 (vs 65.3% for vanilla Claude Code).

### Claude API Requirement

**Yes, it requires a paid Anthropic API key.** There is no CellType subscription — API calls go directly to Anthropic on your key. The agentic loop makes many LLM calls per query (up to 30 turns by default), so costs accumulate quickly:

| Model | Input / 1M tokens | Output / 1M tokens |
|-------|-------------------|---------------------|
| Sonnet 4.5 (default) | $3.00 | $15.00 |
| Haiku 4.5 | $0.80 | $4.00 |
| Opus 4.6 | $15.00 | $75.00 |

Also supports OpenAI and local models (vLLM/ollama) as alternatives.

### Interesting Architectural Patterns

1. **Claude Agent SDK as the core loop** — The `AgentRunner` (`src/ct/agent/runner.py`) uses `ClaudeSDKClient` from `claude-agent-sdk`. Claude directly orchestrates all tools in an agentic loop (plan → call tools → read results → self-correct → synthesize). This replaced an earlier Plan-then-Execute architecture.

2. **In-process MCP server for tool exposure** — All 190+ domain tools are wrapped as MCP tools via `create_sdk_mcp_server` (`src/ct/agent/mcp_server.py`). The existing Python `ToolRegistry` (decorator-based registration) is bridged to MCP so the Agent SDK can invoke them. Each tool handler runs synchronously in a thread via `asyncio.to_thread`.

3. **Massive engineered system prompt** — `src/ct/agent/system_prompt.py` assembles identity, tool catalog, workflow guides, domain knowledge primer, bioinformatics code-gen hints, and synthesis rules into one system prompt. Notably, full tool descriptions are NOT included (would blow up to 155K chars) — instead, MCP provides tool schemas natively and the prompt includes only a brief orientation.

4. **Sandboxed code execution** — `src/ct/agent/sandbox.py` provides a persistent `exec()` environment with:
   - Blocked imports (subprocess, socket, ctypes, etc.)
   - Restricted file I/O (reads: CWD + output dir + downloads + /tmp; writes: output dir + /tmp only)
   - Whitelisted subprocess for bioinformatics CLIs only (bwa, samtools, minimap2, etc.)
   - AST-based protection of pre-imported helper functions (strips LLM redefinitions)
   - Variables persist across tool calls within a query

5. **Multi-agent orchestrator** — `src/ct/agent/orchestrator.py` decomposes complex queries into N parallel research threads via a meta-planner LLM call, runs them in `ThreadPoolExecutor` with an `EvidenceBoard` for shared findings, then merges and synthesizes results. Live Rich terminal display shows per-thread progress.

6. **Nested Claude Code as a tool** — `src/ct/tools/claude.py` defines a `claude.code` tool that spawns `claude -p` (Claude Code CLI) as a subprocess for complex coding tasks. Opt-in, disabled by default. So you get Claude (via Agent SDK) orchestrating tools, one of which can invoke Claude Code as a sub-agent.

7. **Unified LLM client** — `src/ct/models/llm.py` provides a single `LLMClient` interface across Anthropic, OpenAI, local models (vLLM/transformers), and CellType's own "GlueLM" model, with built-in usage/cost tracking and retry with exponential backoff.

### Tool Ecosystem

190+ tools across ~30 categories: target discovery, chemistry (SAR, fingerprints), expression (L1000, pathway enrichment), viability (dose-response, PRISM), clinical (trial search, indication mapping), safety (ADMET, anti-target flagging), omics (GEO, DESeq2), DNA (ORF finding, primer design, Gibson assembly), 30+ database APIs (PubMed, ChEMBL, UniProt, Open Targets, ClinicalTrials.gov, Reactome, PDBe), plus `run_python` and `run_r` sandbox tools.

## Files Modified

None — this was a research/exploration session only. The CellType CLI repo was cloned to `/tmp/celltype-cli` for reading.

## PR Links

None.

## Outcome

Completed a thorough codebase review of CellType CLI. Decided not to try it right now due to Claude API costs. The architectural patterns (Agent SDK + MCP tool wrapping, sandboxed execution, multi-agent orchestration) are useful reference points for future projects.
