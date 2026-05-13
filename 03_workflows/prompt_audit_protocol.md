---
instruction_id: workflow.prompt_audit_protocol
version: 1.0.0
status: stable
owner: A. Verboon
last_reviewed: 2026-05-11
---

# Workflow: Prompt Audit Protocol

## Doel

Gebruik dit protocol om een Space, agentinstructie of promptset te auditen.

## Auditstappen

1. **Identificeer de runtime**: bepaal waar de instructie draait, bijvoorbeeld Space, Claude Project, Custom GPT of workflowtool.
2. **Bepaal de bronstatus**: controleer of de instructie ook in het centrale register bestaat.
3. **Splits de lagen**: onderscheid globale principes, rol, workflow, taaktemplate en adapter.
4. **Check conflicten**: zoek tegenstrijdigheden tussen lokale instructies en broninstructies.
5. **Check onderhoudbaarheid**: beoordeel of de instructie eenvoudig te updaten, testen en hergebruiken is.
6. **Maak aanbevelingen**: geef concrete acties: behouden, splitsen, verplaatsen, herschrijven of registreren.
7. **Werk governance bij**: update manifest, masterregister en changelog.

## Auditoutput

Gebruik deze structuur:

- Samenvatting
- Sterke punten
- Risico's
- Ontbrekende instructielagen
- Aanbevolen opslagmodel
- Concrete wijzigingen
- Open vragen
