---
instruction_id: governance.versioning_release_policy
version: 1.0.0
status: stable
owner: A. Verboon
last_reviewed: 2026-05-11
---

# Versie- en releasebeleid

**Instruction ID:** `governance.versioning_release_policy`
**Versie:** 1.0.0
**Status:** stable
**Eigenaar:** A. Verboon
**Laatst herzien:** 2026-05-11

## Doel

Eén consistente, voorspelbare manier om wijzigingen aan instructies, rollen, workflows, templates en adapters te versioneren en uit te brengen. Dit beleid maakt expliciet wanneer een wijziging `MAJOR`, `MINOR` of `PATCH` is, hoe statussen (`draft`, `review`, `stable`, `deprecated`) overgaan, hoe adapterversies zich verhouden tot bronversies, hoe Spaces weten welke versie actief is en hoe releases worden gedocumenteerd.

Dit document bouwt voort op [`governance.instruction_id_convention`](instruction_id_convention.md) en is op zichzelf onderdeel van de meta-laag (`governance.*`).

## Reikwijdte

Het beleid geldt voor alle instructiesets in dit register, te weten elke rij in `00_register/master_register.csv` en elk item in `00_register/instruction_manifest.yaml`. Het regelt zowel de versie van afzonderlijke instructies als het schemaversie van het register zelf.

## Semver voor instructiesets

