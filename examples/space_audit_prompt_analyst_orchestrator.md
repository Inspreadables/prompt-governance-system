# Voorbeeld-audit: Space `Prompt analyst, manager en orchestrator`

Dit is een **uitgewerkte voorbeeld-audit** voor één concrete Space. Het document is bedoeld als referentie bij het invullen van toekomstige audits. Het volgt de structuur uit [`template.space_audit_checklist`](../04_templates/space_audit_checklist.md) en gebruikt de beslisregel en het afwijkingenlog uit [`workflow.anti_rot_review_routine`](../03_workflows/anti_rot_review_routine.md) en [`template.deviation_log`](../04_templates/deviation_log_template.md).

> Dit voorbeeld is bewust gegeneriek. Namen, datums en bevindingen zijn illustratief; er staan geen account-, klant- of toegangsgegevens in. Kopieer dit bestand niet één-op-één naar een echte Space-audit — vul je eigen bevindingen in.

## Verhouding tot het register

Deze audit operationaliseert:

- [`workflow.prompt_audit_protocol`](../03_workflows/prompt_audit_protocol.md) — stap 1 t/m 7 vormen de structuur.
- [`workflow.anti_rot_protocol`](../03_workflows/anti_rot_protocol.md) — definieert wat als drift telt.
- [`workflow.anti_rot_review_routine`](../03_workflows/anti_rot_review_routine.md) — levert de beslisregel `update_space` / `update_register` / `accept`.
- [`template.space_audit_checklist`](../04_templates/space_audit_checklist.md) — levert de scorevelden en ELI5-versie.
- [`global.quality_standards`](../01_global/quality_standards.md) — bepaalt de kwaliteitslat.
- [`adapter.perplexity_space`](../05_agent_adapters/perplexity_space_adapter.md) — bepaalt hoe de Space-tekst zelf wordt bijgewerkt na `update_space`.

## Auditmetadata

- Naam van de Space of agent: **Prompt analyst, manager en orchestrator**
- Runtime: **Perplexity Space**
- Eigenaar: A. Verboon
- Auditor: A. Verboon
- Auditdatum: 2026-05-12
- Versie van bronregister gebruikt: zie `00_register/instruction_manifest.yaml` (commit op `main`, 2026-05-12)
- Actieve adapter: `adapter.perplexity_space@1.0.0`
- Verwijzing naar relevante instructie-IDs:
  - `role.prompt_analyst_manager_orchestrator@1.0.0`
  - `workflow.prompt_audit_protocol@1.0.0`
  - `workflow.anti_rot_protocol@1.0.0`
  - `workflow.anti_rot_review_routine@1.0.0`
  - `global.operating_principles@1.0.0`
  - `global.communication_style@1.0.0`
  - `global.quality_standards@1.0.0`
  - `template.space_audit_checklist@1.0.0`
  - `template.deviation_log@1.0.0`
  - `adapter.perplexity_space@1.0.0`

## Checklist met scores

Scoreschaal: `0` ontbreekt, `1` onvolledig, `2` bruikbaar met verbeterpunten, `3` volledig en herbruikbaar, `n.v.t.` niet van toepassing.

### 1. Duidelijkheid (clarity)

Toetst aan `global.quality_standards`.

| # | Item | Score | Toelichting |
| - | ---- | ----- | ----------- |
| 1 | Doel van de Space is in één zin uitlegbaar. | 3 | Bootstrap noemt expliciet dat de Space prompts en agent-workflows analyseert, manageert en orkestreert. |
| 2 | Rol is expliciet benoemd. | 3 | Verwijst naar `role.prompt_analyst_manager_orchestrator@1.0.0`. |
| 3 | Verwachte output is beschreven. | 2 | Standaard outputvolgorde staat in de Space, maar het detailniveau van de "concrete wijzigingen"-sectie is nog wat open. |
| 4 | Vrij van interne jargon zonder uitleg. | 3 | Termen als "bron", "adapter", "runtime", "audit" worden in de Space-bootstrap uitgelegd. |
| 5 | Nieuwe gebruiker kan binnen 5 minuten starten. | 2 | Drie standaardvragen aan de start helpen; een minimaal voorbeeldverzoek in de Space zou de drempel verder verlagen. |

Subtotaal duidelijkheid: **13 / 15**.

### 2. Modulariteit (modularity)

Toetst aan `workflow.prompt_audit_protocol`, stap 3 (splits de lagen).

| # | Item | Score | Toelichting |
| - | ---- | ----- | ----------- |
| 1 | Globale principes, rol, workflow, template en adapter zijn herkenbaar gescheiden. | 3 | Bootstrap volgt het lagenmodel uit `adapter.perplexity_space` (bron, adapter, runtime, audit). |
| 2 | Geen gedupliceerde tekst die ook in het register staat. | 2 | Eén zin over "splits adviezen in vier lagen" herhaalt de adaptertekst; geen blokkerend duplicaat, maar `update_space` kan dit korter maken. |
| 3 | Platform-specifieke gedragingen in de adapterlaag. | 3 | Perplexity-eigen beperkingen (Space kan register niet lezen, handmatige sync) staan in `adapter.perplexity_space`, niet in de Space-tekst. |
| 4 | Space verwijst naar instructie-IDs in plaats van lange tekstkopieën. | 3 | Alle instructies worden via ID genoemd, niet uitgeschreven. |

