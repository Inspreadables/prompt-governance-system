# Bijdragen aan het Prompt Governance System

Dit document beschrijft hoe je instructies, adapters, templates en workflows in dit register toevoegt, wijzigt en onderhoudt. Het is bedoeld voor toekomstige bijdragers en onderhouders en gaat ervan uit dat je de [README](README.md) hebt gelezen.

De repo is een instructieregister, geen applicatie. Wijzigingen verlopen daarom via tekstbestanden, het manifest, het masterregister en de changelog — altijd in die volgorde.

## Leidende principes

- **Bron boven runtime.** Wijzig eerst het bronbestand in `01_global/`, `02_roles/`, `03_workflows/`, `04_templates/` of `05_agent_adapters/`. Werk daarna pas adapters, Space-bootstraps en runtime-projecties bij.
- **Eén ID, één plek.** Elke instructie heeft één `instruction_id` (zie [`governance.instruction_id_convention`](00_register/instruction_id_convention.md)) en bestaat één keer op één pad.
- **Manifest is leidend.** [`00_register/instruction_manifest.yaml`](00_register/instruction_manifest.yaml) is de canonieke bron; [`00_register/master_register.csv`](00_register/master_register.csv) is de menselijk leesbare spiegel. Ze mogen nooit uit de pas lopen.
- **Geen stille wijzigingen.** Elke inhoudelijke wijziging krijgt een regel in [`99_changelog/changelog.md`](99_changelog/changelog.md).
- **Anti-rot.** Lokale veranderingen in een Space, Custom GPT of Claude Project moeten terug naar dit register of expliciet als afwijking worden gemarkeerd (zie [`workflow.anti_rot_protocol`](03_workflows/anti_rot_protocol.md) en de [maandelijkse reviewroutine](03_workflows/anti_rot_review_routine.md)).

## Type wijzigingen

