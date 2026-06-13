# Best Self-Hosted AI Gateway in 2026 (LiteLLM vs Bifrost vs TensorZero vs Kong)

*Last updated 2026-06-13 · Part of [Awesome AI Gateway](../README.md). [⭐ Star it](https://github.com/cuihuan/awesome-ai-gateway).*

If you want one OpenAI-compatible endpoint for every model — but on **your own infrastructure, with $0 markup** — you're choosing a self-hosted AI gateway. Here are the four that matter in 2026, and how to pick.

## Quick comparison

| Gateway | Language | Best at | Overhead | License | Stars |
|---|---|---|---|---|---|
| **LiteLLM** | Python | Breadth (100+ providers), features | moderate | MIT | ~50k |
| **Bifrost** | Go | Raw throughput | ~11µs @ 5k RPS¹ | Apache-2.0 | ~5.7k |
| **TensorZero** | Rust | Gateway + evals + observability | <1ms p99 @ 10k QPS¹ | Apache-2.0 | ~11.5k |
| **Kong AI Gateway** | Lua/Go | Enterprise K8s + mature plugins | low | Apache-2.0 | ~44k |

¹ Vendor-published benchmarks — treat cross-vendor "Nx faster" claims as marketing until independently reproduced.

## Pick by what you care about

- **Broadest features, fastest to adopt → LiteLLM.** The default. Virtual keys, budgets, load balancing, guardrails, 100+ providers. Python, huge community. Downside: it's feature-heavy and its broad surface has been a security target (see below).
- **Maximum throughput, minimal footprint → Bifrost.** Go, adaptive load balancing, cluster mode, claims ~11µs overhead. Pick it when the gateway must not be your bottleneck.
- **One binary for gateway + observability + evals → TensorZero.** Rust, <1ms p99, data stays in your ClickHouse. The most *opinionated* choice — it builds an optimization loop from your production data. This single feature is why it hit #1 GitHub Trending at launch.
- **Already run Kubernetes / need mature governance → Kong AI Gateway.** AI plugins (semantic caching, prompt guard, PII sanitization) on a battle-tested gateway. One less new service if Kong is already in your stack. (Higress and Apache APISIX are strong alternatives here.)

## Security: patch discipline matters more than the logo

Self-hosting means **you own the security**. Honest 2026 facts:

- **LiteLLM** had two serious CVEs — a pre-auth SQLi (CVE-2026-42208) and an unauth RCE on CISA's exploited list (CVE-2026-42271) — **both patched in v1.83.7**. It's fine *if* you pin to current stable, restrict egress, and never expose the admin panel publicly.
- **Bifrost / TensorZero**: no CVEs surfaced — but absence of found CVEs ≠ proven secure (less scrutiny).
- **Kong**: inherits Kong's mature, hardened auth/RBAC stack.

Full ★1–5 compliance/security/stability scores for 23 gateways: [gateway scorecard](../BENCHMARKS.md#part-4--gateway-scorecard-compliance--price--security--stability).

## Don't forget the model cost

The gateway is $0-markup; your bill is the **model**. Same 100K-token report: **$0.03 on DeepSeek vs $3.01 on GPT-5.5** (106×). A self-hosted gateway's biggest win is routing cheap-by-default and escalating only when needed — see the [computed cost tables](../BENCHMARKS.md).

## Verdict

- **Most teams → LiteLLM** (then tune for security).
- **Performance-critical → Bifrost or TensorZero.**
- **K8s / enterprise governance → Kong / Higress / Envoy AI Gateway.**

See all 50+ gateways organized by need, with decision tree and data:
👉 **[Awesome AI Gateway](https://github.com/cuihuan/awesome-ai-gateway)** · [interactive site](https://cuihuan.github.io/awesome-ai-gateway/)
