---
instruction_id: governance.manifest_validation_specification
version: 1.0.0
status: stable
owner: A. Verboon
last_reviewed: 2026-05-11
---

# Manifest Validation Specification

**Instruction ID:** `governance.manifest_validation_specification`
**Versie:** 1.0.0
**Status:** stable
**Eigenaar:** A. Verboon
**Laatst herzien:** 2026-05-11

## Doel

Deze specificatie beschrijft welke geautomatiseerde controles dit register uitvoert om te voorkomen dat `00_register/instruction_manifest.yaml`, `00_register/master_register.csv` en de bronbestanden uit elkaar gaan lopen. De specificatie is de bron van waarheid voor het validatiescript (`tools/validate_manifest.py`) en de bijbehorende GitHub Action (`.github/workflows/validate.yml`).

De foutmeldingen zijn opzettelijk geschreven voor niet-programmeurs. Elke melding noemt het bestand, het veld of de ID waar het misgaat en wat de gebruiker moet doen om het op te lossen.

## Scope

De validatie controleert uitsluitend:

- `00_register/instruction_manifest.yaml`
- `00_register/master_register.csv`
- de bestanden waarnaar het manifest verwijst
- de YAML-frontmatter in die bestanden, voor zover aanwezig

De validatie controleert niet de inhoudelijke kwaliteit van een instructie. Daarvoor blijft `workflow.prompt_audit_protocol` van kracht.

## Controles

De validatie kent twee soorten meldingen:

- **fout (error)**: blokkeert een release of merge. De repo is in deze staat niet consistent.
- **waarschuwing (warning)**: wijst op een afwijking die opgelost moet worden, maar die niet direct een release blokkeert. Geschikt voor migratiesituaties.

### C1. Manifest-bestand is leesbaar en correct gestructureerd

- **C1.1 fout** — `00_register/instruction_manifest.yaml` bestaat en is geldige YAML.
- **C1.2 fout** — De sleutel `instruction_sets` is aanwezig en bevat een lijst.
- **C1.3 fout** — Elke entry in `instruction_sets` is een mapping met ten minste de velden `instruction_id`, `path`, `version`, `status`, `applies_to`.

### C2. Manifest-entries verwijzen naar bestaande bestanden

- **C2.1 fout** — Voor elke entry in `instruction_sets` bestaat het bestand op `path` (relatief aan de repo-root).
- **C2.2 fout** — Het `path` ligt binnen de repo (geen `..`, geen absoluut pad).

### C3. Instruction IDs zijn uniek en volgen de conventie

De conventie is vastgelegd in `governance.instruction_id_convention` (`00_register/instruction_id_convention.md`).

- **C3.1 fout** — Elke `instruction_id` komt maximaal één keer voor in `instruction_sets`.
- **C3.2 fout** — Elke `instruction_id` voldoet aan de reguliere expressie `^[a-z0-9_]+(\.[a-z0-9_]+){1,3}$`.
  - Dit dwingt af: alleen ASCII kleine letters, cijfers en underscores, één tot drie puntsegmenten na de prefix, geen spaties, geen streepjes, geen hoofdletters.
- **C3.3 fout** — De prefix (alles vóór de eerste punt) staat in de toegestane lijst: `global`, `role`, `workflow`, `template`, `adapter`, `governance`.
- **C3.4 waarschuwing** — De prefix van de ID komt overeen met de map waarin het bestand staat:
  - `global.*` → `01_global/`
  - `role.*` → `02_roles/`
  - `workflow.*` → `03_workflows/`
  - `template.*` → `04_templates/`
  - `adapter.*` → `05_agent_adapters/`
  - `governance.*` → `00_register/`

### C4. Manifest en masterregister zijn consistent

- **C4.1 fout** — Elke `instruction_id` uit het manifest bestaat ook als rij in `master_register.csv`.
- **C4.2 fout** — Elke `instruction_id` uit `master_register.csv` bestaat ook in het manifest.
- **C4.3 fout** — Voor elke gemeenschappelijke `instruction_id` zijn `version`, `path` en `status` identiek in manifest en masterregister.

