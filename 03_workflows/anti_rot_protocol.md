---
instruction_id: workflow.anti_rot_protocol
version: 1.0.0
status: stable
owner: A. Verboon
last_reviewed: 2026-05-11
---

# Workflow: Anti-Rot Protocol

## Doel

Voorkom dat Spaces, agents en promptsets langzaam uit elkaar groeien.

## Regels

- **Geen stille lokale wijzigingen**: elke inhoudelijke wijziging in een Space moet terug naar het register.
- **Versie boven kopie**: verwijs naar instructie-ID en versie in plaats van lange tekst te dupliceren.
- **Maandelijkse review**: controleer actieve Spaces tegen het masterregister.
- **Adaptercontrole**: platform-specifieke wijzigingen horen in adapterbestanden, niet in generieke bronbestanden.
- **Changelog verplicht**: elke wijziging met impact krijgt een korte changelogregel.

## Drift-signalen

- De Space bevat lange instructies zonder bronverwijzing.
- Twee Spaces hebben bijna dezelfde instructie, maar met kleine verschillen.
- Een gebruiker corrigeert telkens hetzelfde gedrag.
- Een instructie verwijst naar verouderde tools, mappen of rollen.
- Er is geen eigenaar of reviewdatum.

