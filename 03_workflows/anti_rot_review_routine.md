---
instruction_id: workflow.anti_rot_review_routine
version: 1.0.0
status: stable
owner: A. Verboon
last_reviewed: 2026-05-11
---

# Workflow: Anti-Rot Reviewroutine

## Doel

Een praktische, maandelijkse reviewroutine waarmee actieve Spaces en agents systematisch worden gecontroleerd op instructiedrift ten opzichte van het centrale register. De routine operationaliseert de regels uit [`workflow.anti_rot_protocol`](anti_rot_protocol.md) en is uitvoerbaar in **minder dan 30 minuten per Space**.

Deze routine is geen audit (zie [`workflow.prompt_audit_protocol`](prompt_audit_protocol.md) voor de diepere variant). Het is een lichte, terugkerende controle die drift vroeg signaleert en kleine afwijkingen meteen oplost of expliciet markeert.

## Wanneer uitvoeren

- **Maandelijks** voor elke actieve Space of agent in `00_register/master_register.csv` (kolom `used_in`).
- **Ad hoc** bij vermoeden van drift: een gebruiker corrigeert telkens hetzelfde gedrag, of een Space wijkt zichtbaar af van een vergelijkbare Space.
- **Direct na een release** van een bron-instructie waarop de Space leunt (zie [`governance.versioning_release_policy`](../00_register/versioning_and_release_policy.md)).

## Tijdsbudget: 25 minuten per Space

| Stap                                | Richttijd | Output                                      |
| ----------------------------------- | --------- | ------------------------------------------- |
| 1. Voorbereiden                     | 3 min     | Lijst actieve instructie-IDs en versies     |
| 2. Snelle scan op drift-signalen    | 5 min     | Hits of geen hits per signaal               |
| 3. Verschillen vastleggen           | 7 min     | Regels in afwijkingenlog                    |
| 4. Beslisregel toepassen            | 5 min     | Per afwijking: Space, register of accepteer |
| 5. Acties en terugkoppeling         | 5 min     | Wijzigingen, changelogregel, nieuwe datum   |

Loopt het uit boven 30 minuten, dan is dat zelf een signaal: ofwel de Space is te groot voor één review, ofwel er is teveel drift. Splits de Space of plan een volledige audit met [`workflow.prompt_audit_protocol`](prompt_audit_protocol.md).

## Reviewstappen

### 1. Voorbereiden

- Open de Space (runtime) én het masterregister `00_register/master_register.csv`.
- Noteer per Space welke instructie-IDs actief zijn en op welke versie.
- Zet de relevante adapter klaar: voor Perplexity Spaces is dat [`adapter.perplexity_space`](../05_agent_adapters/perplexity_space_adapter.md).

### 2. Snelle scan op drift-signalen

Loop deze signalen uit `workflow.anti_rot_protocol` af en markeer per signaal `hit` of `geen hit`:

- Lange instructies in de Space zonder verwijzing naar een instructie-ID.
- Twee Spaces die bijna dezelfde tekst bevatten met kleine verschillen.
- Gebruiker corrigeert telkens hetzelfde gedrag (vraag in de runtime na).
- Verwijzingen naar verouderde tools, mappen, rollen of versies.
- Ontbrekende eigenaar of laatste reviewdatum in de Space.
- Space pint expliciet op een oude versie terwijl in het register een nieuwere `stable` versie staat.

Geen hits in deze stap betekent: registreer alleen dat de review is uitgevoerd en sluit af. De resterende stappen sla je over.

### 3. Verschillen vastleggen

Open het [afwijkingenlog-template](../04_templates/deviation_log_template.md) (`template.deviation_log`) en leg per geconstateerde afwijking één regel vast. Houd het kort: één zin per veld is voldoende. Beschrijf wat afwijkt, niet hoe je het oplost — dat komt in de volgende stap.

### 4. Beslisregel toepassen

Voor elke afwijking kies je één van drie acties op basis van de onderstaande beslisregel.

#### Beslisregel

| Situatie                                                                                                                                | Actie                       |
| --------------------------------------------------------------------------------------------------------------------------------------- | --------------------------- |
| De Space wijkt af van het register, maar het register klopt nog steeds.                                                                 | **Update de Space/runtime** |
| De afwijking is een verbetering die ook in andere Spaces relevant is, of het register is verouderd ten opzichte van de praktijk.        | **Update het register**     |
| De afwijking is bewust en platform- of doelspecifiek, niet generaliseerbaar, en de eigenaar accepteert het risico.                      | **Accepteer expliciet**     |

Twijfel je tussen twee opties? Kies dan de actie die de kortste tekst in de Space oplevert (verwijzing boven kopie) en bewaar de discussie voor de volgende audit.

#### A. Update de Space/runtime

Kies dit wanneer:

