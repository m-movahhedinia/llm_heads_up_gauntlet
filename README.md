![Status: Incomplete](https://img.shields.io/badge/Status-Incomplete-red)
# Multi-Agent LLM Heads Up Gauntlet
### ⚠️ **This is an incomplete and ongoing project.**
## Overview

This project is a **multi-agent game platform** designed to pit large language models (LLMs) against one another and against humans in a playful yet technically rigorous format. Inspired by the *Heads Up!* game, the system showcases advanced **agentic LLM orchestration**, **evaluation frameworks**, and **human-in-the-loop interaction**.

## 🎮 Game Concept

Two complementary modes highlight different aspects of LLM reasoning:

- **Heads Up! Mode**
    - A reference model or a human receives a word.
    - It generates hints.
    - Models being tested and possibly a human attempt to guess the word.
- **Reverse Mode (Flip the Script)**
    - Models being tested and possibly a human receive the word.
    - They generate hints.
    - The reference model or a human attempts to guess the word.

This dual structure allows evaluation of both **hint generation** and **hint interpretation** across diverse models and humans.

## 🏗️ System Architecture

### 1. Frontend Layer (React Web UI)

- **Features:**
    - User-friendly, visually appealing interface.
    - Leaderboard with live updates (human vs. models).
    - Model metadata per game (name, version, category such as *phi-4-small v1.2*).
    - Separate views for *Heads Up!* and *Flip the Script*.
    - Input selector:
        - Curated set (repeatable experiments).
        - Random generator (novel challenges).
        - Option to “promote” random inputs into curated set.
- **Grafana Integration:**
    - Pull leaderboard stats, drift/trend visualizations, and performance metrics via Grafana’s API.
    - Embed Grafana panels directly into the UI for real-time monitoring.

### 2. Game Orchestration Layer

- **Game Engine (Controller):**
    - Manages rounds, assigns roles, tracks scores.
- **Agent Manager:**
    - Spins up sub-agents for each participant.
    - Assigns tasks: “generate hint,” “make guess,” “judge correctness.”
- **Mode Switcher:**
    - Handles transitions between *Heads Up!* and *Flip the Script*.
- **Enhancements:**
    - Round replay feature.
    - Fairness module ensuring consistent hint distribution.

### 3. LLM & Agent Layer

- **Reference Model Agent:** Generates hints or guesses depending on mode.
- **Guessing Agents (LLMs + Human):** Interpret hints and output guesses with confidence scores.
- **Hinting Agents (LLMs + Human):** Generate hints for the reference model in reverse mode.
- **Judge Agent:** Evaluates correctness, creativity, and efficiency.
- **Model Config Control:**
    - Expose hyperparameters (temperature, top-k, top-p, max tokens) in UI.
    - Allow “agent personalities” via predefined config bundles.

### 4. Knowledge & Processing Layer

- **RAG Module:** Retrieve external knowledge (Wikipedia, arXiv, trivia datasets).
- **LLMLingua Module:** Compress hints to test robustness.
- **LangChain / LangGraph:** Orchestrate multi-agent workflows.
- **Pydantic / Pydantic AI:** Enforce structured outputs (TOON/JSON with fields like `hint`, `guess`, `confidence`).
- **Additional Tools:**
    - Dictionary/thesaurus for semantic hints.
    - Embedding-based similarity search.
    - Noise injection for resilience testing.

### 5. Evaluation & Metrics Layer

- **Core Metrics:**
    - Accuracy (correct guesses).
    - Creativity (novelty of hints).
    - Efficiency (number of hints needed).
    - Perplexity of hints (surprise factor).
    - Entropy of guesses (uncertainty quantification).
    - Calibration curves (confidence vs. correctness).
    - Drift detection (model version evolution).
    - Human vs. model agreement rate.
    - Latency metrics (time-to-first-hint, time-to-guess).
- **Visualization:**
    - Grafana dashboards for real-time monitoring.
    - Leaderboards, drift trends, calibration plots.

### 6. Infrastructure Layer

- **Backend Services:**
    - API endpoints for hint/guess submission.
    - Logging service for storing rounds.
- **Database:**
    - Stores words, hints, guesses, scores.
- **Model Registry:**
    - Tracks participating LLMs (e.g., GPT, Claude, Llama).
- **Infrastructure-as-Code (Terraform):**
    - Codify deployment of:
        - Model registry.
        - API gateway.
        - Database.
        - Grafana + Prometheus stack.
        - CI/CD pipeline.
- **Bonus:**
    - Containerize agents with Docker.
    - Orchestrate with Kubernetes for scalability.

## 🔄 Example Flows

### Heads Up! Mode

1. Word chosen → sent to Reference Model Agent.
2. Reference Model generates hint(s).
3. Guessing Agents (LLMs + human) receive hint(s).
4. Each outputs a guess + confidence.
5. Judge Agent evaluates correctness.
6. Scores logged → Grafana updates leaderboard.

### Flip the Script Mode

1. Word chosen → sent to Guessing Agents (LLMs + human).
2. Each generates hint(s).
3. Reference Model Agent receives hints.
4. Outputs guess + confidence.
5. Judge Agent evaluates correctness.
6. Scores logged → Grafana updates leaderboard.
