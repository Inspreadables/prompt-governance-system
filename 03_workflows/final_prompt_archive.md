---
id: workflow.final_prompt_archive
version: 1.0.0
status: draft
applies_to: [perplexity_space, claude_project]
---

# Workflow: Finale prompt archiveren

**Doel:** Archiveer alleen de **finale** prompt van een document na meerdere correcties. Tussenliggende prompts zijn ruis.

## Trigger

Gebruiker typt in de chat:
- `akkoord, archiveer`
- `finale versie`
- `archiveer dit document`

## Uitvoering door de agent

1. **Detecteer de meest recente prompt** uit de conversatiehistorie.
2. **Negeer alle eerdere prompts** (die horen bij eerdere versies/correcties).
3. **Verzamel metadata:**
   - Documentnaam (uit context of vraag indien ontbrekend)
   - Project/space naam
   - Datum/tijd
4. **Maak een GitHub issue aan** in de daarvoor bestemde repository (bijv. `Inspreadables/documentprompt-archief` — pas aan naar eigen inrichting).
   - Titel: `[YYYY-MM-DD] [Project] Finale prompt: [documentnaam]`
   - Body: bevat de **volledige prompt** en de metadata.
5. **Optioneel:** Als er een `save-session.sh` script bestaat, roep het aan om ook een lokale kopie te maken.
6. **Bevestig aan de gebruiker:** `✅ Gearchiveerd in issue #<nummer>`

## Uitzonderingen

| Situatie | Actie |
|----------|-------|
| Gebruiker zegt `archiveer volledige chat` | Bewaar **ook het antwoord** van de AI (niet alleen de prompt). |
| Geen documentnaam duidelijk | Vraag gebruiker: "Voor welk document moet ik deze prompt archiveren?" |
| Eerste versie zonder correcties | Nog steeds alleen de prompt (antwoord is niet leidend). |

## Integratie met andere systemen

- **Backup repo** (`Inspreadables/Backup`): Wordt gebruikt via `save-session.sh` voor lokale/gearchiveerde kopieën.
- **Prompt Governance System (deze repo):** Deze workflow is zelf onderdeel van het PGS.

## Versiegeschiedenis

- 1.0.0 (2026-06-15) — Eerste draft, alleen finale prompt, GitHub issue als primaire bestemming.

## Zie ook

- `adapter.perplexity_space` (voegt trigger toe aan Perplexity)
- `anti_rot_review_routine` (maandelijkse check of deze workflow nog klopt) 
