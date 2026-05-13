---
instruction_id: governance.cost_token_control
version: 0.1.0
status: draft
owner: A. Verboon
last_reviewed: 2026-05-13
---

# Kosten- en tokencontrolebeleid

**Instruction ID:** `governance.cost_token_control`
**Versie:** 0.1.0
**Status:** draft
**Eigenaar:** A. Verboon
**Laatst herzien:** 2026-05-13

## Doel

Beperk onnodig tokenverbruik en kosten bij werk met agents (Claude Code, Custom GPT, Perplexity, Copilot, Cursor) op deze repo. Dit beleid bepaalt wanneer een agent in **lean mode** werkt en wanneer pas **volledige governanceverwerking** mag worden ingezet. Het beleid is generiek: agents en menselijke bijdragers passen het toe ongeacht het platform.

## Scope

Geldt voor elke interactie waarin een agent of bijdrager wijzigingen aan deze repo of aan een aangesloten Space/Project voorbereidt of uitvoert. Geldt niet voor het inhoudelijk schrijven van een instructie zelf zodra de gebruiker `verwerk` of `voer uit` heeft gegeven.

## Modi

| Modus                          | Wanneer                                                                                          | Standaardgedrag                                                                                                                                                                  |
| ------------------------------ | ------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Lean mode** (standaard)      | Default tenzij de gebruiker expliciet om volledige governanceverwerking vraagt.                  | Kort plan of advies eerst. Geen nieuwe bestanden, registerupdates of changelogregels zonder expliciete opdracht. Tests met korte prompts. Rapportage: alleen PASS/FAIL + advies. |
| **Sandbox-test**               | Gebruiker vraagt om bewijs voor productie-update.                                                | Voer test uit in een geïsoleerde context (concept-bestand, dry-run, voorbeeld-prompt). Rapporteer PASS/FAIL, gaten, risico, advies. Geen registermutaties.                       |
| **Volledige governanceverwerking** | Gebruiker geeft `verwerk` of `voer uit` of vraagt expliciet om volledige verwerking.            | Pas conventies uit `governance.versioning_release_policy` en `governance.instruction_id_convention` volledig toe. Manifest, masterregister, frontmatter, changelog en validatie.  |

## Lean mode-regels

1. **Kort plan of advies eerst.** Geef in maximaal vijf regels het voorstel en de impact. Wacht op akkoord voor uitvoering.
2. **Geen nieuwe bestanden** tenzij de gebruiker `maak bestand` of `voer uit` zegt. Gebruik bestaande bestanden eerst.
3. **Alleen blijvende standaarden, templates, adapters of broninstructies** rechtvaardigen een nieuw bestand. Ad-hoc analyses blijven in de chat.
4. **Geen automatische registermutaties.** Werk `instruction_manifest.yaml`, `master_register.csv`, `13_anti_rot_register.md`, `16_changelog.md`, manifest of masterregister niet bij zonder `verwerk`.
5. **Verzamel concept-updates.** Houd voorgestelde register-, manifest- en changelogregels in een lijst gereed; verwerk pas na opdracht.
6. **Sandbox waar mogelijk.** Test wijzigingen tegen een korte voorbeeld-prompt of dry-run voordat productie-bestanden raken.
7. **Compacte rapportage.** Standaardformaat: PASS/FAIL, gaten, risico, advies. Geen lange reflecties als een checklist volstaat.

## Kostenwaarschuwing (verplicht voor de agent)

Voordat een van onderstaande acties wordt gestart, **moet** de agent expliciet een kostenwaarschuwing geven én een goedkoper batch-alternatief voorstellen. Pas na expliciete goedkeuring van de gebruiker mag de setup-zware of multi-agent route worden uitgevoerd.

- Meerdere subagents tegelijk (parallel of seriëel).
- Brede bestandsscans (bijvoorbeeld `**/*` over de hele repo).
- Aanmaken of bewerken van meerdere documenten in één run.
- Herhaalde setup-zware operaties (cloning, dependency-installs, container-builds).
- Reeks issues één-voor-één afhandelen in plaats van in één batch.
- Brede audits (meer dan één Space of meer dan één adapter tegelijk).
- Aansluiten of bevragen van meerdere externe tools of connectors.

Format kostenwaarschuwing:

```text
Kostenwaarschuwing: <korte beschrijving van de zware route>.
Goedkoper alternatief: <batch- of lean-variant met geschatte besparing>.
Akkoord nodig: ja/nee?
```

## Standaardvraag bij multi-file werk

Voordat een agent meer dan één bestand aanpast of meer dan één issue tegelijk verwerkt, stelt de agent de volgende vraag aan de gebruiker:

> **Wil je lean plan, sandbox-test of volledige governanceverwerking?**

Definities die de agent bij de vraag meegeeft:

- **Lean plan:** kort voorstel in chat, geen bestanden, geen register-updates. Goedkoopste optie.
- **Sandbox-test:** voer in concept of dry-run uit, rapporteer PASS/FAIL en risico, geen registermutaties.
- **Volledige governanceverwerking:** bron, manifest, masterregister, frontmatter, changelog en validatie volgens `governance.versioning_release_policy` en `governance.manifest_validation_specification`.

## Repo-specifieke conditie

Als de actieve repository bestanden bevat als `13_anti_rot_register.md`, `16_changelog.md`, een manifest of een masterregister: werk deze in lean mode nooit automatisch bij. Verzamel voorgestelde regels als concept en verwerk uitsluitend na `verwerk`. In deze repo zijn de relevante registers `00_register/instruction_manifest.yaml`, `00_register/master_register.csv` en `99_changelog/changelog.md`; dezelfde regel geldt.

## Triggers en commando's

| Commando van gebruiker      | Effect                                                                                              |
| --------------------------- | --------------------------------------------------------------------------------------------------- |
| `lean`                      | Forceer lean mode voor de rest van de sessie of taak.                                              |
| `maak bestand`              | Sta het aanmaken van één concreet nieuw bestand toe binnen lean mode.                              |
| `voer uit`                  | Sta uitvoering toe van het laatst voorgestelde plan binnen de gegeven scope.                       |
| `verwerk`                   | Promoveer verzamelde concepten naar manifest, masterregister, changelog en eventueel adapters.    |
| `volledige governance`      | Schakel over naar volledige governanceverwerking; alle relevante registers worden meegenomen.      |
| `sandbox`                   | Voer in dry-run of conceptmodus uit; alleen rapportage, geen registermutaties.                     |

## Rapportagestijl

- Kort, blokvormig, geen lange essays.
- Standaardvelden bij tests: **PASS/FAIL**, **gaten**, **risico**, **advies**.
- Verwijs naar `instruction_id` en eventueel `@versie` in plaats van lange citaten.
- Geen tussentijdse statusrapporten van meer dan twee regels per stap.

## Relatie tot andere instructies

- Volgt taalconventies uit `global.communication_style`.
- Kwaliteitslat blijft `global.quality_standards`; dit beleid bepaalt alleen wanneer welke diepte aan rapportage of verwerking past.
- Promotie naar `stable` (`>= 1.0.0`) volgt `governance.versioning_release_policy`.
- Validatie van registermutaties blijft `governance.manifest_validation_specification`.

## Openstaande punten

- Het beleid staat op `draft` totdat het minstens één maand actief is gebruikt en geëvalueerd op false positives (te streng) en false negatives (zware routes onaangekondigd uitgevoerd).
- Bij promotie naar `1.0.0` worden voorbeelden van kostenwaarschuwingen en sandboxtests toegevoegd op basis van praktijkervaring.