Versies volgen [Semantic Versioning](https://semver.org/lang/nl/): `MAJOR.MINOR.PATCH`.

| Component | Verhoog wanneer                                                                                                                                                | Voorbeeld                                                                                          |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `MAJOR`   | De wijziging is **niet backwards-compatible** voor consumenten (Spaces, agents, adapters). Bestaande verwijzingen, gedrag, structuur of contractuele afspraken breken. | Een rol verandert van scope; een workflow krijgt verplichte nieuwe stappen; een template-veld verdwijnt. |
| `MINOR`   | Inhoud wordt **uitgebreid op een additieve manier**. Bestaande consumenten blijven correct werken zonder aanpassingen.                                          | Een sectie wordt toegevoegd; een optioneel veld komt erbij; een nieuwe variant naast bestaande.    |
| `PATCH`   | **Correcties, verduidelijkingen of redactionele wijzigingen** zonder gedragsverandering.                                                                        | Typefouten, formatteringsverbeteringen, verfijnen van een voorbeeld, het verduidelijken van zinnen. |

### Tot 1.0.0

- Voor productierijp is, blijft de versie `< 1.0.0` en de status `draft`.
- In het bereik `0.y.z` mogen breaking changes ook met een minor-bump worden gedaan, maar leg dit altijd vast in de changelog.
- De eerste productiewaardige versie is `1.0.0` met status `stable`.

### Twijfelregel

Bij twijfel tussen `MINOR` en `MAJOR`: kies `MAJOR` als een bestaande Space, adapter of bootstrap zijn tekst, configuratie of gedrag zou moeten aanpassen om met de nieuwe versie correct te blijven werken.

## Status-levenscyclus

Statussen staan in `00_register/instruction_id_convention.md` en hebben de volgende toegestane overgangen:

```
draft → review → stable → deprecated
```

| Status        | Betekenis                                                                                       | Toegestaan gebruik in productie? |
| ------------- | ----------------------------------------------------------------------------------------------- | -------------------------------- |
| `draft`       | In ontwikkeling, niet stabiel, mag breken. Versie `< 1.0.0`.                                    | Nee, alleen experimenteel.       |
| `review`      | Inhoud is compleet en wordt beoordeeld. Versie mag `< 1.0.0` of een release candidate zijn.     | Nee, alleen voor reviewers.      |
| `stable`      | Productiewaardig. Versie `>= 1.0.0`. Wijzigingen volgen het semver-beleid hierboven.            | Ja.                              |
| `deprecated`  | Niet meer gebruiken. `notes` in het masterregister verwijst naar de opvolger of de reden.       | Nee, alleen voor migratiepaden.  |

Regels:

- Een instructie mag pas naar `stable` als haar versie `>= 1.0.0` is, een changelog-regel bestaat en het manifest plus masterregister consistent zijn.
- Een `stable` instructie blijft `stable` zolang er geen `deprecated`-besluit valt. Versies blijven binnen `stable` doorlopen via patch/minor/major.
- `deprecated` betekent: niet langer onderhouden. Een opvolger heeft een nieuwe `instruction_id` (zie conventie, regel 7).

## Adapterversies versus bronversies

Adapters (`adapter.*`) leven boven op één of meer bronnen (`global.*`, `role.*`, `workflow.*`, `template.*`). Versies van adapters en bronnen lopen onafhankelijk, met de volgende koppelingsregels.

1. Een adapter declareert in zijn frontmatter zijn eigen `version` en `status`.
2. Een adapter verwijst in zijn tekst altijd via `instruction_id` naar bronnen. Een expliciete versie (`@semver`) is optioneel; gebruik die alleen wanneer een specifieke bronversie nodig is.
3. Een bron-bump:
   - `PATCH` op een bron triggert geen verplichte adapter-bump.
   - `MINOR` op een bron triggert geen verplichte adapter-bump, tenzij de adapter de nieuwe inhoud expliciet wil aanbieden (`MINOR` op adapter).
   - `MAJOR` op een bron triggert minimaal `MINOR` op elke adapter die naar die bron verwijst (om de migratie zichtbaar te maken), en `MAJOR` op de adapter als de adapter-tekst zelf moet veranderen om correct te blijven werken.
4. Een adapter mag nooit naar een `deprecated` bron blijven verwijzen zonder migratieplan in zijn `notes`.

## Hoe Spaces weten welke versie actief is

Een Space is altijd een **runtime-projectie** van het register. De canonieke bron is `00_register/instruction_manifest.yaml`; `00_register/master_register.csv` is de menselijk leesbare spiegel.

Regels voor Spaces:

1. Een Space-bootstrap verwijst per instructie via `instruction_id` (en optioneel `@semver`). Lange tekstkopieën in de runtime-laag zijn niet toegestaan; zie [`adapter.perplexity_space`](../05_agent_adapters/perplexity_space_adapter.md), sectie *Lagenmodel*.
2. Standaard volgt een Space de **actuele `stable` versie** van elk verwezen `instruction_id`. Het manifest is leidend.
3. Wil een Space bewust pinnen op een specifieke versie (bijvoorbeeld om reproducerebaarheid te garanderen tijdens een audit), dan vermeldt de bootstrap expliciet `instruction_id@semver` per gepinde verwijzing. Pinning moet ook in `master_register.csv` (kolom `notes` of `used_in`) worden gemeld bij de betreffende Space, zodat de afhankelijkheid traceerbaar is.
4. Een Space die op een `deprecated` versie staat, is per definitie afwijkend. De auditor markeert dit volgens `workflow.anti_rot_protocol` en stelt migratie voor.
5. Bij een `MAJOR`-bump van een bron of adapter informeert de registereigenaar bekende Spaces (via `used_in` in het masterregister) en plant de migratie. Zie sectie *Releaseproces*.

## Releaseproces

Een release in dit register is een wijziging die ten minste één van de volgende doet: een nieuwe instructie toevoegen, een bestaande instructie van versie of status laten wijzigen, of een instructie deprecaten. Elke release doorloopt deze stappen:

1. **Bewerk bronbestand(en).** Wijzig de inhoud en pas de frontmatter aan (`version`, `status`, `last_reviewed`).
2. **Update manifest.** Pas `00_register/instruction_manifest.yaml` aan (regel van de betrokken instructie).
3. **Update masterregister.** Pas `00_register/master_register.csv` aan (zelfde instructie, plus `last_reviewed` en eventueel `notes`).
4. **Update adapters indien nodig.** Volg de regels in *Adapterversies versus bronversies*.
5. **Schrijf changelog-regel.** Voeg een regel toe aan `99_changelog/changelog.md` onder de huidige datum, met `instruction_id@versie`, statuswijziging (indien van toepassing) en een korte motivering. Gebruik bij grotere releases het [release-notes-template](../04_templates/release_notes_template.md).
6. **Commit en push.** Eén logische release per commit of pull request. PR-titel verwijst naar het issuenummer.
7. **Communiceer downstream.** Bij `MAJOR`-wijzigingen: meld de migratie aan bekende Spaces (zie `used_in`).

### Consistentie-eisen

- `instruction_manifest.yaml` en `master_register.csv` mogen nooit uit de pas lopen.
- Het pad in `path` moet exact overeenkomen met het bestand op schijf.
- Voor elke `stable` instructie geldt `version >= 1.0.0`.

### Schemaversie van het register zelf

Het veld `versioning.schema_version` in `instruction_manifest.yaml` versionneert de **structuur** van het manifest en het masterregister. Verhoog dit veld alleen wanneer veldnamen, verplichte velden of statuswaarden in het register zelf wijzigen, niet wanneer alleen individuele instructies bewegen.

## Documentatie van releases

Voor kleine wijzigingen (één instructie, `PATCH` of additieve `MINOR`) volstaat een changelog-regel. Voor grotere releases (meerdere instructies, één of meer `MAJOR`-bumps, of een statuswijziging naar `stable` of `deprecated`) gebruik je het release-notes-template in `04_templates/release_notes_template.md`. De gevulde release notes kunnen worden meegegeven in de PR-beschrijving of in een sectie onder `99_changelog/`.

## Relatie tot bestaande conventies

- **`governance.instruction_id_convention`** definieert hoe een ID heet en wat de toegestane statussen zijn. Dit beleid definieert hoe je tussen versies en statussen beweegt.
- **`workflow.anti_rot_protocol`** beschrijft hoe afwijkingen in een Space worden teruggekoppeld. Dit beleid bepaalt of zo'n afwijking een nieuwe versie of een nieuwe instructie wordt.
- **`adapter.perplexity_space`** geeft het lagenmodel (bron, adapter, runtime, audit). Dit beleid bepaalt welke versie in de adapter- en runtime-laag actief is.

## Voorbeelden

| Wijziging                                                                                          | Type    |
| --------------------------------------------------------------------------------------------------- | ------- |
| Typefout in `global.quality_standards`.                                                             | `PATCH` |
| Extra optioneel scoreveld toegevoegd aan `template.space_audit_checklist`.                          | `MINOR` |
| Rol `role.prompt_analyst_manager_orchestrator` splitst in twee rollen; oude ID wordt `deprecated`. | `MAJOR` op de nieuwe IDs, plus deprecatie van de oude. |
| Adapter `adapter.perplexity_space` herschrijft de bootstrap-tekst om een nieuwe bron mee te nemen.  | `MINOR` op de adapter. |
| Een veld in `instruction_manifest.yaml` wordt verplicht in plaats van optioneel.                    | `schema_version` bump (eigenstandig). |

## Open punten

Geen openstaande uitzonderingen op het moment van schrijven. Eventuele toekomstige uitbreidingen (bijvoorbeeld release candidates `1.0.0-rc.1`, of geautomatiseerde validatie van manifest tegen masterregister) worden via een nieuwe `MINOR` of `MAJOR` van dit document toegevoegd.