Subtotaal modulariteit: **11 / 12**.

### 3. Herbruikbaarheid (reusability)

Toetst aan `global.quality_standards` en `workflow.prompt_audit_protocol`.

| # | Item | Score | Toelichting |
| - | ---- | ----- | ----------- |
| 1 | Instructie is bruikbaar in meer dan één Space. | 3 | Dezelfde rol kan ook in `adapter.claude_project` of `adapter.custom_gpt` worden geprojecteerd. |
| 2 | Rol kan worden hergebruikt met een andere workflow. | 3 | `role.prompt_analyst_manager_orchestrator` koppelt expliciet aan `workflow.prompt_audit_protocol`, maar is generiek genoeg voor andere workflows. |
| 3 | Workflow kan worden hergebruikt met een andere rol. | 3 | `workflow.prompt_audit_protocol` is rolneutraal. |
| 4 | Templates en adapters kunnen onafhankelijk worden bijgewerkt. | 3 | Versies van `template.space_audit_checklist@1.0.0` en `adapter.perplexity_space@1.0.0` zijn losgekoppeld. |

Subtotaal herbruikbaarheid: **12 / 12**.

### 4. Anti-rot

Toetst aan `workflow.anti_rot_protocol`.

| # | Item | Score | Toelichting |
| - | ---- | ----- | ----------- |
| 1 | Elke actieve instructie heeft een instructie-ID en versie. | 3 | Bootstrap noemt de v1-IDs expliciet. |
| 2 | Eigenaar en laatste reviewdatum zichtbaar. | 3 | `Eigenaar: A. Verboon`, `Laatst gereviewd: 2026-05-12`. |
| 3 | Geen stille lokale wijzigingen ten opzichte van het register. | 2 | Eén lokale toevoeging gevonden: een extra zin over "altijd in het Nederlands antwoorden". Niet in `global.communication_style` afgedwongen — zie afwijking #2 hieronder. |
| 4 | Geen langzaam afwijkende kopie elders. | 3 | Geen tweede Space met overlappende inhoud aangetroffen. |
| 5 | Geen verouderde verwijzingen naar tools, mappen of rollen. | 3 | Alle verwijzingen kloppen met de huidige repo-structuur. |
| 6 | Elke wijziging met impact staat in de changelog. | 2 | Laatste runtime-update aan deze Space is niet in `99_changelog/changelog.md` opgenomen — zie afwijking #3. |

Subtotaal anti-rot: **16 / 18**.

### Totaal

- Totaal: **52 / 57**
- Indicatieve status (zie drempels in `template.space_audit_checklist`):
  - `50-57` → **Sterk. Geschikt als referentie-Space.**
- Geen `n.v.t.`-items in deze audit, dus de noemer blijft 57.

## ELI5-samenvatting

Voor lezers zonder governance-achtergrond. Vijf vragen uit `template.space_audit_checklist` met duim-omhoog (👍), duim-opzij (👌) of duim-omlaag (👎).

1. **Snap ik in één zin wat deze Space doet?** 👍 — analyseert en organiseert prompts en agent-workflows.
2. **Weet ik welke "pet" de agent op heeft?** 👍 — promptanalist, manager en orchestrator.
3. **Is duidelijk hoe een goed antwoord eruitziet?** 👌 — de outputvolgorde staat in de Space, maar een mini-voorbeeld zou helpen.
4. **Staat de uitleg ook ergens buiten deze Space?** 👍 — alles staat in dit register en is via instructie-IDs te vinden.
5. **Weet ik wie verantwoordelijk is en wanneer het laatst is nagekeken?** 👍 — eigenaar en reviewdatum staan bovenaan de Space.

Vier duimen omhoog en één duim opzij: prima startpunt, kleine verbetering aanbevolen voor punt 3.

## Auditoutput (samenvatting)

Conform uitvoerstructuur van `workflow.prompt_audit_protocol`.

- **Samenvatting**: De Space `Prompt analyst, manager en orchestrator` is stabiel, modulair en goed gekoppeld aan het register. Drie kleine afwijkingen vragen actie, geen ervan blokkeert gebruik.
- **Sterke punten**: heldere rolomschrijving, expliciet lagenmodel, consequente verwijzing via instructie-IDs, herbruikbare workflow- en templatebasis.
- **Risico's**: één lokale gedragsregel zonder bronregistratie en één ongedocumenteerde runtime-update. Beide kleine drift-signalen volgens `workflow.anti_rot_protocol`.
- **Ontbrekende instructielagen**: geen. Alle vier lagen (bron, adapter, runtime, audit) zijn aanwezig.
- **Aanbevolen opslagmodel**: bron en adapter ongewijzigd; runtime krijgt twee kleine aanpassingen; audit landt in dit voorbeeldbestand en in het afwijkingenlog van de Space.
- **Concrete wijzigingen**: zie tabel hieronder.
- **Open vragen**: moet "altijd in het Nederlands antwoorden" een generieke regel worden in `global.communication_style@1.1.0`, of blijft het een platform-keuze per Space?