| Type wijziging                                            | Workflow                                                  |
| --------------------------------------------------------- | --------------------------------------------------------- |
| Nieuwe instructie (bron, adapter, template, workflow, rol) | [Nieuwe instructie toevoegen](#nieuwe-instructie-toevoegen) |
| Bestaande instructie aanpassen                            | [Bestaande instructie bijwerken](#bestaande-instructie-bijwerken) |
| Lokale Space-verandering terugkoppelen                    | [Space-wijziging terugbrengen naar de repo](#space-wijziging-terugbrengen-naar-de-repo) |
| Repo-procesdocument (zoals dit bestand)                   | Geen registratie nodig; geen frontmatter; alleen changelog-regel |

## Nieuwe instructie toevoegen

1. **Kies een `instruction_id`** volgens [`governance.instruction_id_convention`](00_register/instruction_id_convention.md). Prefix = categorie (`global.`, `role.`, `workflow.`, `template.`, `adapter.`, `governance.`). De prefix bepaalt de directory.
2. **Maak het bronbestand** op het pad dat hoort bij de ID (bijvoorbeeld `template.intake_form` → `04_templates/intake_form.md`).
3. **Voeg verplichte frontmatter toe** bovenaan het bestand (zie [Minimale metadata](#minimale-metadata-voor-instructies)).
4. **Vul de instructie-inhoud in.** Schrijf in heldere taal, verwijs via `instruction_id` naar andere instructies (geen lange tekstkopieën).
5. **Registreer in het manifest.** Voeg een entry toe aan [`00_register/instruction_manifest.yaml`](00_register/instruction_manifest.yaml) met `instruction_id`, `path`, `version`, `status` en `applies_to`.
6. **Registreer in het masterregister.** Voeg een rij toe aan [`00_register/master_register.csv`](00_register/master_register.csv) met `instruction_id`, `version`, `path`, `status`, `owner`, `last_reviewed`, `used_in`, `notes`.
7. **Voeg een changelog-regel toe** in [`99_changelog/changelog.md`](99_changelog/changelog.md) onder de huidige datum (zie [Changelogregels](#changelogregels)).
8. **Valideer lokaal:** `python3 tools/validate_manifest.py`. Streef naar 0 fouten en 0 waarschuwingen.
9. **Open een pull request** met een korte beschrijving en verwijzing naar het issuenummer.

## Bestaande instructie bijwerken

1. **Bepaal het type wijziging** volgens [`governance.versioning_release_policy`](00_register/versioning_and_release_policy.md):
   - `PATCH` — typefouten, redactionele verbeteringen, verduidelijkingen zonder gedragsverandering.
   - `MINOR` — additieve uitbreidingen die bestaande gebruikers niet breken.
   - `MAJOR` — niet backwards-compatible wijziging (verplichte nieuwe stappen, verdwijnende velden, scope-shift). Bij twijfel tussen `MINOR` en `MAJOR`: kies `MAJOR`.
2. **Wijzig het bronbestand** en pas de frontmatter aan (`version`, `status`, `last_reviewed`).
3. **Werk het manifest bij** (`version`, `status`).
4. **Werk het masterregister bij** (`version`, `status`, `last_reviewed`, eventueel `notes`).
5. **Werk afhankelijke adapters bij** volgens de regels in [`governance.versioning_release_policy`](00_register/versioning_and_release_policy.md) (sectie *Adapterversies versus bronversies*).
6. **Voeg een changelog-regel toe** met `instruction_id@versie`, statuswijziging (indien van toepassing) en korte motivering.
7. **Valideer lokaal:** `python3 tools/validate_manifest.py`. Streef naar 0 fouten en 0 waarschuwingen.
8. **Open een pull request.** Bij `MAJOR`-wijzigingen: noem in de PR welke Spaces en adapters geraakt worden (zie `used_in` in het masterregister) en gebruik het [release-notes-template](04_templates/release_notes_template.md).

### Statusovergangen

`draft` → `review` → `stable` → `deprecated`. Een instructie mag pas naar `stable` als haar versie `>= 1.0.0` is, een changelog-regel bestaat en manifest + masterregister consistent zijn. Een opvolger van een `deprecated` instructie krijgt een nieuwe `instruction_id`.

## Minimale metadata voor instructies

Elk instructiebestand (alles in `01_global/`, `02_roles/`, `03_workflows/`, `04_templates/`, `05_agent_adapters/` en de `governance.*`-bestanden in `00_register/`) heeft een YAML-frontmatterblok bovenaan:

```yaml
---
instruction_id: <prefix>.<naam>
version: <semver>
status: draft|review|stable|deprecated
owner: <naam of team>
last_reviewed: YYYY-MM-DD
---
```

Aanvullende eisen:

- `instruction_id` in de frontmatter is identiek aan die in het manifest en het masterregister.
- `version` in de frontmatter is identiek aan die in het manifest en het masterregister.
- `path` in het manifest komt exact overeen met het bestand op schijf.
- Voor elke `stable` instructie geldt `version >= 1.0.0`.

Repo-procesdocumenten zoals `CONTRIBUTING.md`, `README.md` en `.github/PULL_REQUEST_TEMPLATE.md` zijn **geen instructies** en krijgen géén frontmatter en géén registratie in manifest of masterregister. De manifestvalidatie negeert bestanden zonder frontmatter buiten de instructiemappen.

## Choose-an-ID: snelle beslisboom

1. Is dit een meta-document over het register zelf (conventies, beleid, schemaregels)? → prefix `governance.`, pad `00_register/`.
2. Beschrijft het een persona of functieprofiel? → prefix `role.`, pad `02_roles/`.
3. Beschrijft het een meerstappenproces of audit? → prefix `workflow.`, pad `03_workflows/`.
4. Is het een invulformat (checklist, brief, log)? → prefix `template.`, pad `04_templates/`.
5. Vertaalt het bronbestanden naar een specifieke runtime (Perplexity, Claude, GPT, Copilot, Cursor)? → prefix `adapter.`, pad `05_agent_adapters/`. Gebruik het [adapter-template](04_templates/adapter_template.md) als startpunt.
6. Geldt het voor alle agents en is het inhoudelijk generiek? → prefix `global.`, pad `01_global/`.

Volg vervolgens de naamgevingsregels in [`governance.instruction_id_convention`](00_register/instruction_id_convention.md): ASCII kleine letters, underscores binnen een segment, singular, taalneutraal (Engels), uniek, maximaal drie segmenten na de prefix.

## Versionering en releasebeleid toepassen

Het volledige beleid staat in [`governance.versioning_release_policy`](00_register/versioning_and_release_policy.md). Korte samenvatting:

- Tot productierijp: versie blijft `< 1.0.0`, status `draft`. Eerste productieversie is `1.0.0` met status `stable`.
- Adapterversies en bronversies lopen onafhankelijk; een `MAJOR`-bump op een bron triggert minimaal een `MINOR` op elke verwijzende adapter.
- Spaces volgen standaard de actuele `stable` versie via `instruction_id`. Pinning op `instruction_id@semver` is toegestaan maar moet expliciet worden vastgelegd in `used_in` of `notes` van het masterregister.
- Bij grotere releases (meerdere instructies of een `MAJOR`-bump): gebruik het [release-notes-template](04_templates/release_notes_template.md).

## Validatie

De repo bevat een automatische manifestvalidatie. Controles staan in [`governance.manifest_validation_specification`](00_register/manifest_validation_specification.md).

Lokaal uitvoeren:

```bash
pip install pyyaml   # alleen de eerste keer
python3 tools/validate_manifest.py
```

Streefdoel: **0 fouten en 0 waarschuwingen** voordat je een pull request opent. In CI draait dezelfde controle automatisch via [`.github/workflows/validate.yml`](.github/workflows/validate.yml) op elke push en pull request naar `main`. Een PR mag pas worden gemerged als CI groen is.

Veelvoorkomende fouten:

- `C1`/`C2` — verplicht veld ontbreekt in manifest of masterregister.
- `C3` — pad in manifest komt niet overeen met bestand op schijf.
- `C4` — instructie-ID voldoet niet aan de conventie.
- `C5` — frontmatter is inconsistent met manifest of masterregister.
- `C8.1` — een bronbestand met frontmatter staat niet in het manifest.

## Space-wijziging terugbrengen naar de repo

Lokale wijzigingen in een Space, Custom GPT of Claude Project zijn een drift-signaal. Volg dit pad zodra je iets in de runtime tegenkomt dat niet (meer) overeenkomt met het register:

1. **Signaleer** de afwijking via de [maandelijkse anti-rot reviewroutine](03_workflows/anti_rot_review_routine.md) of ad hoc.
2. **Classificeer** in het [afwijkingenlog](04_templates/deviation_log_template.md): is dit drift, een platform-specifieke aanpassing, of een legitieme inhoudelijke verbetering?
3. **Pas de beslisregel toe** uit `workflow.anti_rot_review_routine`:
   - **Space bijwerken** — de Space loopt achter; breng de Space terug in lijn met het register.
   - **Register bijwerken** — de Space-verbetering is generiek; voer hem terug naar het bronbestand (volg [Bestaande instructie bijwerken](#bestaande-instructie-bijwerken)) of voeg een nieuwe instructie toe (volg [Nieuwe instructie toevoegen](#nieuwe-instructie-toevoegen)).
   - **Afwijking expliciet accepteren** — de wijziging is platform-specifiek of tijdelijk; leg vast in het afwijkingenlog met eigenaar, einddatum en motivering. Platform-specifieke regels horen in de adapterlaag, niet in `01_global/`, `02_roles/`, `03_workflows/` of `04_templates/`.
4. **Werk manifest, masterregister en changelog bij** zodra de aanpassing in de repo landt.

## Reviewcriteria voor nieuwe en gewijzigde instructies

Een reviewer (of registereigenaar) controleert minimaal:

1. **Doel en scope** — is duidelijk wat de instructie wel en niet regelt? Geen overlap met bestaande instructies zonder expliciete verwijzing.
2. **ID-conventie** — `instruction_id` voldoet aan [`governance.instruction_id_convention`](00_register/instruction_id_convention.md): prefix correct, snake_case, Engels, singular, uniek, maximaal drie segmenten na de prefix.
3. **Pad** — bestandspad komt overeen met de prefix-tot-directory-mapping en met het manifest.
4. **Frontmatter** — `instruction_id`, `version`, `status`, `owner`, `last_reviewed` zijn aanwezig en consistent met manifest en masterregister.
5. **Versie en status** — kloppen met [`governance.versioning_release_policy`](00_register/versioning_and_release_policy.md). `stable` impliceert `version >= 1.0.0`.
6. **Verwijzingen** — naar andere instructies via `instruction_id`, niet via gedupliceerde tekst. Geen verwijzingen naar `deprecated` instructies zonder migratieplan.
7. **Agent-onafhankelijkheid** — bronbestanden bevatten geen platform-specifieke regels; die horen in `05_agent_adapters/`.
8. **Taal en stijl** — heldere taal, consistent met [`global.communication_style`](01_global/communication_style.md) en [`global.quality_standards`](01_global/quality_standards.md).
9. **Manifest + masterregister** — beide bijgewerkt en consistent.
10. **Changelog** — regel toegevoegd met `instruction_id@versie`, statuswijziging en korte motivering.
11. **Validatie** — `python3 tools/validate_manifest.py` rapporteert 0 fouten en 0 waarschuwingen.

## Changelogregels

[`99_changelog/changelog.md`](99_changelog/changelog.md) is omgekeerd-chronologisch (nieuwste bovenaan) en gegroepeerd per datum. Elke regel beschrijft één logische wijziging.

Een goede changelog-regel bevat:

- **`instruction_id@versie`** (of meerdere) — wat is er gewijzigd.
- **Statusovergang** (indien van toepassing) — bijvoorbeeld `draft` → `stable`.
- **Pad** van het bronbestand.
- **Korte motivering** — waarom de wijziging nodig was.
- **Verwijzing naar gerelateerde instructies** waar relevant (via `instruction_id`).
- **PR- of issuenummer** tussen haakjes aan het einde, bijvoorbeeld `(#8)`.

Voorbeeld:

> `template.intake_form@1.0.0` (status `draft` → `stable`) in `04_templates/intake_form.md`: productieversie met verplichte velden voor doel, doelgroep en succescriteria; verwijzingen naar `workflow.prompt_audit_protocol` en `global.quality_standards`. Manifest en masterregister bijgewerkt (#12).

Voor grotere releases (meerdere instructies, `MAJOR`-bumps, of meerdere statuswijzigingen naar `stable`/`deprecated`): vul daarnaast het [release-notes-template](04_templates/release_notes_template.md) in en koppel dit in de PR-beschrijving.

## Maintainer-checklist

Doorloop deze checklist voordat je een pull request mergt:

- [ ] Doel en scope van de wijziging zijn duidelijk in de PR-beschrijving.
- [ ] Bronbestand(en) bijgewerkt; geen platform-specifieke regels in generieke bronbestanden.
- [ ] Frontmatter compleet en consistent (`instruction_id`, `version`, `status`, `owner`, `last_reviewed`).
- [ ] `instruction_id` voldoet aan de conventie en is uniek.
- [ ] Versie- en statusovergang volgen het releasebeleid.
- [ ] `00_register/instruction_manifest.yaml` bijgewerkt.
- [ ] `00_register/master_register.csv` bijgewerkt (zelfde versie, status, datum als manifest).
- [ ] Afhankelijke adapters en bootstraps bijgewerkt waar nodig.
- [ ] Changelog-regel toegevoegd in `99_changelog/changelog.md`.
- [ ] Bij grotere releases: release notes ingevuld via `04_templates/release_notes_template.md`.
- [ ] `python3 tools/validate_manifest.py` rapporteert 0 fouten en 0 waarschuwingen.
- [ ] CI-workflow `validate.yml` is groen.
- [ ] PR verwijst naar het issuenummer en, bij `MAJOR`-wijzigingen, naar geraakte Spaces (`used_in`).

## Vragen of voorstellen

Open een GitHub-issue voor inhoudelijke voorstellen, twijfelgevallen rond ID-keuze of releasebeleid, of voorstellen voor nieuwe categorieën (prefixes). Wijzig pas bestanden nadat het issue is besproken om dubbel werk te voorkomen.
