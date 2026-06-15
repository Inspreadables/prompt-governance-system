---
instruction_id: workflow.final_prompt_archive
version: 1.0.0
status: draft
owner: A. Verboon
last_reviewed: 2026-06-15
applies_to: [perplexity_space, claude_project]
---
---

# Workflow: Finale prompt archiveren

**Doel:** Archiveer alleen de **finale** prompt van een document na meerdere correcties. Tussenliggende prompts zijn ruis.

## Trigger

Gebruiker typt in de chat:
- `akkoord, archiveer`
- `finale versie`
- `archiveer dit document`

## Uitvoering door de agent

1. **Detecteer de meest recente prompt** uit de conversatiehistorie. Negeer alle eerdere prompts (die horen bij eerdere versies/correcties).

2. **Verzamel metadata:** documentnaam (uit context of vraag indien ontbrekend), project/space naam, datum/tijd.

3. **Toon de finale prompt** en leg uit:  
   *"Deze prompt is de blauwdruk. Je kunt hiermee later het document opnieuw genereren."*

4. **Geef een directe link naar GitHub issues** (gebruik de repository `Inspreadables/documentprompt-archief`):  
   `https://github.com/Inspreadables/documentprompt-archief/issues/new?title=[YYYY-MM-DD]+[DOCUMENTNAAM]&body=##+Prompt%0A%0A[PLAK+HIER+DE+PROMPT]%0A%0A##+Metadata%0A-%20Space%3A%20[naam]%0A-%20Datum%3A%20[vandaag]`

5. **Vraag de gebruiker het issue-nummer terug te plakken:**  
   *"Na het aanmaken van het issue, kopieer het issue-nummer (bijv. #5) en plak het hier. Dan voeg ik het toe aan het printrapport."*

6. **Waarschuw de gebruiker nadrukkelijk:**  
   *"⚠️ **Let op:** Klik de link, plak de prompt in het `## Prompt`-veld, **controleer of de tekst er staat**, en klik **pas dan** op `Create`. Verstuur geen leeg issue."*

7. **Bevestig dat de chat verwijderd mag worden:**  
   *"Na het versturen mag je deze chat verwijderen. De prompt is veilig opgeslagen in GitHub."*



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
