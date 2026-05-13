---
instruction_id: template.adapter
version: 1.0.0
status: stable
owner: A. Verboon
last_reviewed: 2026-05-13
---

# Adapter-template

Gebruik dit template als startpunt voor een nieuwe `adapter.*`-instructie in `05_agent_adapters/`. Elke adapter vertaalt het agent-onafhankelijke instructieregister naar een concrete agentomgeving (bijvoorbeeld Perplexity Space, Claude Project, Custom GPT, GitHub Copilot, Cursor). Het template borgt dat elke adapter dezelfde structuur, lagen en metadata heeft als bestaande adapters (`adapter.perplexity_space@1.0.0`, `adapter.claude_project@1.0.0`, `adapter.custom_gpt@1.0.0`).

Verplichte referenties:

- [`governance.instruction_id_convention`](../00_register/instruction_id_convention.md) — naamgeving en prefixen.
- [`governance.versioning_release_policy`](../00_register/versioning_and_release_policy.md) — versies, statussen en koppeling tussen adapterversie en bronversie.
- [`governance.manifest_validation_specification`](../00_register/manifest_validation_specification.md) — validatieregels (inclusief `applies_to`-vocabulaire, sectie C9).
- [`governance.cost_token_control`](../00_register/cost_token_control.md) — lean mode-werkwijze bij het bouwen van nieuwe adapters.

## Stappen voordat je dit template gebruikt

1. Kies een unieke ID volgens `adapter.<naam>` (snake_case, Engels, singular).
2. Maak het bestand `05_agent_adapters/<naam>_adapter.md` aan.
3. Vul de frontmatter in met status `draft` zolang de adapter nog niet productiegeschikt is.
4. Registreer de adapter in `00_register/instruction_manifest.yaml` en `00_register/master_register.csv` met dezelfde versie en status.
5. Werk `README.md` bij in de adaptertabel.
6. Voeg een changelogregel toe in `99_changelog/changelog.md`.

---

## Frontmatter (verplicht)

```markdown
---
instruction_id: adapter.<naam>
version: 0.1.0
status: draft
owner: <naam eigenaar>
last_reviewed: YYYY-MM-DD
---
```

Promoveer naar `1.0.0`/`stable` zodra de adapter twee varianten heeft (compact en uitgebreid), is gevalideerd met `tools/validate_manifest.py` en minstens één keer in een echte Space of project is gebruikt.

## Sectie-opbouw (verplicht)

### 1. Titel en doel

```markdown
# Adapter: <Doelomgeving>

## Doel

Deze adapter vertaalt het agent-onafhankelijke instructieregister naar concrete,
direct kopieerbare instructies voor <doelomgeving>. De adapter levert twee varianten:

- Een **compacte bootstrap** voor een werkende <doelomgeving> met minimale tekst.
- Een **uitgebreide beheerder/manager-versie** voor instanties die ook governance,
  audit en terugkoppeling naar het register actief moeten ondersteunen.

Beide varianten verwijzen expliciet naar de actuele v1-instructie-IDs in
`00_register/instruction_manifest.yaml` en `00_register/master_register.csv`.
```

### 2. Lagenmodel (verplicht)

Houd vier lagen strikt gescheiden. Kopieer en pas alleen de kolom **Locatie** aan voor de doelomgeving.

| Laag        | Locatie                                                                             | Eigenaar                  | Voorbeelden                                                              |
| ----------- | ----------------------------------------------------------------------------------- | ------------------------- | ------------------------------------------------------------------------ |
| **Bron**    | Dit register (`01_global/`, `02_roles/`, `03_workflows/`, `04_templates/`)          | Registereigenaar          | `global.operating_principles`, `role.prompt_analyst_manager_orchestrator` |
| **Adapter** | `05_agent_adapters/<naam>_adapter.md`                                               | Registereigenaar          | Deze adapter zelf                                                        |
| **Runtime** | De daadwerkelijke <doelomgeving>-instructie                                          | Eigenaar van de runtime   | De geplakte bootstrap- of beheerderversie binnen één concrete instance   |
| **Audit**   | `04_templates/space_audit_checklist.md` + `99_changelog/changelog.md`               | Auditor en registereigenaar | Ingevulde checklist per instance, changelog-regels per wijziging        |

Regel: tekst in de runtime-laag mag inhoudelijk niet afwijken van de bron. Wijkt het toch af, dan volgt terugkoppeling via de feedbackprocedure (sectie 6).

### 3. Actieve v1-instructie-IDs

Lijst de instructie-IDs die deze adapter canoniek doorgeeft. Verwijs in de runtime altijd via `instruction_id` (en optioneel `@versie`), nooit via lange tekstkopieën.

Standaardset voor een rol-adapter:

- `global.operating_principles`
- `global.communication_style`
- `global.quality_standards`
- `role.<rolnaam>`
- `workflow.prompt_audit_protocol`
- `workflow.anti_rot_protocol`
- `workflow.anti_rot_review_routine`
- `template.space_audit_checklist`
- `template.deviation_log`
- `adapter.<naam>` (deze adapter zelf)

