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

## Conventies

- [Instructie-ID conventie](00_register/instruction_id_convention.md) — prefixes, naamgevingsregels, voorbeelden en relatie tot bestandspaden, versies, manifest en masterregister. Lees dit voordat je een nieuwe instructie toevoegt.
- [Versie- en releasebeleid](00_register/versioning_and_release_policy.md) — semver-regels (`MAJOR`/`MINOR`/`PATCH`), statusovergangen (`draft` → `review` → `stable` → `deprecated`), de verhouding tussen adapterversies en bronversies, hoe Spaces weten welke versie actief is en hoe releases worden gedocumenteerd. Gebruik bij grotere releases het [release-notes-template](04_templates/release_notes_template.md).

