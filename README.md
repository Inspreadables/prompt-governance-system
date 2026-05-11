# Prompt Governance System

Agent-onafhankelijk instructieregister voor Spaces, agents, custom GPTs, Claude Projects en andere AI-uitvoeringsomgevingen.

## Doel

Deze repository is de bron van waarheid voor herbruikbare prompt-, rol-, workflow- en kwaliteitsinstructies. Individuele Spaces of agents bevatten alleen een korte bootstrap die naar deze instructies verwijst.

## Kernprincipes

- **Bron boven runtime**: de repo is leidend; Spaces en agents zijn uitvoeringslagen.
- **Modulair ontwerp**: rollen, workflows, standaarden en adapters staan los van elkaar.
- **Versiebeheerbaar**: elke instructie heeft een eigen ID, versie en reviewstatus.
- **Agent-onafhankelijk**: instructies zijn geschreven in generieke Markdown en kunnen via adapters worden vertaald naar specifieke tools.
- **Anti-rot**: lokale wijzigingen in een Space worden teruggevoerd naar dit register of expliciet als afwijking gemarkeerd.

## Structuur

```text
00_register/       Manifesten en masterregisters
01_global/         Generieke werkprincipes en kwaliteitsstandaarden
02_roles/          Herbruikbare agentrollen
03_workflows/      Standaardprocessen en protocollen
04_templates/      Invulformats voor Spaces, briefs en taken
05_agent_adapters/ Vertalingen naar specifieke agentomgevingen
99_changelog/      Wijzigingsgeschiedenis
```

## Startpunt

1. Werk eerst `00_register/instruction_manifest.yaml` bij.
2. Kies de benodigde rol uit `02_roles/`.
3. Combineer die rol met een workflow uit `03_workflows/`.
4. Gebruik een adapter uit `05_agent_adapters/` om de instructies naar een specifieke agentomgeving te vertalen.
5. Registreer elke actieve implementatie in `00_register/master_register.csv`.

## Adapters

De repo bevat adapters voor verschillende agentomgevingen in `05_agent_adapters/`. Elke adapter levert minimaal een minimale en (waar zinvol) een uitgebreide variant en verwijst expliciet naar de actuele instructie-IDs in het manifest.

| Adapter                                                          | Instructie-ID              | Status | Doelomgeving                       |
| ---------------------------------------------------------------- | -------------------------- | ------ | ---------------------------------- |
| [Perplexity Space](05_agent_adapters/perplexity_space_adapter.md) | `adapter.perplexity_space` | stable | Perplexity Spaces                  |
| [Claude Project](05_agent_adapters/claude_project_adapter.md)     | `adapter.claude_project`   | draft  | Anthropic Claude Projects          |
| [Custom GPT](05_agent_adapters/custom_gpt_adapter.md)             | `adapter.custom_gpt`       | draft  | OpenAI Custom GPTs                 |
| [GitHub Copilot](05_agent_adapters/github_copilot_adapter.md)     | `adapter.github_copilot`   | stable | GitHub Copilot in repositories     |
| [Cursor Rules](05_agent_adapters/cursor_rules_adapter.md)         | `adapter.cursor_rules`     | stable | Cursor in repositories             |

Platform-specifieke regels (bestandsnamen, syntax, IDE-gedrag) horen in de adapterlaag, niet in de bronbestanden in `01_global/`, `02_roles/`, `03_workflows/` of `04_templates/`.

## Conventies

- [Instructie-ID conventie](00_register/instruction_id_convention.md) — prefixes, naamgevingsregels, voorbeelden en relatie tot bestandspaden, versies, manifest en masterregister. Lees dit voordat je een nieuwe instructie toevoegt.
- [Versie- en releasebeleid](00_register/versioning_and_release_policy.md) — semver-regels (`MAJOR`/`MINOR`/`PATCH`), statusovergangen (`draft` → `review` → `stable` → `deprecated`), de verhouding tussen adapterversies en bronversies, hoe Spaces weten welke versie actief is en hoe releases worden gedocumenteerd. Gebruik bij grotere releases het [release-notes-template](04_templates/release_notes_template.md).

## Maandelijkse anti-rot review

Gebruik de [anti-rot reviewroutine](03_workflows/anti_rot_review_routine.md) om actieve Spaces en agents maandelijks in minder dan 30 minuten te controleren op drift. Houd per Space een [afwijkingenlog](04_templates/deviation_log_template.md) bij en pas de beslisregel toe: **Space bijwerken**, **register bijwerken** of **afwijking expliciet accepteren**.

## Validatie

De repo bevat een automatische manifestvalidatie die controleert of `00_register/instruction_manifest.yaml`, `00_register/master_register.csv` en de bronbestanden bij elkaar passen. De controles zijn beschreven in de [manifest-validatiespecificatie](00_register/manifest_validation_specification.md).

Lokaal uitvoeren:

```bash
pip install pyyaml   # alleen de eerste keer
python3 tools/validate_manifest.py
```

Het script geeft fouten (blokkerend) en waarschuwingen (informatief) in begrijpelijke taal. Bij fouten verschijnt per melding wat er aan de hand is en wat je moet doen.

In CI draait dezelfde controle automatisch via de workflow [`.github/workflows/validate.yml`](.github/workflows/validate.yml) op elke push en pull request naar `main`.

## Bijdragen en onderhoud

Lees [`CONTRIBUTING.md`](CONTRIBUTING.md) voordat je een nieuwe instructie toevoegt, een bestaande instructie aanpast of een lokale Space-wijziging terugkoppelt naar dit register. Het document bevat de volledige workflow (bronbestand → manifest → masterregister → changelog → validatie), de minimale metadata-eisen, de reviewcriteria voor nieuwe instructies, de changelogregels en een maintainer-checklist. Bij het openen van een pull request wordt automatisch het sjabloon uit [`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md) gebruikt.

