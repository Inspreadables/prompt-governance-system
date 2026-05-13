---
datum: 2026-05-13
type: governance
status: actief
versie: 1.0
auteur: Librarian Agent
tags: [kluis, workflow, anti-fragiel, governance, drie-laagsmodel]
---

# Kluis Workflow — Anti-fragiel Drie-laagsmodel

## Doel

Een werkbare, stress-bestendige flow voor het opslaan van Librarian-outputs in `Inspreadables/prompt-governance-system`, waarbij fouten klein blijven en de Kluis bron van waarde wordt in plaats van vervuiling.

## De drie lagen

### Laag 1 — Draft (in chat)
- Librarian genereert in de Perplexity-chat.
- Geen GitHub-actie.
- Mini-banner onderaan: `📋 Klaar voor Kluis · titel: [YYYYMMDD]_[TITEL].md`
- Fouten kosten nul commits.

### Laag 2 — Vault-inbox (branch `vault-inbox/*`)
- Op trigger commit Librarian naar een dedicated branch.
- Automatische Pull Request naar `main`.
- Frontmatter YAML + conventional commit message.
- Eén document per PR.

### Laag 3 — Main (canonieke Kluis)
- Alleen gemergde, gereviewde content.
- Geen force-pushes, geen rebases.
- Tagged releases voor mijlpalen.

## Anti-fragiele eigenschappen

| Eigenschap | Hoe ingevuld |
|---|---|
| Optioneel | Drie routes (chat, expliciete commit, weekly batch) |
| Reversibel | PR sluiten = één klik, geen `main`-vervuiling |
| Zichtbaar | Commit-hash + PR-historie + diff per document |
| Klein-stappig | Eén document per PR, geen bulk-dumps |
| Zelf-corrigerend | Mens-in-de-lus bij elke merge |
| Redundant | Connector down → Save-to-Vault link; link down → directe commit; beide down → `.md`-export |

## Bestandsconventie

- Naam: `[YYYYMMDD]_[TITEL_MET_UNDERSCORES].md`
- Frontmatter verplicht: `datum`, `type`, `status`, `versie`, `auteur`, `tags`
- Conventional commits: `feat(librarian):`, `docs:`, `refactor:`, `chore:`

## Niet doen

- Geen automatische commits zonder trigger.
- Geen rebases of force-pushes op `main`.
- Geen meerdere documenten in één PR (uitzondering: bootstrap).
- Geen lange brainstorms in de Kluis — die blijven in chat.
