---
instruction_id: template.release_notes
version: 1.0.0
status: stable
owner: A. Verboon
last_reviewed: 2026-05-11
---

# Release notes-template

Gebruik dit template bij elke release die meer is dan een enkele `PATCH` of additieve `MINOR` op één instructie. Vul het sjabloon in een PR-beschrijving of als bijlage onder `99_changelog/`. Voor kleine wijzigingen volstaat een regel in `99_changelog/changelog.md`.

Conventies en regels staan in [`governance.versioning_release_policy`](../00_register/versioning_and_release_policy.md) en [`governance.instruction_id_convention`](../00_register/instruction_id_convention.md).

---

## Release: `<korte titel>`

- **Datum:** `YYYY-MM-DD`
- **Releasetype:** `patch` | `minor` | `major` | `mixed`
- **Issue / PR:** `#<nummer>` (en eventuele gerelateerde issues)
- **Auteur:** `<naam>`

## Samenvatting

Een korte beschrijving (twee tot vier zinnen) van wat er verandert en waarom. Schrijf in actieve vorm. Vermijd jargon dat buiten de context van deze repository niet bestaat.

## Gewijzigde instructies

Lijst per gewijzigde of nieuwe instructie. Eén tabelrij per `instruction_id`.

| instruction_id                            | van → naar versie | statuswijziging        | type    | toelichting                                       |
| ----------------------------------------- | ----------------- | ---------------------- | ------- | -------------------------------------------------- |
| `governance.example_instruction`          | `1.2.0 → 1.3.0`   | `stable` (ongewijzigd) | `minor` | Voeg sectie X toe voor use case Y.                 |
| `workflow.example_protocol`               | `0.4.0 → 1.0.0`   | `review → stable`      | `major` | Eerste productieversie; scope vastgezet.           |

## Breaking changes

Beschrijf elke `MAJOR`-wijziging in detail. Vermeld:

- Wat brak.
- Welke consumenten (adapters, Spaces, templates) hierdoor moeten worden aangepast.
- Welk migratiepad geldt en op welke termijn.

Als er geen breaking changes zijn: schrijf `Geen.`.

## Migratiepad

Stappenplan voor bestaande Spaces, adapters en bootstraps. Verwijs naar betrokken bestanden en eventuele scripts of checklists.

1. ...
2. ...
3. ...

## Impact op adapters

Per adapter (`adapter.*`) die wordt geraakt:

- `adapter.<naam>` blijft op `<versie>`: geen actie nodig.
- `adapter.<naam>` gaat naar `<nieuwe versie>`: tekst aangepast, zie commit `<hash>`.

Volg de regels in `governance.versioning_release_policy`, sectie *Adapterversies versus bronversies*.

## Impact op Spaces en runtime

- Welke Spaces in `master_register.csv` kolom `used_in` verwijzen naar de gewijzigde instructies?
- Welke Spaces pinnen expliciet op een oude versie en moeten worden gemigreerd?
- Welke actie wordt verwacht en door wie?

## Manifest en masterregister

Bevestig met een vinkje dat de volgende artefacten consistent zijn bijgewerkt:

- [ ] `00_register/instruction_manifest.yaml` weerspiegelt de nieuwe versies en statussen.
- [ ] `00_register/master_register.csv` is bijgewerkt; `last_reviewed` is verzet.
- [ ] Alle paden in `path` bestaan op schijf.
- [ ] `99_changelog/changelog.md` bevat een dichte regel die naar deze release-notes verwijst.
- [ ] `versioning.schema_version` in het manifest is alleen aangepast als de structuur van het register wijzigt.

## Verifieerbare acceptatiecriteria

Lijst van controles waarmee een reviewer of auditor kan vaststellen dat de release klopt.

- [ ] Elke `stable` instructie heeft `version >= 1.0.0`.
- [ ] Geen enkele actieve adapter verwijst naar een `deprecated` bron zonder migratieplan.
- [ ] Wijzigingen zijn beschreven in `99_changelog/changelog.md`.
- [ ] PR-titel verwijst naar het juiste issuenummer.

## Vervolg

Optionele paragraaf met openstaande punten, geplande vervolg-releases of openstaande issues.