## Afwijkingenlog (illustratief)

Volgt `template.deviation_log`. Drie regels, één per beslissing in de beslisregel uit `workflow.anti_rot_review_routine`.

| # | Datum gezien | Instructie-ID (`<id>@<versie>`) | Beschrijving van de afwijking | Reden / context | Beslissing | Status | Eigenaar | Herzieningsdatum | Referentie |
| - | ------------ | ------------------------------- | ----------------------------- | --------------- | ---------- | ------ | -------- | ---------------- | ---------- |
| 1 | 2026-05-12 | `adapter.perplexity_space@1.0.0` | Space-tekst dupliceert één zin over het lagenmodel die ook in de adapter staat. | Kopie ontstond bij eerste opzet; register klopt. | `update_space` | `in_uitvoering` | A. Verboon | 2026-05-19 | Volgt in eerstvolgende Space-edit; geen registerwijziging nodig. |
| 2 | 2026-05-12 | `global.communication_style@1.0.0` | Space dwingt "altijd Nederlands" af, terwijl de bron Nederlands én Engels toelaat. | Voorkeur van de eigenaar voor deze klantgroep; mogelijk breder relevant. | `update_register` | `open` | A. Verboon | 2026-06-12 | Open PR-voorstel: `global.communication_style@1.1.0` met expliciete taalkeuze per Space. |
| 3 | 2026-05-12 | `adapter.perplexity_space@1.0.0` | Vorige runtime-update aan de Space staat niet in `99_changelog/changelog.md`. | Update was tekstueel, geen impact op IDs; toch valt het onder "changelog verplicht" uit `workflow.anti_rot_protocol`. | `accept` | `geaccepteerd` | A. Verboon | 2026-08-12 | Acceptatie tot eerstvolgende inhoudelijke wijziging; daarna alsnog loggen. |

### Hoe deze drie beslissingen worden uitgevoerd

- **`update_space` (regel 1)** — Pas alleen de Space-bootstrap in Perplexity aan: verwijder de duplicaatzin en houd de verwijzing naar `adapter.perplexity_space@1.0.0`. Geen wijziging aan bronbestanden. Geen changelogregel nodig tenzij meerdere Spaces tegelijk worden bijgewerkt. Werk `Laatst gereviewd` in de Space bij naar `2026-05-12`.
- **`update_register` (regel 2)** — Open een PR die `01_global/communication_style.md` aanpast, verhoog naar `1.1.0` (additieve regel: expliciete taalkeuze per Space mag), werk frontmatter, `00_register/instruction_manifest.yaml` en `00_register/master_register.csv` bij in dezelfde commit volgens `governance.versioning_release_policy`. Voeg een regel toe in `99_changelog/changelog.md`. Pas daarna de Space-tekst aan zodat zij naar `global.communication_style@1.1.0` verwijst.
- **`accept` (regel 3)** — Leg de acceptatie vast in dit afwijkingenlog met herzieningsdatum 2026-08-12 (drie maandelijkse reviews vooruit). Bij de eerstvolgende inhoudelijke runtime-update wordt alsnog een changelogregel toegevoegd; tot dan geen actie.

## Terugkoppeling naar register

- Aanpassingen in `00_register/instruction_manifest.yaml`: alleen na uitvoering van regel 2 (versie van `global.communication_style` van `1.0.0` naar `1.1.0`).
- Aanpassingen in `00_register/master_register.csv`: idem, plus `last_reviewed` bijwerken naar uitvoeringsdatum.
- Regel voor `99_changelog/changelog.md`: bij uitvoering van regel 2 één regel met datum, instructie-ID en korte omschrijving; bij regel 1 en regel 3 geen changelogregel.
- Nieuwe of bijgewerkte adapters: geen.

## Volgende review

- Volgende anti-rot review: **2026-06-12**.
- Trigger voor vervroegde review: een vierde open `accept`-regel, of een `MINOR`/`MAJOR`-update van één van de genoemde bron-instructies.

## Hoe gebruik je dit voorbeeld

1. Kopieer dit bestand naar je eigen werkmap (niet terug naar `examples/`).
2. Vervang **Auditmetadata**, **Checklist met scores**, **Afwijkingenlog** en **Volgende review** met je eigen bevindingen.
3. Volg de stappen uit `workflow.anti_rot_review_routine` voor de uitvoering.
4. Voeg geen account-, klant- of toegangsgegevens toe. Houd het voorbeeldbestand in deze map zelf bewust generiek.
