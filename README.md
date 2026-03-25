# Negotiation Simulator

Ein KI-gestützter Prototyp zur Verhandlungsvorbereitung und -simulation — vollständig im Terminal, ohne App oder Framework.

---

## Konzept

Drei Agenten, drei Phasen:

1. **Preparation Agent** — führt interaktiv durch Lewickis Vorbereitungsschritte und speichert das Ergebnis als `.md`-Datei. Diese Datei ist gleichzeitig deine echte Verhandlungsvorbereitung für die Praxis und der Kontext-Input für die Simulation.

2. **Opponent Agents** — simulieren die Gegenseite auf Basis deiner Vorbereitung. Vier Typen, theoretisch verankert, austauschbar:
   - **Hardball** — kompetitiv, maximiert eigene Gewinne, setzt unter Druck
   - **Cooperative** — sucht Win-win, transparent, kooperativ
   - **Skeptical** — vorsichtig, risikoavers, fordert Belege
   - **Analytical** — datengetrieben, detailorientiert, logisch

3. **Coach Agent** — gibt nach der Simulation strukturiertes Feedback nach den vier Harvard-Prinzipien, BATNA-Nutzung und Strategie-Gegner-Fit.

---

## Technisches

Alles läuft über **Claude Code** im Terminal. Die `CLAUDE.md` im Root orchestriert den Workflow.

Die `.md`-Dateien in `agents/` sind gleichzeitig Dokumentation und lauffähige Agenten-Definitionen — kein Framework, keine App-Schicht dazwischen.

Die Struktur ist so gebaut, dass daraus später ein **MCP-Server** oder eine **Teams-Integration** entstehen kann, ohne alles umzubauen.

---

## Workflow

```
1. Preparation Agent starten
   → interaktive Vorbereitung nach Lewicki
   → Ergebnis wird in outputs/ gespeichert

2. Opponent Agent wählen
   → Simulation auf Basis der Vorbereitung
   → freie Verhandlung im Dialog

3. Coach Agent starten
   → strukturiertes Feedback
   → Harvard-Prinzipien, BATNA, Strategie-Fit
```

---

## Projektstruktur

```
negotiation-simulator/
├── CLAUDE.md                          # Workflow-Orchestrierung
├── README.md
├── .env.example
├── .gitignore
├── requirements.txt
├── python.instructions.md
├── agents.instructions.md
│
├── agents/
│   ├── preparation.md                 # Preparation Agent
│   ├── opponent_cooperative.md        # Opponent: kooperativ
│   ├── opponent_hardball.md           # Opponent: kompetitiv
│   ├── opponent_skeptical.md          # Opponent: skeptisch
│   ├── opponent_analytical.md         # Opponent: analytisch
│   └── coach.md                       # Coach Agent (Feedback)
│
├── outputs/                           # Gespeicherte Vorbereitungen
│   └── .gitkeep
│
├── data/
│   └── sample_cases.json              # Beispiel-Szenarien
│
└── .github/
    ├── copilot-instructions.md
    ├── agents/
    │   ├── planner.agent.md
    │   └── builder.agent.md
    └── prompts/
        └── bootstrap-negotiation-prototype.prompt.md
```

---

## Voraussetzungen

- [Claude Code](https://claude.ai/code) installiert und eingerichtet
- Anthropic API Key (in `.env` konfiguriert)

```bash
cp .env.example .env
# ANTHROPIC_API_KEY eintragen
```

---

## Theoretischer Rahmen

- **Vorbereitung**: Lewicki et al. — *Negotiation* (Interessen, Ziele, BATNA, Prioritäten)
- **Feedback**: Fisher & Ury — *Getting to Yes* (Harvard-Prinzipien)
- **Opponent-Typen**: Verhandlungsstilmodelle (kompetitiv, kooperativ, analytisch, skeptisch)
