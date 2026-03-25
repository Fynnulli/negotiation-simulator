# Negotiation Simulator — Claude Code Einstiegspunkt

Dieses Repository enthält einen KI-gestützten Verhandlungssimulator,
der auf wissenschaftlicher Verhandlungstheorie basiert. Der Simulator
läuft vollständig über Claude Code — kein Frontend, kein Framework.

---

## Workflow: Drei Phasen

### Phase 1 — Vorbereitung (`/start`)
Lade `agents/preparation.md` und führe den Nutzer interaktiv durch
alle 9 implementierten Vorbereitungsschritte nach Lewicki et al. (2010,
S. 119 ff.). Schritt 10 (Protocol) ist bewusst ausgeklammert (MVP-Scope).

Speichere das Ergebnis als:
`outputs/preparation_YYYY-MM-DD_[topic].md`

Diese Datei ist Pflicht-Input für Phase 2.

### Phase 2 — Simulation (`/simulate`)
1. Frage den Nutzer welchen Gegnertyp er simulieren möchte
2. Lade den entsprechenden `agents/opponent_*.md`
3. Lade die zuletzt erstellte `outputs/preparation_*.md` als Kontext
4. Führe die Verhandlungssimulation durch (multi-turn)
5. Der Nutzer beendet mit `/done`

### Phase 3 — Feedback (`/feedback`)
Lade `agents/coach.md` und übergib den vollständigen
Simulationsverlauf sowie den preparation output.
Erzeuge strukturiertes Feedback nach den Harvard-Prinzipien.

---

## Verfügbare Befehle

| Befehl | Aktion |
|--------|--------|
| `/start` | Startet Phase 1 — Vorbereitung |
| `/simulate` | Startet Phase 2 — setzt preparation output voraus |
| `/feedback` | Startet Phase 3 — setzt Simulationsverlauf voraus |
| `/agents` | Listet verfügbare Gegnertypen mit kurzer Beschreibung |
| `/done` | Beendet die laufende Simulation und leitet zu Phase 3 |

---

## Verfügbare Gegnertypen

| Agent | Strategie | Theoretische Basis |
|-------|-----------|--------------------|
| `opponent_hardball` | Distributiv | Lewicki et al. (2010), Kap. 2–3 |
| `opponent_cooperative` | Integrativ | Fisher & Ury (1981); Lewicki et al. (2010), Kap. 4 |
| `opponent_skeptical` | Gemischt | Lewicki et al. (2010), S. 131 ff. |
| `opponent_analytical` | Integrativ/gemischt | Lewicki et al. (2010), S. 123 f. |

---

## Hinweise

- Phase 1 muss vor Phase 2 abgeschlossen sein
- Der preparation output wird automatisch als Kontext geladen
- Alle outputs werden in `outputs/` gespeichert und nicht committed
