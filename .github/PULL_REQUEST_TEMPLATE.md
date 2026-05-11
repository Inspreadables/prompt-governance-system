# Pull request

## Doel van deze wijziging

<!-- Eén of twee zinnen. Verwijs naar het issuenummer, bijvoorbeeld: Closes #123. -->

## Type wijziging

- [ ] Nieuwe instructie (bron, adapter, template, workflow, rol)
- [ ] Bestaande instructie bijgewerkt (`PATCH` / `MINOR` / `MAJOR`)
- [ ] Statuswijziging (`draft` → `review` → `stable` → `deprecated`)
- [ ] Repo-proces of documentatie (geen instructie; geen registratie)
- [ ] Tooling, CI of validatie

## Geraakte instructies

<!-- Lijst `instruction_id@versie` van wat wijzigt of nieuw is. Bij MAJOR: noem ook geraakte Spaces uit `used_in`. -->

## Checklist (uit CONTRIBUTING.md)

- [ ] Bronbestand(en) bijgewerkt; geen platform-specifieke regels in generieke bronbestanden.
- [ ] Frontmatter compleet en consistent (`instruction_id`, `version`, `status`, `owner`, `last_reviewed`).
- [ ] `instruction_id` voldoet aan [`governance.instruction_id_convention`](../00_register/instruction_id_convention.md) en is uniek.
- [ ] Versie- en statusovergang volgen [`governance.versioning_release_policy`](../00_register/versioning_and_release_policy.md).
- [ ] `00_register/instruction_manifest.yaml` bijgewerkt.
- [ ] `00_register/master_register.csv` bijgewerkt (zelfde versie, status, datum als manifest).
- [ ] Afhankelijke adapters en Space-bootstraps bijgewerkt waar nodig.
- [ ] Changelog-regel toegevoegd in `99_changelog/changelog.md` met `instruction_id@versie` en motivering.
- [ ] Bij grotere releases: release notes ingevuld via `04_templates/release_notes_template.md`.
- [ ] `python3 tools/validate_manifest.py` rapporteert 0 fouten en 0 waarschuwingen.

## Opmerkingen voor reviewer

<!-- Optioneel: aandachtspunten, twijfelpunten, vragen. -->
