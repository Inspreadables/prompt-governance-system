---
instruction_id: template.deviation_log
version: 1.0.0
status: stable
owner: A. Verboon
last_reviewed: 2026-05-11
---

# Template: Afwijkingenlog (Deviation Log)

## Doel

Een lichtgewicht logboek per Space of agent waarin afwijkingen ten opzichte van het centrale register worden vastgelegd. Het log voedt de maandelijkse [`workflow.anti_rot_review_routine`](../03_workflows/anti_rot_review_routine.md) en maakt drift zichtbaar zonder dat er een volledige audit nodig is.

Het log is bewust kort. Eén regel per afwijking; één tabel per Space; één bestand of paragraaf onder de Space-bootstrap.

## Hoe te gebruiken

1. Maak per actieve Space één afwijkingenlog aan. Plaats het naast de Space-bootstrap of als sectie onderaan dezelfde Space-instructie.
2. Vul de **metadata** in voordat je de eerste review uitvoert.
3. Voeg tijdens elke maandelijkse review nieuwe regels toe aan de **afwijkingentabel**. Werk bestaande regels bij als de status verandert.
4. Werk de regel **Laatste review** bij na elke review, ook als er geen nieuwe afwijkingen zijn.
5. Volg de beslisregel uit [`workflow.anti_rot_review_routine`](../03_workflows/anti_rot_review_routine.md), sectie *Beslisregel*, om elke afwijking te classificeren.

## Metadata

- Naam van de Space of agent:
- Runtime (Perplexity Space, Claude Project, Custom GPT, anders):
- Eigenaar:
- Actieve adapter (bijvoorbeeld `adapter.perplexity_space@1.0.0`):
- Gebruikte bron-instructies en versies:
  - `global.quality_standards@<versie>`
  - `workflow.anti_rot_protocol@<versie>`
  - `workflow.prompt_audit_protocol@<versie>`
  - `template.space_audit_checklist@<versie>`
  - `<andere instructie-IDs>@<versie>`
- Eerste reviewdatum:
- Laatste review:
- Geplande volgende review:

## Afwijkingentabel

Eén regel per afwijking. Houd het kort: één korte zin per veld.

| # | Datum gezien | Instructie-ID (`<id>@<versie>`) | Beschrijving van de afwijking | Reden / context | Beslissing (`update_space` / `update_register` / `accept`) | Status (`open` / `in_uitvoering` / `opgelost` / `geaccepteerd`) | Eigenaar | Herzieningsdatum | Referentie (commit, PR, changelogregel) |
| - | ------------ | ------------------------------- | ----------------------------- | --------------- | ---------------------------------------------------------- | -------------------------------------------------------------- | -------- | ---------------- | -------------------------------------- |
| 1 | YYYY-MM-DD   | `<id>@<versie>`                 | <wat wijkt af>                | <waarom>        | `update_space`                                             | `open`                                                         | <naam>   | YYYY-MM-DD       | <commit/PR>                            |
| 2 | YYYY-MM-DD   | `<id>@<versie>`                 | <wat wijkt af>                | <waarom>        | `update_register`                                          | `in_uitvoering`                                                | <naam>   | YYYY-MM-DD       | <commit/PR>                            |
| 3 | YYYY-MM-DD   | `<id>@<versie>`                 | <wat wijkt af>                | <waarom>        | `accept`                                                   | `geaccepteerd`                                                 | <naam>   | YYYY-MM-DD       | n.v.t.                                 |

### Toelichting bij de kolommen

- **Datum gezien**: de dag waarop de afwijking is opgemerkt.
- **Instructie-ID (`<id>@<versie>`)**: de bron-instructie waar de afwijking tegen wordt afgezet. Volg [`governance.instruction_id_convention`](../00_register/instruction_id_convention.md) en gebruik de versie zoals in het manifest.
- **Beschrijving**: één zin over wat de Space anders doet dan de bron voorschrijft.
- **Reden / context**: bewust of onbewust ontstaan, platformbeperking, gebruikersfeedback, et cetera.
- **Beslissing**: één van drie waarden uit de beslisregel:
  - `update_space` — Space/runtime bijwerken naar de bron.
  - `update_register` — bronbestand en register aanpassen volgens [`governance.versioning_release_policy`](../00_register/versioning_and_release_policy.md).
  - `accept` — afwijking expliciet accepteren met herzieningsdatum.
- **Status**: huidige toestand van de afwijking. Een `geaccepteerd`-regel blijft staan tot de herzieningsdatum.
- **Eigenaar**: de persoon die actie neemt of het risico draagt.
- **Herzieningsdatum**: voor `update_*` de streefdatum waarop de actie af is; voor `accept` de datum waarop de acceptatie opnieuw wordt beoordeeld (maximaal drie maandelijkse reviews verder).
- **Referentie**: commit-hash, pull request, changelogregel of release-notes-verwijzing waarmee de actie traceerbaar is.

## Beslisregel (samenvatting)

| Situatie                                                                                                                  | Beslissing        |
| ------------------------------------------------------------------------------------------------------------------------- | ----------------- |
| Space wijkt af, register klopt nog.                                                                                       | `update_space`    |
| Afwijking is een verbetering voor meerdere Spaces, of het register is verouderd.                                          | `update_register` |
| Afwijking is bewust, platform- of klantspecifiek, niet generaliseerbaar, en de eigenaar draagt het risico.                | `accept`          |

De volledige uitleg en uitvoeringsstappen staan in [`workflow.anti_rot_review_routine`](../03_workflows/anti_rot_review_routine.md), sectie *Beslisregel toepassen*.

## Drempels voor escalatie

- **Drie of meer `accept`-regels open in één Space**: plan een volledige audit met [`workflow.prompt_audit_protocol`](../03_workflows/prompt_audit_protocol.md) en [`template.space_audit_checklist`](space_audit_checklist.md).
- **Eén afwijking blijft drie reviews op `open` staan**: escaleer naar de eigenaar van de bron-instructie en zet het op de eerstvolgende releaseplanning.
- **Herhaalde afwijkingen op hetzelfde instructie-ID over meerdere Spaces**: dat is een sterk signaal voor `update_register`, niet voor herhaaldelijke `update_space`-acties.

## Reviewregels per maand

Aan het einde van elke review:

- Vul **Laatste review** in op de datum van vandaag.
- Vul **Geplande volgende review** in op +1 maand.
- Werk frontmatter `last_reviewed` bij in elk bronbestand dat is aangepast.
- Werk `00_register/master_register.csv` bij voor elke gewijzigde instructie.
- Voeg een regel toe in `99_changelog/changelog.md` als een wijziging het register raakt.
- Draai `python3 tools/validate_manifest.py` en los meldingen op.

## Verhouding tot andere instructies

- [`workflow.anti_rot_review_routine`](../03_workflows/anti_rot_review_routine.md) — gebruikt dit log als invulformat.
- [`workflow.anti_rot_protocol`](../03_workflows/anti_rot_protocol.md) — definieert de regels die dit log handhaaft.
- [`template.space_audit_checklist`](space_audit_checklist.md) — de diepere variant voor jaarlijkse of incidentele audits.
- [`global.quality_standards`](../01_global/quality_standards.md) — bepaalt de kwaliteitslat waaraan afwijkingen worden afgemeten.
- [`adapter.perplexity_space`](../05_agent_adapters/perplexity_space_adapter.md) — bepaalt hoe een Perplexity Space wordt bijgewerkt na een `update_space`-beslissing.
