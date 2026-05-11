# Instructie-ID conventie

**Instruction ID:** `governance.instruction_id_convention`
**Versie:** 1.0.0
**Status:** stable
**Eigenaar:** A. Verboon
**Laatst herzien:** 2026-05-11

## Doel

Eén consistente, voorspelbare naamgeving voor elke instructie in dit register. Een goede ID maakt direct duidelijk waar een instructie thuishoort, hoe zij gebruikt wordt en waar het bronbestand staat. Nieuwe bijdragers moeten zonder verdere uitleg een correcte ID kunnen kiezen.

## Algemene vorm

```
<prefix>.<naam>[.<subnaam>]
```

Optioneel kan in adapters, manifesten en bootstraps een versie worden toegevoegd:

```
<prefix>.<naam>@<semver>
```

Bijvoorbeeld: `adapter.perplexity_space@1.0.0`.

## Naamgevingsregels

1. **Alleen ASCII kleine letters, cijfers, punten en underscores.** Geen spaties, hoofdletters, streepjes of accenten.
2. **Prefix is verplicht** en bepaalt de categorie (zie tabel hieronder).
3. **Eén punt scheidt prefix van naam.** Extra subniveaus worden ook met een punt gescheiden.
4. **Underscores binnen een segment** voor leesbaarheid (`prompt_audit_protocol`), nooit op de grens tussen segmenten.
5. **Singular, niet plural.** Gebruik `role.prompt_analyst`, niet `roles.prompt_analysts`.
6. **Beschrijvend en compact.** Maximaal drie segmenten na de prefix; geef de voorkeur aan twee.
7. **Stabiel.** Een ID verandert niet als de inhoud evolueert; alleen de versie loopt op. Bij een fundamentele scope-wijziging maak je een nieuwe ID en zet je de oude op `deprecated`.
8. **Uniek over het hele register.** Twee bestanden mogen nooit dezelfde ID dragen.
9. **Taalneutraal.** Schrijf de ID in het Engels, ook als het bronbestand in het Nederlands is. Dit maakt cross-tool gebruik eenvoudiger.

## Prefixes

| Prefix        | Categorie                            | Map               | Wanneer gebruiken                                                                          |
|---------------|--------------------------------------|-------------------|--------------------------------------------------------------------------------------------|
| `global.`     | Generieke werkprincipes & standaarden | `01_global/`      | Instructie geldt voor alle agents, rollen en workflows.                                    |
| `role.`       | Herbruikbare agentrollen              | `02_roles/`       | Beschrijft een persona of functieprofiel dat in meerdere omgevingen kan worden gebruikt.   |
| `workflow.`   | Standaardprocessen en protocollen     | `03_workflows/`   | Beschrijft een meerstappenproces, audit of protocol.                                        |
| `template.`   | Invulformats                          | `04_templates/`   | Vormgegeven format dat de gebruiker invult (brief, checklist, intakeformulier).            |
| `adapter.`    | Vertalingen naar agentomgevingen      | `05_agent_adapters/` | Maakt brondocumenten geschikt voor een specifieke runtime (Perplexity Space, GPT, Claude). |
| `governance.` | Meta-instructies over het register zelf | `00_register/`  | Conventies, manifest-regels en andere meta-documentatie. Beperkt gebruik.                  |

Andere prefixes worden alleen toegevoegd als ze een duidelijk nieuwe categorie vertegenwoordigen die niet binnen de bestaande past. Voeg in dat geval ook een rij toe aan deze tabel.

## Relatie tot bestandspaden

De prefix komt overeen met de directory. Het tweede segment komt overeen met de bestandsnaam zonder extensie.

| Instruction ID                                | Pad                                                       |
|-----------------------------------------------|-----------------------------------------------------------|
| `global.operating_principles`                 | `01_global/operating_principles.md`                       |
| `role.prompt_analyst_manager_orchestrator`    | `02_roles/prompt_analyst_manager_orchestrator.md`         |
| `workflow.prompt_audit_protocol`              | `03_workflows/prompt_audit_protocol.md`                   |
| `template.space_audit_checklist`              | `04_templates/space_audit_checklist.md`                   |
| `adapter.perplexity_space`                    | `05_agent_adapters/perplexity_space_adapter.md`           |
| `governance.instruction_id_convention`        | `00_register/instruction_id_convention.md`                |

