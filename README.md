# Negotiation Simulator

Ein KI-gestützter Prototyp zur Verhandlungsvorbereitung und -simulation — vollständig über Claude Code, ohne App oder Framework.

---

## Konzept

Drei Agenten, drei Phasen:

1. **Preparation Agent** — führt interaktiv durch den 10-Schritt-Planungsprozess nach Lewicki et al. und speichert das Ergebnis als `.md`-Datei. Diese Datei ist gleichzeitig echte Verhandlungsvorbereitung für die Praxis und Kontext-Input für die Simulation.

2. **Opponent Agents** — simulieren die Gegenseite auf Basis der Vorbereitung. Zwei Typen, direkt aus der Verhandlungstheorie hergeleitet:
   - **Distributiver Verhandler** — positionsorientiert, Nullsummen-Logik, Anchoring, Zeitdruck (Lewicki et al.)
   - **Integrativer Verhandler** — interessenbasiert, Win-Win-Logik, Harvard-Prinzipien (Fisher & Ury)
   
   Der Kommunikationsstil des Gegners wird aus der Vorbereitung (Schritt 8) geladen und in den jeweiligen Agenten eingespeist.

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
   → interaktive Vorbereitung nach Lewicki et al.
   → Ergebnis wird in outputs/ gespeichert

2. Opponent Agent wählen
   → distributiv oder integrativ
   → Kommunikationsstil aus Schritt 8 wird automatisch geladen
   → freie Verhandlung im Dialog

3. Coach Agent starten
   → strukturiertes Feedback
   → Harvard-Prinzipien, BATNA-Awareness, Strategie-Gegner-Fit
```

---

## Projektstruktur

```
negotiation-simulator/
├── CLAUDE.md                          # Workflow-Orchestrierung
├── README.md
├── .env.example
├── .gitignore
│
├── agents/
│   ├── preparation.md                 # Preparation Agent (Lewicki 9 Schritte)
│   ├── opponent_distributive.md       # Distributiver Verhandler
│   ├── opponent_integrative.md        # Integrativer Verhandler
│   └── coach.md                       # Coach Agent (Feedback)
│
├── outputs/                           # Gespeicherte Vorbereitungen
│   └── .gitkeep
│
└── data/
    └── sample_cases.json
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

- **Vorbereitung**: Lewicki et al. — *Negotiation* (10-Schritt-Planungsprozess, BATNA, ZOPA, Bargaining Mix)
- **Gegnertypen**: Lewicki et al. — distributive vs. integrative Verhandlungsführung
- **Feedback**: Fisher & Ury — *Getting to Yes* (Harvard-Prinzipien)
