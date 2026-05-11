---
instruction_id: adapter.github_copilot
version: 1.0.0
status: stable
owner: A. Verboon
last_reviewed: 2026-05-11
---

# Adapter: GitHub Copilot

## Doel

Deze adapter vertaalt het agent-onafhankelijke instructieregister naar concrete instructies voor GitHub Copilot in een repositorycontext. De adapter levert twee varianten:

- Een **minimale variant** voor een snelle repository-onboarding via een kort `.github/copilot-instructions.md` bestand.
- Een **uitgebreide variant** voor repositories waar Copilot Chat ook governance, audit en kwaliteitscontroles moet ondersteunen.

Beide varianten verwijzen expliciet naar de actuele v1-instructie-IDs in `00_register/instruction_manifest.yaml` en `00_register/master_register.csv`.

## Lagenmodel

Copilot leest instructies uit de repository zelf (bijvoorbeeld via `.github/copilot-instructions.md` of vergelijkbare aangewezen instructiebestanden). Houd de vier lagen strikt gescheiden:

| Laag        | Locatie                                                       | Eigenaar                         | Voorbeelden                                                                          |
| ----------- | ------------------------------------------------------------- | -------------------------------- | ------------------------------------------------------------------------------------ |
| **Bron**    | Dit register (`01_global/`, `02_roles/`, `03_workflows/`, `04_templates/`) | Registereigenaar (A. Verboon)   | `global.operating_principles`, `global.quality_standards`                            |
| **Adapter** | `05_agent_adapters/github_copilot_adapter.md`                 | Registereigenaar                 | Deze adapter zelf, met platform-specifieke instructies voor GitHub Copilot           |
| **Runtime** | `.github/copilot-instructions.md` in de doelrepository        | Repository-eigenaar              | De daadwerkelijk geplakte minimale of uitgebreide variant binnen één concrete repo   |
| **Audit**   | `04_templates/space_audit_checklist.md` + `99_changelog/changelog.md` | Auditor en registereigenaar | Ingevulde checklist per repository, changelog-regels per wijziging                   |

Regel: platform-specifieke regels (bestandsnamen, paden, Copilot-instructiesyntax, taalspecifieke aanwijzingen) horen in deze adapter of in de runtime-laag, nooit in bronbestanden in `01_global/`, `02_roles/`, `03_workflows/` of `04_templates/`.

## Geschikte instructies voor repositorycontext

Niet elke instructie uit het register is even relevant voor een coderepository. Onderstaande lijst markeert welke instructie-IDs typisch nuttig zijn voor Copilot:

| Instructie-ID                              | Geschikt voor repo? | Toelichting                                                                                  |
| ------------------------------------------ | ------------------- | -------------------------------------------------------------------------------------------- |
| `global.operating_principles`              | Ja                  | Geldt overal: bron boven runtime, modulariteit, traceerbaarheid.                              |
| `global.communication_style`               | Ja                  | Stijlrichting voor commit messages, PR-beschrijvingen en commentaar.                          |
| `global.quality_standards`                 | Ja                  | Kwaliteitslat voor code, documentatie en gegenereerde output.                                 |
| `workflow.anti_rot_protocol`               | Ja                  | Signaleert drift tussen runtime (de repo) en bron (dit register).                             |
| `workflow.prompt_audit_protocol`           | Optioneel           | Alleen relevant in repositories die zelf prompts of agentinstructies onderhouden.             |
| `role.prompt_analyst_manager_orchestrator` | Optioneel           | Alleen relevant in repositories die governance of promptbeheer als kerntaak hebben.           |
| `template.space_audit_checklist`           | Optioneel           | Alleen relevant bij audits van Spaces, projects of GPTs vanuit de repo.                       |
| `governance.*`                             | Alleen referentie   | Niet als runtime-instructie in code, wel als verwijzing voor naamgeving en versiebeheer.      |

Verwijs in een repository altijd via `instruction_id` (en optioneel `@versie`), niet via lange tekstkopieën. Houd de runtime-tekst zo kort mogelijk.

## Variant A: Minimale variant

Gebruik dit blok voor een repository die de basisprincipes van het register wil volgen zonder veel governance-tekst. Plak letterlijk in `.github/copilot-instructions.md` in de doelrepository.

```md
# Copilot Instructies (Prompt Governance System v1)

Deze repository volgt het externe Prompt Governance System als bron van waarheid.
Bron: https://github.com/ArieJanVerboon/prompt-governance-system

Actieve instructie-IDs (zie `00_register/instruction_manifest.yaml` voor versies):
- global.operating_principles
- global.communication_style
- global.quality_standards
- workflow.anti_rot_protocol
- adapter.github_copilot

Gedrag van Copilot in deze repo:
- Volg de geldende code- en documentatieconventies van deze repository.
- Schrijf compact, modulair en herbruikbaar; vermijd duplicatie.
- Genereer commit messages en PR-beschrijvingen in dezelfde taal en stijl als de bestaande historie.
- Markeer voorstellen die conflicteren met bestaande conventies expliciet.

Conflictregel: bij conflict tussen lokale repo-tekst en het externe register heeft het register prioriteit, tenzij de repo-eigenaar expliciet anders beslist en dit gelogd wordt.
```