Voor repository-context-adapters (Copilot, Cursor): kies de subset die in een coderepo zinvol is en geef expliciet aan welke instructies bewust niet zijn opgenomen.

### 4. Variant A — Compacte bootstrap (verplicht)

Een direct kopieerbaar blok van maximaal ongeveer 30 regels. Bevat:

- Titelregel met versie van het register.
- Pointer naar de repository-URL.
- Lijst actieve instructie-IDs.
- Een korte regel voor terugkoppeling van afwijkingen (verwijs naar sectie 6).

```md
# <Doelomgeving> Bootstrap (Prompt Governance System v1)

Deze <doelomgeving> gebruikt het externe Prompt Governance System als bron van waarheid.
Bron: https://github.com/ArieJanVerboon/prompt-governance-system

Actieve instructie-IDs (zie `00_register/instruction_manifest.yaml` voor versies):
- global.operating_principles
- global.communication_style
- global.quality_standards
- role.<rolnaam>
- workflow.prompt_audit_protocol
- workflow.anti_rot_protocol
- template.space_audit_checklist

Bij twijfel: volg het bronregister; rapporteer afwijkingen via de feedbackprocedure in `adapter.<naam>`.
```

### 5. Variant B — Uitgebreide beheerder/manager-versie (verplicht)

Een uitgebreid blok voor instanties die ook governance, audit en terugkoppeling actief ondersteunen. Bevat minimaal:

- Volledige lijst actieve instructie-IDs inclusief audit- en deviation-templates.
- Concrete voorbeeldopdrachten of -workflows die in deze omgeving worden ondersteund.
- Verwijzing naar `template.space_audit_checklist` voor periodieke audit.
- Verwijzing naar `template.deviation_log` voor afwijkingenlog.
- Verwijzing naar `workflow.anti_rot_review_routine` voor maandelijkse review.

### 6. Terugkoppeling van afwijkingen naar het register

Beschrijf het pad waarlangs runtime-afwijkingen terugkomen in het register:

1. Eigenaar van de runtime documenteert afwijking in lokaal `template.deviation_log`.
2. Bij maandelijkse review wordt de beslisregel uit `workflow.anti_rot_review_routine` toegepast: **Space bijwerken**, **register bijwerken** of **afwijking expliciet accepteren**.
3. Bij keuze "register bijwerken": open een pull request volgens `CONTRIBUTING.md`.
4. Pas de adapter aan en bump versie volgens `governance.versioning_release_policy`.

### 7. Platform-specifieke notities (optioneel maar aanbevolen)

Een korte sectie met regels die alleen voor deze runtime gelden:

- Maximale instructielengte of tokenlimieten.
- Conventies voor knowledge files, project files, conversatiestarters of vergelijkbare platform-features.
- Eventuele beperkingen in opmaak (bijvoorbeeld geen YAML-frontmatter ondersteund).
- Eventuele integraties met externe tools binnen het platform.

### 8. Metadata-eisen (verplicht)

- `instruction_id` volgt `adapter.<naam>` en is uniek in manifest en masterregister.
- `version` volgt semver; `MAJOR` bij scope-wijziging, `MINOR` bij toevoeging van varianten of secties, `PATCH` bij redactionele correcties.
- `status` is `draft` tot Variant A en Variant B beide compleet en getest zijn; daarna `review` of `stable`.
- `applies_to` in het manifest bevat één geldige waarde uit het toegestane vocabulaire (zie `governance.manifest_validation_specification`, sectie C9).
- `last_reviewed` is een ISO-datum (`YYYY-MM-DD`).

### 9. Validatie

Voer voor elke wijziging uit:

```bash
python3 tools/validate_manifest.py
```

Verwacht resultaat: 0 fouten en 0 waarschuwingen. Bij waarschuwingen: los ze op of motiveer in de PR-beschrijving waarom een waarschuwing blijft staan.

## Checklist (samenvattend)

- [ ] Frontmatter met alle verplichte velden ingevuld.
- [ ] Lagenmodel-tabel ingevuld voor de doelomgeving.
- [ ] Lijst actieve instructie-IDs is compleet en consistent met `instruction_manifest.yaml`.
- [ ] Variant A (compacte bootstrap) aanwezig en getest.
- [ ] Variant B (uitgebreide versie) aanwezig en getest.
- [ ] Feedbackprocedure beschreven.
- [ ] Platform-specifieke notities toegevoegd indien relevant.
- [ ] Manifest en masterregister bijgewerkt met identieke `version`, `status`, `path`.
- [ ] Adaptertabel in `README.md` bijgewerkt.
- [ ] Changelogregel toegevoegd in `99_changelog/changelog.md`.
- [ ] `python3 tools/validate_manifest.py` rapporteert 0 fouten en 0 waarschuwingen.
