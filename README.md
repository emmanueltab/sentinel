# Sentinel

A browser-agnostic, AI-powered web content filter for Linux. Sentinel intercepts all browser traffic at the network level, evaluates search queries in real time, and enforces session limits and cooldowns across every browser on the machine.

Unlike DNS blocklists and keyword filters, Sentinel understands context. It can recognize that an innocent-looking search title refers to inappropriate content, evaluate intent behind ambiguous queries, and look up unknown names and titles before making a judgment.

---

## How it works

Sentinel runs as a local proxy that all browser traffic passes through. Every search query is extracted from the request and evaluated through a multi-layer filter pipeline. If a query is flagged, all browsers are closed immediately and a cooldown is enforced before any browser can be reopened.

The system is locked behind an admin password. Once installed, no component can be modified, disabled, or uninstalled without it.

---

## Filter Pipeline

| Layer            | Method                                         | Speed    | Privacy        |
|------------------|------------------------------------------------|----------|----------------|
| 0 — Wordlist     | Instant match against custom word list         | Instant  | Full           |
| 1 — URL Patterns | Match against known danger URL patterns        | Instant  | Full           |
| Whitelist        | Skip AI for known safe queries                 | Instant  | Full           |
| 2 — AI           | Contextual evaluation with optional web search | 1-5 sec  | Local or Cloud |

---

## What the AI layer catches that blocklists miss

- Titles and names that appear innocent but lead to inappropriate content
- Misspelled, abbreviated, or garbled versions of flagged terms
- Queries in foreign languages or alternative encodings
- Searches framed as innocent or educational but with inappropriate intent
- Individuals searched by name who are adult entertainers
- Platforms and communities that are high risk regardless of the search term

---

## Session Management

| Trigger                      | Cooldown   |
|------------------------------|------------|
| Session ends normally        | 5 minutes  |
| Manual close                 | 5 minutes  |
| Wordlist or pattern match    | 20 minutes |
| AI flags search              | 20 minutes |
| AI unavailable               | 5 minutes  |

---

## AI Backends

Sentinel supports multiple AI backends. Privacy-conscious deployments should use local Ollama. Cloud backends are faster but send queries to a third party.

| Backend         | Privacy | Speed   | Web Search | Cost             |
|-----------------|---------|---------|------------|------------------|
| Ollama (local)  | Full    | 1-5 sec | No         | Free             |
| Groq            | Cloud   | 1-2 sec | Yes        | Free (rate limit)|
| Anthropic       | Cloud   | 1-2 sec | No         | Paid             |

The backend is configured in `config.yml`. If no backend is configured, Sentinel fails closed — sessions are terminated rather than allowed through unfiltered.

---

## Hardware Requirements for Local AI

Running the AI layer locally via Ollama requires sufficient hardware to perform inference at acceptable speeds. The following are the recommended specifications based on model size.

### Minimum (CPU only)
- **CPU** — Quad core, 2.5GHz+ (Intel i5 / AMD Ryzen 5 or better)
- **RAM** — 16GB
- **Storage** — 20GB free for models
- **Expected speed** — 5-15 seconds per query (3B model)

CPU-only inference is functional but slow. Suitable for low-traffic deployments where a few seconds of latency is acceptable.

### Recommended (dedicated GPU)
- **CPU** — Intel i5 / AMD Ryzen 5 or better
- **RAM** — 16GB+
- **GPU** — 6GB VRAM minimum (NVIDIA GTX 1660 / AMD RX 5600 or better)
- **Storage** — 50GB free for models
- **Expected speed** — 1-3 seconds per query (7B model)

A dedicated GPU dramatically improves inference speed. NVIDIA GPUs use CUDA which has the broadest model support. AMD GPUs (RDNA2 and newer) are supported via ROCm on Linux and perform comparably for 7B models.

### Network server (serves multiple machines)
- Any machine meeting the recommended specs above
- Connected via wired ethernet to the local network
- Runs Ollama as a service, accessible at `http://server-ip:11434`
- Each machine on the network points its Sentinel config to the server IP
- One AI box serves an entire household or institution

### Recommended models by hardware

| Hardware         | Recommended Model  | Query Speed  |
|------------------|--------------------|--------------|
| CPU only         | llama3.2:3b        | 5-15 sec     |
| 6GB VRAM GPU     | llama3.1:8b        | 2-4 sec      |
| 8GB+ VRAM GPU    | llama3.1:8b        | 1-2 sec      |
| 16GB+ VRAM GPU   | mistral:7b         | <1 sec       |

---

## Security Model

- Sentinel runs as a dedicated system user with its own password
- All configuration files, wordlists, and binaries are owned by the sentinel system user
- Modifying or uninstalling any component requires the admin password
- Cooldown state is stored under the sentinel user — cannot be reset without the password
- Once installed, the setup cannot be bypassed by the regular user even with sudo

---

## Compared to existing solutions

| Tool          | Session limits | AI evaluation | Browser agnostic | Privacy | Bypass resistant |
|---------------|----------------|---------------|------------------|---------|------------------|
| Pi-hole       | ✗              | ✗             | ✓                | ✓       | Partial          |
| E2Guardian    | ✗              | ✗             | ✓                | ✓       | Partial          |
| DansGuardian  | ✗              | ✗             | ✓                | ✓       | Partial          |
| Firefox Guard | ✓              | ✓             | ✗                | ✓       | Partial          |
| **Sentinel**  | ✓              | ✓             | ✓                | ✓       | ✓                |

---

## Requirements

- Linux (Debian/Ubuntu based)
- Python 3.10+
- mitmproxy
- Ollama (optional, for local AI)
- Groq API key (optional, for cloud AI)

---

## Project Status

Early development. The filter pipeline and AI backend are based on battle-tested logic from [Firefox Guard](https://github.com/YOUR_USERNAME/firefox-guard).

---

## Philosophy

Unrestricted browser access is not a neutral default. Sentinel is built on the premise that intentional, time-limited, and monitored access is healthier than passive, unlimited browsing. The goal is not surveillance but structure.
