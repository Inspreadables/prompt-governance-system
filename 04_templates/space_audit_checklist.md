---
instruction_id: template.space_audit_checklist
version: 0.1.0
status: draft
owner: A. Verboon
last_reviewed: 2026-05-11
---

# Template: Space Audit Checklist

## Doel

Een herbruikbare checklist om een Perplexity Space, Claude Project, Custom GPT of vergelijkbare agentomgeving snel te auditen. Deze checklist operationaliseert `workflow.prompt_audit_protocol` en bewaakt de regels uit `workflow.anti_rot_protocol` en `global.quality_standards`. Voor Perplexity Spaces wordt aanvullend gebruik gemaakt van `adapter.perplexity_space`.

## Hoe te gebruiken

1. Vul de auditmetadata in.
2. Loop de checklist sectie voor sectie door. Geef per item een score van 0 t/m 3 of markeer `n.v.t.`.
3. Tel de scores op per categorie en bepaal de eindstatus.
4. Werk daarna `00_register/instruction_manifest.yaml`, `00_register/master_register.csv` en `99_changelog/changelog.md` bij als er wijzigingen volgen.

### Scoreschaal

- `0` Niet aanwezig of onbruikbaar.
- `1` Aanwezig, maar onvolledig of onduidelijk.
- `2` Aanwezig en bruikbaar, met kleine verbeterpunten.
- `3` Volledig, duidelijk en herbruikbaar.
- `n.v.t.` Niet van toepassing voor deze runtime.

## Auditmetadata

- Naam van de Space of agent:
- Runtime (Perplexity Space, Claude Project, Custom GPT, anders):
- Eigenaar:
- Auditor:
- Auditdatum:
- Versie van bronregister gebruikt:
- Verwijzing naar relevante instructie-IDs:
  - `workflow.prompt_audit_protocol`
  - `workflow.anti_rot_protocol`
  - `global.quality_standards`
  - `adapter.perplexity_space` (alleen voor Perplexity Spaces)

## Checklist

### 1. Duidelijkheid (clarity)

Verwijst naar `global.quality_standards`.

- [ ] Het doel van de Space is in één zin uitlegbaar. Score: __
- [ ] De rol van de agent is expliciet benoemd. Score: __
- [ ] De verwachte output (formaat, structuur, detailniveau) is beschreven. Score: __
- [ ] De instructies zijn vrij van interne jargon zonder uitleg. Score: __
- [ ] Een nieuwe gebruiker kan binnen 5 minuten starten zonder extra uitleg. Score: __

Subtotaal duidelijkheid: __ / 15

### 2. Modulariteit (modularity)

Verwijst naar `workflow.prompt_audit_protocol` (stap 3: splits de lagen).

- [ ] Globale principes, rol, workflow, template en adapter zijn herkenbaar gescheiden. Score: __
- [ ] Er staat geen gedupliceerde tekst in de Space die ook in het register staat. Score: __
- [ ] Platform-specifieke gedragingen staan in een adapter, niet in een generieke laag. Score: __
- [ ] De Space verwijst naar instructie-IDs in plaats van lange tekstkopieën. Score: __

Subtotaal modulariteit: __ / 12

### 3. Herbruikbaarheid (reusability)

Verwijst naar `global.quality_standards` en `workflow.prompt_audit_protocol`.

- [ ] De instructie is bruikbaar in meer dan één Space of project. Score: __
- [ ] De rol kan worden hergebruikt met een andere workflow. Score: __
- [ ] De workflow kan worden hergebruikt met een andere rol. Score: __
- [ ] Templates en adapters kunnen onafhankelijk worden bijgewerkt. Score: __

Subtotaal herbruikbaarheid: __ / 12

### 4. Anti-rot

Verwijst naar `workflow.anti_rot_protocol`.

- [ ] Elke actieve instructie heeft een instructie-ID en versie. Score: __
- [ ] Er is een eigenaar en een laatste reviewdatum. Score: __
- [ ] Er zijn geen stille lokale wijzigingen ten opzichte van het register. Score: __
- [ ] Er is geen langzaam afwijkende kopie van een instructie elders. Score: __
- [ ] Verouderde verwijzingen naar tools, mappen of rollen ontbreken. Score: __
- [ ] Elke wijziging met impact staat in de changelog. Score: __

Subtotaal anti-rot: __ / 18

## Totaalscore en status

- Totaal: __ / 57
- Indicatieve status:
  - `0-19` Hoog risico, niet productie-waardig. Herstructureer eerst.
  - `20-37` Matig. Bruikbaar, maar belangrijke aanpassingen nodig.
  - `38-49` Goed. Kleine verbeteringen aanbevolen.
  - `50-57` Sterk. Geschikt als referentie-Space.

`n.v.t.`-items tellen niet mee in de noemer. Pas de drempels naar verhouding aan.

## Aanbevolen acties

Gebruik de uitvoerstructuur uit `workflow.prompt_audit_protocol`:

- Samenvatting:
- Sterke punten:
- Risico's:
- Ontbrekende instructielagen:
- Aanbevolen opslagmodel (bron, adapter, runtime):
- Concrete wijzigingen (behouden, splitsen, verplaatsen, herschrijven, registreren):
- Open vragen:

## Terugkoppeling naar register

- Aanpassingen in `00_register/instruction_manifest.yaml`:
- Aanpassingen in `00_register/master_register.csv`:
- Regel voor `99_changelog/changelog.md`:
- Nieuwe of bijgewerkte adapters:

---

## ELI5-versie

Voor gebruikers zonder technische achtergrond. Loop deze vijf vragen langs en geef bij elke vraag een duim omhoog, duim opzij of duim omlaag.

1. **Snap ik in één zin wat deze Space doet?**
   Als je het niet aan een collega kunt uitleggen, is de uitleg te vaag.
2. **Weet ik welke "pet" de agent op heeft?**
   Bijvoorbeeld: adviseur, analist, schrijver. Niet meerdere petten tegelijk zonder uitleg.
3. **Is duidelijk hoe een goed antwoord eruitziet?**
   Lengte, vorm, voorbeeld of stijl moeten ergens benoemd zijn.
4. **Staat de uitleg ook ergens buiten deze Space?**
   Zo niet, dan kan de Space langzaam afdwalen zonder dat iemand het merkt.
5. **Weet ik wie verantwoordelijk is en wanneer het laatst is nagekeken?**
   Geen naam en geen datum betekent: niemand houdt het bij.

Drie of meer duimen omhoog: prima startpunt. Twee of minder: vraag de eigenaar om het te verbeteren voordat je erop bouwt.