- De Space een oudere versie gebruikt dan het `stable` register zonder reden om te pinnen.
- De Space tekst dupliceert die al in een bron- of adapterbestand staat.
- De Space een platformregel mist die in de adapter (`adapter.*`) is vastgelegd.
- Een gebruiker telkens dezelfde correctie geeft die al in `global.quality_standards` of een rol staat.

**Hoe**: pas de Space-bootstrap aan zodat zij verwijst naar de actuele instructie-IDs en versies. Volg de adapterregels (bijvoorbeeld `adapter.perplexity_space`). Geen wijziging aan bronbestanden nodig. Geen changelogregel nodig tenzij meerdere Spaces tegelijk worden bijgewerkt.

#### B. Update het centrale register

Kies dit wanneer:

- De afwijking een inhoudelijke verbetering is die voor meer dan één Space geldt.
- De praktijk is voortgegaan terwijl de broninstructie is achtergebleven.
- Een terugkerend `n.v.t.` of correctie in meerdere Spaces wijst op een ontbrekende of foute regel in de bron.

**Hoe**:

1. Wijzig het bronbestand in `01_global/`, `02_roles/`, `03_workflows/`, `04_templates/` of `05_agent_adapters/`.
2. Verhoog de versie volgens [`governance.versioning_release_policy`](../00_register/versioning_and_release_policy.md) (`PATCH` voor verduidelijking, `MINOR` voor additieve regels, `MAJOR` voor breken).
3. Werk frontmatter, `00_register/instruction_manifest.yaml` en `00_register/master_register.csv` in dezelfde commit bij. Volg [`governance.instruction_id_convention`](../00_register/instruction_id_convention.md).
4. Voeg een regel toe in `99_changelog/changelog.md`.
5. Werk daarna de Spaces bij die op de oude versie pinnen.

#### C. Accepteer de afwijking expliciet

Kies dit alleen wanneer:

- De afwijking platform- of klantspecifiek is en niet thuishoort in een generieke bron of adapter.
- De afwijking bewust experimenteel is en de eigenaar het risico draagt.
- Wijzigen meer kost dan accepteren én de afwijking geen drift veroorzaakt naar andere Spaces.

**Hoe**: registreer de afwijking in het afwijkingenlog van de Space met status `geaccepteerd`, eigenaar, datum en een herzieningsmoment (uiterlijk drie maandelijkse reviews verder). Geen wijziging aan bronbestand of register. Een geaccepteerde afwijking telt mee in de score `anti-rot` van [`template.space_audit_checklist`](../04_templates/space_audit_checklist.md): drie of meer geaccepteerde afwijkingen in één Space is een trigger voor een volledige audit.

### 5. Acties en terugkoppeling

- Voer de gekozen acties uit. Houd elke wijziging klein en logisch in één commit.
- Werk per gewijzigd bestand de frontmatter `last_reviewed` bij naar de reviewdatum.
- Werk de relevante rijen in `00_register/master_register.csv` bij (`version`, `status`, `last_reviewed`).
- Voeg waar van toepassing één regel toe in `99_changelog/changelog.md`.
- Draai `python3 tools/validate_manifest.py` en los fouten en waarschuwingen op.
- Noteer in het afwijkingenlog van de Space dat de review is afgerond, inclusief datum en gekozen acties.

## Output van één review

Per Space lever je drie dingen op:

1. Een ingevuld of bijgewerkt [afwijkingenlog](../04_templates/deviation_log_template.md) (zelfs als de log leeg blijft, leg je de reviewdatum vast).
2. Eventuele commits met wijzigingen in Space, register of bronbestanden.
3. Een datum voor de volgende review (standaard +1 maand).

## Verhouding tot andere instructies

- [`workflow.anti_rot_protocol`](anti_rot_protocol.md) — de regels die deze routine afdwingt.
- [`workflow.prompt_audit_protocol`](prompt_audit_protocol.md) — de diepere audit die je inzet als de routine te vaak hits oplevert.
- [`template.space_audit_checklist`](../04_templates/space_audit_checklist.md) — de checklist voor die diepere audit.
- [`template.deviation_log`](../04_templates/deviation_log_template.md) — het invulformat dat deze routine gebruikt.
- [`governance.versioning_release_policy`](../00_register/versioning_and_release_policy.md) — bepaalt hoe een register-update wordt geversied.
- [`governance.instruction_id_convention`](../00_register/instruction_id_convention.md) — bepaalt naamgeving bij nieuwe instructies.
- [`global.quality_standards`](../01_global/quality_standards.md) — bepaalt de kwaliteitslat waaraan een Space wordt getoetst.
- [`adapter.perplexity_space`](../05_agent_adapters/perplexity_space_adapter.md) — bepaalt hoe de Space-bootstrap eruitziet bij een runtime-update.