## Variant B: Uitgebreide variant

Gebruik dit blok in repositories waar Copilot ook governance, audit en kwaliteitsbewaking ondersteunt (bijvoorbeeld documentatierepositories, instructieregisters of repositories met agent-bootstraps). Plak letterlijk in `.github/copilot-instructions.md`.

```md
# Copilot Instructies — Uitgebreide variant (Prompt Governance System v1)

## 1. Bron van waarheid

Deze repository is een runtime-omgeving voor instructies uit het Prompt Governance System.
Bron: https://github.com/ArieJanVerboon/prompt-governance-system
Bronpaden: `00_register/instruction_manifest.yaml`, `00_register/master_register.csv`.

Wijzig nooit inhoudelijk in deze repository zonder dat de wijziging ook in het register landt.

## 2. Actieve instructie-IDs (v1)

- global.operating_principles
- global.communication_style
- global.quality_standards
- workflow.anti_rot_protocol
- workflow.prompt_audit_protocol
- role.prompt_analyst_manager_orchestrator
- template.space_audit_checklist
- adapter.github_copilot

Verwijs altijd via instructie-ID en versie, niet via gedupliceerde tekst.

## 3. Gedrag in deze repository

- Volg `global.operating_principles`: bron boven runtime, modulariteit, traceerbaarheid.
- Houd je aan `global.quality_standards`: herbruikbaar, traceerbaar, concreet, onderhoudbaar, agent-neutraal.
- Bij conflicterende aanwijzingen tussen bestanden: het register en deze instructie hebben voorrang boven losse opmerkingen in code.
- Schrijf commit messages en PR-beschrijvingen in dezelfde taal en stijl als de bestaande historie.

## 4. Lagenmodel (bron, adapter, runtime, audit)

Splits elk voorstel en elke wijziging expliciet in vier lagen:
- **Bron**: behoort dit in `01_global/`, `02_roles/`, `03_workflows/` of `04_templates/`?
- **Adapter**: behoort dit in `05_agent_adapters/<platform>_adapter.md`?
- **Runtime**: behoort dit in `.github/copilot-instructions.md` of de repository-instructie zelf?
- **Audit**: behoort dit in `template.space_audit_checklist` en `99_changelog/changelog.md`?

Geen platform-specifieke syntax of UI-gedrag in bronbestanden; dat hoort in de adapterlaag.

## 5. Workflows

- Bij drift, duplicatie of stille lokale wijzigingen: volg `workflow.anti_rot_protocol`.
- Bij audits van instructies of bootstraps in deze repository: volg `workflow.prompt_audit_protocol`.
- Bij outputkwaliteit: toets aan `global.quality_standards`.

## 6. Terugkoppeling naar het register

Elke inhoudelijke afwijking of verbetering volgt deze procedure:
1. Beschrijf de afwijking in één zin (wat wijkt af van welk instructie-ID).
2. Bepaal de juiste laag (bron, adapter, runtime, audit).
3. Stel een concrete wijziging voor in manifest, masterregister of het betreffende bronbestand.
4. Stel een changelog-regel voor in `99_changelog/changelog.md`.
5. Pas in de repository pas tekst aan nadat de registerwijziging is doorgevoerd (of gelijktijdig).

## 7. Conflictregel

Bij conflict tussen lokale repo-tekst en het externe register heeft het register prioriteit, tenzij de repo-eigenaar expliciet anders beslist en de reden in de PR-beschrijving documenteert.

## 8. Reviewcadans

- Maandelijkse review tegen het masterregister (`workflow.anti_rot_protocol`).
- Eigenaar en `last_reviewed` zichtbaar in deze instructie.
- Bij twijfel over actualiteit: doe eerst een audit met `template.space_audit_checklist` voordat nieuwe Copilot-instructies worden toegevoegd.
```

## Beperkingen van GitHub Copilot

- Copilot leest alleen bestanden die expliciet als instructie zijn aangewezen (zoals `.github/copilot-instructions.md`) of die als context bij een prompt worden aangeleverd; het register zelf wordt niet automatisch geladen.
- Houd de runtime-tekst kort en verwijs naar instructie-IDs in plaats van volledige bronbestanden over te nemen.
- Update bij elke registerwijziging het runtime-bestand handmatig, of plan dit in de maandelijkse review.
- Copilot kent geen native versie-pinning op instructie-IDs; noteer de gewenste versie expliciet in de runtime-tekst (bijvoorbeeld `adapter.github_copilot@1.0.0`).

## Onderhoud van deze adapter

- Eigenaar: A. Verboon.
- Reviewcadans: maandelijks, samen met de bronbestanden waarnaar deze adapter verwijst.
- Wijzigingen volgen semver en worden gelogd in `99_changelog/changelog.md`.
