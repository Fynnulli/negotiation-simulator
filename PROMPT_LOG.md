# 📌 Projektzusammenfassung: KI-basierte Simulation von Verhandlungsszenarien

---

# 1. Projektübersicht

## Ziel des Projekts
Entwicklung eines **lokalen Prototyps zur KI-gestützten Simulation von Verhandlungsszenarien**, um die **Verhandlungsvorbereitung zu verbessern**.

Der Prototyp soll:
- Verhandlungssituationen simulieren
- verschiedene Gegnertypen darstellen
- Feedback zur eigenen Verhandlungsstrategie geben
- auf **wissenschaftlicher Verhandlungstheorie basieren**

## Kernidee
Ein System, das:
1. ein Verhandlungsszenario erstellt  
2. eine Gegenseite simuliert  
3. den Verlauf analysiert  
4. Verbesserungsvorschläge liefert  

👉 Ziel: **Trainings- und Entscheidungsunterstützungssystem für Verhandlungen**

---

# 2. Aktueller Stand

## ✅ Fertig umgesetzt

### Projektstruktur
- Vollständige Ordnerstruktur erstellt
- `.github` Copilot-Konfiguration eingerichtet
- Markdown-Agenten und Prompt-Dateien angelegt
- Python-MVP implementiert
- Streamlit UI vorhanden

### Komponenten

#### 🔹 Markdown-basierte Agenten
- `opponent_cooperative.md`
- `opponent_hardball.md`
- `opponent_skeptical.md`
- `opponent_analytical.md`
- `reflection_agent.md`

#### 🔹 Prompt-Dateien
- `scenario_builder.md`
- `feedback_template.md`

#### 🔹 Python-Module
- `utils/prompt_loader.py`
- `utils/llm_client.py`
- `utils/simulator.py`

#### 🔹 UI
- `app.py` (Streamlit)

#### 🔹 Konfiguration
- `.env.example`
- `requirements.txt`
- `.gitignore`

---

## 🔄 Letzter Schritt

👉 Integration von **Verhandlungstheorie in Markdown-Agenten**

Wir haben begonnen:
- Harvard-Konzept
- BATNA
- Verhandlungsstile
- Taktiken

👉 Ziel: Agenten = **theoriegestützte Verhaltensmodelle**

---

# 3. Wichtige Entscheidungen

## Architekturentscheidungen

### 1. Markdown-first Ansatz
**Warum:**
- Verhalten nicht im Code, sondern in Markdown
- hohe Transparenz
- einfach anpassbar
- wissenschaftlich gut erklärbar

👉 zentrale Idee des Projekts

---

### 2. Trennung von Logik und Verhalten

| Ebene | Aufgabe |
|------|--------|
| Markdown | Verhalten / Strategie |
| Python | Orchestrierung |
| LLM | Simulation |
| Streamlit | UI |

---

### 3. Modularer Aufbau

- `prompt_loader` → lädt Markdown
- `llm_client` → abstrahiert LLM
- `simulator` → orchestriert Flow
- `app.py` → UI

👉 Ziel: **Austauschbarkeit & Erweiterbarkeit**

---

### 4. LLM-Wahl

**Entscheidung:**
- OpenAI API (`gpt-5.4-mini` empfohlen)

**Warum:**
- stabil
- einfach integrierbar
- Copilot-kompatibel

👉 Gemini optional, aber nicht initial integriert

---

### 5. Lokaler Prototyp statt Deployment

**Warum:**
- Fokus auf Hausarbeit
- Nachvollziehbarkeit
- keine Infrastruktur notwendig

---

### 6. Single-Turn Simulation (MVP)

**Warum:**
- reduziert Komplexität
- schneller Proof of Concept

---

# 4. Offene Aufgaben

## 🔴 Hochpriorität

### 1. Agenten finalisieren (mit Theorie)
- Harvard-Konzept integrieren
- BATNA explizit einbauen
- klare Verhandlungsstile definieren
- Taktiken strukturieren

---

### 2. Scenario Builder verbessern
- Verhandlungstyp (integrativ vs distributiv)
- Machtverhältnis
- Risiken
- Gegnerannahmen

---

### 3. Reflection Agent erweitern
- strukturierte Bewertung:
  - Strategie
  - Argumentation
  - BATNA-Nutzung
  - Kommunikation
  - Anpassungsfähigkeit

---

### 4. System testen
- mehrere Szenarien durchspielen
- Unterschiede zwischen Agents prüfen
- Feedbackqualität validieren

---

## 🟡 Mittelfristig

- Multi-Turn Verhandlungen
- Vergleich verschiedener Strategien
- Logging / Speicherung
- mehrere LLMs (OpenAI + Gemini)

---

## 🟢 Optional

- Deployment (Streamlit Cloud)
- UI verbessern
- Visualisierung der Ergebnisse

---

# 5. Wichtiger Kontext

## Technologiestack

- Python
- Streamlit
- OpenAI API
- Markdown-basierte Agentensteuerung
- VS Code + Copilot mit Custom Instructions

---

## Projektphilosophie

👉 **Nicht klassisch programmieren, sondern Verhalten definieren**

- keine Logik hart codieren
- stattdessen:
  - Rollen in Markdown
  - Verhalten durch Prompts

---

## Copilot Setup

### `.github/` Ordner

| Datei | Zweck |
|------|------|
| copilot-instructions.md | globale Regeln |
| agents/*.agent.md | Copilot Rollen |
| prompts/*.prompt.md | Wiederverwendbare Tasks |

👉 beeinflusst nur Entwicklung, nicht App

---

## Agenten-Konzept

### Drei Haupt-Agenten:

1. **Scenario Builder**
2. **Opponent Agent**
3. **Reflection Agent**

👉 bilden zusammen einen Trainingsloop

---

## System-Flow

```text
User Input
   ↓
Scenario Builder
   ↓
Opponent Agent
   ↓
Simulation
   ↓
Reflection Agent
   ↓
Feedback