Als een instructie meerdere bestanden omvat, gebruik dan een submap met dezelfde naam en verwijs in de manifest naar het hoofd-Markdownbestand.

## Relatie tot versies

- Versies volgen [Semantic Versioning](https://semver.org/lang/nl/): `MAJOR.MINOR.PATCH`.
- Tot een instructie productierijp is, blijft de versie `< 1.0.0` en status `draft`.
- Pas `MAJOR` aan bij niet-backwards-compatible scope-wijziging.
- Pas `MINOR` aan bij toegevoegde inhoud die bestaande gebruikers niet breekt.
- Pas `PATCH` aan bij correcties, redactionele wijzigingen of verduidelijkingen.
- De combinatie `<id>@<version>` is de canonieke verwijzing in adapters, bootstraps en logs.

## Relatie tot het manifest

Elke instructie heeft één regel in `00_register/instruction_manifest.yaml`:

```yaml
- instruction_id: governance.instruction_id_convention
  path: 00_register/instruction_id_convention.md
  version: 1.0.0
  status: stable
  applies_to:
    - all_agents
```

Verplichte velden: `instruction_id`, `path`, `version`, `status`, `applies_to`. De `path` moet exact overeenkomen met het bestand op schijf.

## Relatie tot het masterregister

Elke instructie heeft één rij in `00_register/master_register.csv`. De ID is daar de primaire sleutel; `version`, `path`, `status`, `owner`, `last_reviewed`, `used_in` en `notes` zijn ondersteunende velden. Het masterregister en het manifest mogen nooit uit de pas lopen.

## Statuswaarden

| Status        | Betekenis                                                                 |
|---------------|---------------------------------------------------------------------------|
| `draft`       | In ontwikkeling, nog niet betrouwbaar voor productiegebruik.              |
| `review`      | Inhoud is compleet en wordt beoordeeld voordat het stabiel wordt.         |
| `stable`      | Productiewaardig; mag onbeperkt door agents en Spaces worden gebruikt.    |
| `deprecated`  | Niet meer gebruiken; verwijzing naar opvolger in `notes`.                 |

## Voorbeelden (do)

- `global.operating_principles`
- `global.quality_standards`
- `role.prompt_analyst_manager_orchestrator`
- `workflow.anti_rot_protocol`
- `template.agent_brief`
- `template.space_audit_checklist`
- `adapter.claude_project`
- `adapter.custom_gpt`
- `adapter.perplexity_space@1.0.0`
- `governance.instruction_id_convention`

## Anti-voorbeelden (don't)

| ID                                    | Probleem                                                         |
|---------------------------------------|------------------------------------------------------------------|
| `PromptAuditProtocol`                 | Hoofdletters; geen prefix.                                       |
| `workflows.prompt-audit-protocol`     | Plural prefix; streepjes in plaats van underscores.              |
| `workflow.prompt audit protocol`      | Spaties.                                                         |
| `workflow/prompt_audit_protocol`      | Verkeerd scheidingsteken.                                        |
| `audit`                               | Geen prefix; te generiek.                                        |
| `role.prompt_analyst.v2`              | Versie hoort niet in de ID; gebruik `@2.0.0`.                    |
| `adapter.perplexity_spaces`           | Plural in de naam.                                               |
| `template.brief_voor_klant`           | Mengtaal; houd de ID Engels.                                     |

## Workflow voor nieuwe IDs

1. Kies een prefix uit de tabel.
2. Kies een korte, beschrijvende naam in `snake_case`, Engels, singular.
3. Controleer dat de ID nog niet bestaat in `master_register.csv` en `instruction_manifest.yaml`.
4. Maak het bronbestand op het pad dat overeenkomt met de ID.
5. Registreer de ID in `instruction_manifest.yaml` en `master_register.csv` met de juiste versie en status.
6. Voeg een regel toe aan `99_changelog/changelog.md`.

## Bestaande situatie

Alle huidige instructies in dit register volgen deze conventie. Er zijn geen openstaande uitzonderingen. Wanneer in de toekomst een ID nodig is die niet past binnen de bestaande prefixes, breid deze tabel uit voordat de ID in gebruik wordt genomen.
