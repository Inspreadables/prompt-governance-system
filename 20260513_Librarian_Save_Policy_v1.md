---
datum: 2026-05-13
type: governance
status: actief
versie: 1.0
auteur: Librarian Agent
tags: [librarian, save-policy, triggers, workflow]
---

# Librarian Save Policy v1

## Beslissingsmatrix

| Wat de gebruiker wil | Wat de gebruiker zegt | Wat Librarian doet |
|---|---|---|
| Direct naar Kluis | "commit" / "vault" / "naar de kluis" / "PR" / "save" / "bewaar" | Open PR via `vault-inbox/*` naar `main` |
| Alleen in chat | (niets — default) | Genereer + toon mini-banner met klaargemaakte titel |
| Handmatige review via GitHub UI | "geef me de Save-to-Vault link" | URL-encoded `new file`-link |
| Verzamel-update | "weekly batch" | CHANGELOG-PR met index van losse fragmenten |
| Geen proactieve vragen | "stille modus" | Vraag niet meer proactief |
| Vragen weer aan | "alert modus" | Hervat proactieve vragen |

## Proactieve vraag — wanneer wel

Librarian vraagt actief "wil je dit naar de Kluis?" bij:

1. **Skelet-output** — tekst volgt expliciet één van de 8 skeletten.
2. **Lange analyses** — >800 woorden met structuur en bronnen.
3. **Governance-beslissingen** — workflow-keuzes, policy-wijzigingen, taxonomie-updates.

Bij al het andere geldt: stilte = chat-only.

## Trigger-detectie regels

- Triggerwoord moet in de huidige of vorige beurt staan.
- Casus-ongevoelig.
- "Commit" als zelfstandig woord, niet als deel van bv. "committeren" of "commitment".
- Bij twijfel: één korte vraag "Bedoel je naar de Kluis?" — geen lange ceremonie.

## PR-conventies

- Branchnaam: `vault-inbox/[skelet-type-of-trefwoord]-[YYYYMMDD]`
- Titel: `[skelet|docs|governance]: korte beschrijving`
- Body: één-regel samenvatting + frontmatter-preview + checklist (taxonomie ✓, frontmatter ✓, naam ✓).
- Eén document per PR (tenzij expliciet anders gevraagd).

## Frontmatter — minimum verplicht

```yaml
---
datum: YYYY-MM-DD
type: [skelet-1 | skelet-2 | ... | skelet-8 | governance | analyse | notitie]
status: [draft | actief | gearchiveerd]
versie: x.y
auteur: [naam of agent]
tags: [lijst]
---
```

## Wat deze policy expliciet NIET is

- Geen volledige auto-commit per antwoord (PR-moeheid, ruis).
- Geen pure handmatige modus (vergeet-risico, kennislekkage).
- Geen rigide formulier — één triggerwoord volstaat.

## Reviewcyclus voor deze policy

- Elke 3 maanden: evalueren of triggerwoorden uitgebreid moeten worden.
- Bij elke nieuwe skelet-toevoeging: frontmatter-types updaten.
- Bij elk falen (gemiste commit, ongewenste PR): root-cause toevoegen aan changelog van deze policy.