### C5. Statuswaarden zijn geldig

- **C5.1 fout** — Het veld `status` in manifest en masterregister is één van: `draft`, `review`, `stable`, `deprecated`.

### C6. Versies zijn geldige semver

- **C6.1 fout** — Het veld `version` in manifest en masterregister voldoet aan `MAJOR.MINOR.PATCH` (uitsluitend cijfers, drie segmenten).

### C7. Frontmatter in bronbestanden is consistent (waar aanwezig)

Niet elk bronbestand heeft YAML-frontmatter; templates zonder semantische status mogen die weglaten. Wanneer een bestand wél frontmatter heeft, gelden de volgende controles:

- **C7.1 fout** — Als een bestand frontmatter heeft, bevat die de sleutels `instruction_id`, `version`, `status`, `owner`, `last_reviewed`.
- **C7.2 fout** — `instruction_id`, `version` en `status` in de frontmatter komen exact overeen met de waarden voor dezelfde `instruction_id` in het manifest.
- **C7.3 waarschuwing** — `owner` en `last_reviewed` in de frontmatter komen overeen met het masterregister.
- **C7.4 waarschuwing** — `last_reviewed` is een datum in ISO-formaat (`YYYY-MM-DD`).

### C8. Niet-gemanifesteerde bestanden

- **C8.1 waarschuwing** — Een bestand in `01_global/`, `02_roles/`, `03_workflows/`, `04_templates/`, `05_agent_adapters/` of `00_register/` met geldige frontmatter dat niet in het manifest is opgenomen wordt gemeld. Dit is een waarschuwing omdat er bestanden kunnen zijn die nog niet productierijp zijn.
- **C8.2 informatie** — Bestanden zonder frontmatter (zoals oudere templates) worden genegeerd. Zij vallen buiten de scope van automatische validatie tot zij frontmatter krijgen.

## Foutmeldingen

Elke melding heeft dezelfde opbouw zodat ze begrijpelijk blijft voor niet-programmeurs:

```
[NIVEAU] [CODE] korte beschrijving in het Nederlands
Bestand: <pad>
Wat is er aan de hand: <uitleg in normale taal>
Wat moet je doen: <concrete actie>
```

Voorbeeld:

```
[FOUT] [C2.1] Het manifest verwijst naar een bestand dat niet bestaat.
Bestand: 04_templates/release_notes_template.md
Wat is er aan de hand: in 00_register/instruction_manifest.yaml staat een verwijzing naar dit bestand, maar het is niet aanwezig in de repo.
Wat moet je doen: maak het bestand aan op dit pad, of pas het manifest aan zodat het naar het juiste pad verwijst.
```

## Uitvoer

Het validatiescript schrijft een leesbaar verslag naar standaarduitvoer met:

1. Een kop met het tijdstip en de gecontroleerde bestanden.
2. Een lijst meldingen, gegroepeerd op niveau (`FOUT` eerst, daarna `WAARSCHUWING`).
3. Een samenvatting met het aantal fouten en waarschuwingen.

De return-code is:

- `0` — geen fouten (waarschuwingen worden wel getoond).
- `1` — één of meer fouten.

De GitHub Action gebruikt deze return-code om merges te blokkeren wanneer er fouten zijn.

## Uitvoeren

Lokaal:

```bash
python3 tools/validate_manifest.py
```

Het script gebruikt alleen de standaardbibliotheek en `PyYAML`. `PyYAML` zit op de meeste Python-installaties al; anders: `pip install pyyaml`.

In CI: de workflow `.github/workflows/validate.yml` draait automatisch op elke push en pull request naar `main`.

## Onderhoud

Wanneer een nieuwe controle wordt toegevoegd:

1. Beschrijf de controle hier met een unieke code (`C9.1`, enzovoort).
2. Implementeer de controle in `tools/validate_manifest.py`.
3. Documenteer de nieuwe controle in `99_changelog/changelog.md`.
4. Verhoog `MINOR` van deze specificatie als de nieuwe controle nieuwe meldingen toevoegt zonder bestaande meldingen te wijzigen; verhoog `MAJOR` als bestaand gedrag breekt.
