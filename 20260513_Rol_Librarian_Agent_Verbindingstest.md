# Rol Librarian Agent — Verbindingstest

**Datum:** 2026-05-13
**Auteur:** Librarian Agent (Perplexity Space "Prompt analyst, manager en orchestrator")
**Owner-account:** ArieJanVerboon (admin van Inspreadables)
**Repository:** Inspreadables/prompt-governance-system (branch: main)
**Status:** ✅ Verbindingstest geslaagd

---

## Samenvatting van mijn rol als Librarian Agent

Ik fungeer als **Librarian Agent** binnen het prompt-governance-systeem van Inspreadables. Mijn kerntaken:

- **Genereren** van analyses en teksten volgens de 8 vastgestelde skeletten.
- **Voorbereiden** van elke output voor directe opslag in de centrale repository (`Inspreadables/prompt-governance-system`, branch `main`).
- **Aanbieden** van een kant-en-klare "Save-to-Vault" link onder elk inhoudelijk antwoord, zodat het document met één klik als `.md`-bestand kan worden vastgelegd in de Kluis.
- **Naamgeving** volgt het patroon `[YYYYMMDD]_[TITEL].md` met underscores in plaats van spaties, conform de taxonomie- en governance-standaarden.
- **URL-encoding** van de volledige inhoud, zodat opmaak, enters en speciale tekens behouden blijven bij doorgifte via de GitHub `new file`-route.
- **Directe commits** via de GitHub-connector (`gh` CLI) zodra autorisatie is verleend — sneller en betrouwbaarder dan de handmatige link-route.

Op deze manier blijft elke gegenereerde output **traceable**, **versioneerbaar** en **anti-fragiel** opgenomen in de kennisarchitectuur.

---

## Technische verbindingscheck (uitgevoerd 2026-05-13, 23:11 CEST)

| Check | Resultaat |
|---|---|
| OAuth App access (Inspreadables) | ✅ Goedgekeurd via Optie B (settings/applications) |
| Membership `ArieJanVerboon` | ✅ Active, role: admin |
| Repo-lookup `prompt-governance-system` | ✅ Privé, default branch `main` |
| Zichtbare repos in org | 5 (test-automation, Backup, baakie-orchestrator, petra-reporting-prototype, prompt-governance-system) |
| Schrijfrechten via `gh` CLI | ✅ Bevestigd door deze commit |

---

## Vervolgafspraken

1. Vanaf nu commit ik documenten **direct** naar de Kluis op verzoek, in plaats van alleen een Save-to-Vault link aan te bieden.
2. De Save-to-Vault link blijft beschikbaar als fallback en voor handmatige review.
3. Bestandsnaamconventie blijft `[YYYYMMDD]_[TITEL].md` met underscores.
4. Alle commits gebeuren op branch `main` tenzij anders gespecificeerd.
