#!/usr/bin/env python3
"""Valideer instruction_manifest.yaml, master_register.csv en bronbestanden.

Specificatie: 00_register/manifest_validation_specification.md
Voer uit met: python3 tools/validate_manifest.py
"""

from __future__ import annotations

import csv
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write(
        "Dit script heeft de Python-bibliotheek 'PyYAML' nodig.\n"
        "Installeer hem met: pip install pyyaml\n"
    )
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "00_register" / "instruction_manifest.yaml"
REGISTER_PATH = REPO_ROOT / "00_register" / "master_register.csv"

ID_PATTERN = re.compile(r"^[a-z0-9_]+(\.[a-z0-9_]+){1,3}$")
SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

ALLOWED_PREFIXES = {"global", "role", "workflow", "template", "adapter", "governance"}
ALLOWED_STATUSES = {"draft", "review", "stable", "deprecated"}

PREFIX_TO_DIR = {
    "global": "01_global",
    "role": "02_roles",
    "workflow": "03_workflows",
    "template": "04_templates",
    "adapter": "05_agent_adapters",
    "governance": "00_register",
}

SOURCE_DIRS = [
    "00_register",
    "01_global",
    "02_roles",
    "03_workflows",
    "04_templates",
    "05_agent_adapters",
]

REQUIRED_MANIFEST_FIELDS = ("instruction_id", "path", "version", "status", "applies_to")
REQUIRED_FRONTMATTER_FIELDS = ("instruction_id", "version", "status", "owner", "last_reviewed")


class Report:
    def __init__(self) -> None:
        self.errors: list[dict] = []
        self.warnings: list[dict] = []

    def error(self, code: str, summary: str, file: str, what: str, fix: str) -> None:
        self.errors.append(
            {"code": code, "summary": summary, "file": file, "what": what, "fix": fix}
        )

    def warning(self, code: str, summary: str, file: str, what: str, fix: str) -> None:
        self.warnings.append(
            {"code": code, "summary": summary, "file": file, "what": what, "fix": fix}
        )

    def print(self) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Manifestvalidatie — {timestamp}")
        print(f"Repo: {REPO_ROOT}")
        print(f"Manifest: {MANIFEST_PATH.relative_to(REPO_ROOT)}")
        print(f"Masterregister: {REGISTER_PATH.relative_to(REPO_ROOT)}")
        print("-" * 72)

        if self.errors:
            print(f"\nFouten ({len(self.errors)}):\n")
            for m in self.errors:
                _print_message("FOUT", m)
        if self.warnings:
            print(f"\nWaarschuwingen ({len(self.warnings)}):\n")
            for m in self.warnings:
                _print_message("WAARSCHUWING", m)

        print("-" * 72)
        print(f"Samenvatting: {len(self.errors)} fout(en), {len(self.warnings)} waarschuwing(en).")
        if not self.errors and not self.warnings:
            print("Alles consistent. Geen actie nodig.")


def _print_message(level: str, m: dict) -> None:
    print(f"[{level}] [{m['code']}] {m['summary']}")
    print(f"  Bestand: {m['file']}")
    print(f"  Wat is er aan de hand: {m['what']}")
    print(f"  Wat moet je doen: {m['fix']}")
    print()


def _load_manifest(report: Report) -> dict | None:
    if not MANIFEST_PATH.exists():
        report.error(
            "C1.1",
            "Het manifestbestand ontbreekt.",
            str(MANIFEST_PATH.relative_to(REPO_ROOT)),
            "Het bestand 00_register/instruction_manifest.yaml is niet aanwezig in de repo.",
            "Herstel het manifestbestand vanuit git of maak het opnieuw aan.",
        )
        return None
    try:
        with MANIFEST_PATH.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
    except yaml.YAMLError as exc:
        report.error(
            "C1.1",
            "Het manifest is geen geldige YAML.",
            str(MANIFEST_PATH.relative_to(REPO_ROOT)),
            f"De YAML-parser geeft de volgende fout: {exc}",
            "Open het bestand in een editor met YAML-ondersteuning en herstel de syntaxis (let op inspringing en dubbele punten).",
        )
        return None
    if not isinstance(data, dict) or "instruction_sets" not in data:
        report.error(
            "C1.2",
            "Het manifest mist de sleutel 'instruction_sets'.",
            str(MANIFEST_PATH.relative_to(REPO_ROOT)),
            "Op het hoogste niveau van het manifest moet een lijst 'instruction_sets:' staan.",
            "Voeg de sleutel 'instruction_sets:' toe en zet alle instructie-entries als lijstitems daaronder.",
        )
        return None
    if not isinstance(data["instruction_sets"], list):
        report.error(
            "C1.2",
            "De sleutel 'instruction_sets' is geen lijst.",
            str(MANIFEST_PATH.relative_to(REPO_ROOT)),
            "'instruction_sets' moet een lijst (YAML-array) met instructie-entries zijn.",
            "Zorg dat de items beginnen met '- ' onder 'instruction_sets:'.",
        )
        return None
    return data


def _load_register(report: Report) -> list[dict] | None:
    if not REGISTER_PATH.exists():
        report.error(
            "C4.2",
            "Het masterregister ontbreekt.",
            str(REGISTER_PATH.relative_to(REPO_ROOT)),
            "Het bestand 00_register/master_register.csv is niet aanwezig in de repo.",
            "Herstel het masterregister vanuit git of maak het opnieuw aan.",
        )
        return None
    with REGISTER_PATH.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _parse_frontmatter(text: str) -> dict | None:
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None
    if isinstance(data, dict):
        return data
    return None


def validate_manifest_entries(manifest: dict, report: Report) -> list[dict]:
    valid_entries: list[dict] = []
    seen_ids: set[str] = set()
    for index, entry in enumerate(manifest["instruction_sets"], start=1):
        location = f"{MANIFEST_PATH.relative_to(REPO_ROOT)} (entry #{index})"
        if not isinstance(entry, dict):
            report.error(
                "C1.3",
                "Een entry in het manifest is geen mapping.",
                location,
                "Elke instructie moet een mapping zijn met velden zoals 'instruction_id' en 'path'.",
                "Controleer de inspringing en zorg dat het item een YAML-mapping is.",
            )
            continue

        missing = [f for f in REQUIRED_MANIFEST_FIELDS if f not in entry]
        if missing:
            report.error(
                "C1.3",
                "Een manifest-entry mist verplichte velden.",
                location,
                f"De volgende velden ontbreken: {', '.join(missing)}.",
                "Vul de ontbrekende velden aan; zie 00_register/manifest_validation_specification.md voor details.",
            )
            continue

        iid = entry["instruction_id"]
        path = entry["path"]
        version = entry["version"]
        status = entry["status"]

        # C3.1 unique
        if iid in seen_ids:
            report.error(
                "C3.1",
                "Twee manifest-entries hebben dezelfde instruction_id.",
                location,
                f"De id '{iid}' komt meerdere keren voor in het manifest.",
                "Hernoem één van de twee entries of verwijder de dubbele entry.",
            )
        else:
            seen_ids.add(iid)

        # C3.2 / C3.3 id format
        if not ID_PATTERN.match(str(iid)):
            report.error(
                "C3.2",
                "Een instruction_id voldoet niet aan de naamgevingsconventie.",
                location,
                f"De id '{iid}' bevat ongeldige tekens of een onjuist aantal segmenten.",
                "Gebruik alleen kleine letters, cijfers en underscores; scheid prefix en naam met een punt (zie governance.instruction_id_convention).",
            )
        else:
            prefix = str(iid).split(".", 1)[0]
            if prefix not in ALLOWED_PREFIXES:
                report.error(
                    "C3.3",
                    "Een instruction_id gebruikt een onbekende prefix.",
                    location,
                    f"De prefix '{prefix}' in id '{iid}' staat niet in de toegestane lijst {sorted(ALLOWED_PREFIXES)}.",
                    "Kies een bestaande prefix of voeg de nieuwe prefix eerst toe aan governance.instruction_id_convention.",
                )
            elif prefix in PREFIX_TO_DIR and not str(path).startswith(PREFIX_TO_DIR[prefix] + "/"):
                report.warning(
                    "C3.4",
                    "De map waarin het bestand staat past niet bij de prefix.",
                    location,
                    f"De id '{iid}' heeft prefix '{prefix}' maar het pad '{path}' ligt niet in '{PREFIX_TO_DIR[prefix]}/'.",
                    "Verplaats het bestand naar de juiste map of pas de prefix aan; zie governance.instruction_id_convention.",
                )

        # C2 path checks
        if ".." in Path(path).parts or Path(path).is_absolute():
            report.error(
                "C2.2",
                "Een pad in het manifest ligt buiten de repo.",
                location,
                f"Het pad '{path}' bevat '..' of is absoluut.",
                "Gebruik een relatief pad binnen de repo, bijvoorbeeld '01_global/operating_principles.md'.",
            )
        else:
            file_path = REPO_ROOT / path
            if not file_path.exists():
                report.error(
                    "C2.1",
                    "Het manifest verwijst naar een bestand dat niet bestaat.",
                    location,
                    f"In het manifest staat een verwijzing naar '{path}', maar dat bestand is niet aanwezig in de repo.",
                    "Maak het bestand aan op dit pad, of pas het manifest aan zodat het naar het juiste pad verwijst.",
                )

        # C5 status
        if status not in ALLOWED_STATUSES:
            report.error(
                "C5.1",
                "Een manifest-entry heeft een ongeldige status.",
                location,
                f"De waarde '{status}' voor '{iid}' is geen geldige status.",
                f"Gebruik één van: {', '.join(sorted(ALLOWED_STATUSES))}.",
            )

        # C6 version
        if not SEMVER_PATTERN.match(str(version)):
            report.error(
                "C6.1",
                "Een manifest-entry heeft een ongeldige versie.",
                location,
                f"De waarde '{version}' voor '{iid}' is geen geldige semver (MAJOR.MINOR.PATCH).",
                "Gebruik drie getallen gescheiden door punten, bijvoorbeeld '1.0.0'.",
            )

        valid_entries.append(entry)

    return valid_entries


def validate_register(register_rows: list[dict], report: Report) -> dict[str, dict]:
    register_by_id: dict[str, dict] = {}
    location = str(REGISTER_PATH.relative_to(REPO_ROOT))
    for index, row in enumerate(register_rows, start=2):  # header is row 1
        iid = row.get("instruction_id", "").strip()
        row_loc = f"{location} (regel {index})"
        if not iid:
            report.error(
                "C4.2",
                "Een rij in het masterregister mist een instruction_id.",
                row_loc,
                "De kolom 'instruction_id' is leeg op deze regel.",
                "Vul de id in of verwijder de lege regel.",
            )
            continue
        if iid in register_by_id:
            report.error(
                "C3.1",
                "Twee rijen in het masterregister hebben dezelfde instruction_id.",
                row_loc,
                f"De id '{iid}' komt meerdere keren voor in master_register.csv.",
                "Verwijder de dubbele rij of geef één van de twee een eigen id.",
            )
        register_by_id[iid] = row

        status = row.get("status", "").strip()
        if status and status not in ALLOWED_STATUSES:
            report.error(
                "C5.1",
                "Een rij in het masterregister heeft een ongeldige status.",
                row_loc,
                f"De waarde '{status}' voor '{iid}' is geen geldige status.",
                f"Gebruik één van: {', '.join(sorted(ALLOWED_STATUSES))}.",
            )
        version = row.get("version", "").strip()
        if version and not SEMVER_PATTERN.match(version):
            report.error(
                "C6.1",
                "Een rij in het masterregister heeft een ongeldige versie.",
                row_loc,
                f"De waarde '{version}' voor '{iid}' is geen geldige semver.",
                "Gebruik MAJOR.MINOR.PATCH, bijvoorbeeld '1.0.0'.",
            )
    return register_by_id


def cross_check(manifest_entries: list[dict], register_by_id: dict[str, dict], report: Report) -> None:
    manifest_by_id = {e["instruction_id"]: e for e in manifest_entries}
    manifest_loc = str(MANIFEST_PATH.relative_to(REPO_ROOT))
    register_loc = str(REGISTER_PATH.relative_to(REPO_ROOT))

    for iid, entry in manifest_by_id.items():
        if iid not in register_by_id:
            report.error(
                "C4.1",
                "Een instructie staat wel in het manifest maar niet in het masterregister.",
                register_loc,
                f"De id '{iid}' ontbreekt in master_register.csv.",
                f"Voeg een rij toe in master_register.csv met id '{iid}', dezelfde versie, status, pad en eigenaar als in het manifest.",
            )
            continue
        row = register_by_id[iid]
        for field in ("version", "path", "status"):
            mv = str(entry.get(field, "")).strip()
            rv = str(row.get(field, "")).strip()
            if mv != rv:
                report.error(
                    "C4.3",
                    f"Het veld '{field}' wijkt af tussen manifest en masterregister.",
                    f"{manifest_loc} ↔ {register_loc}",
                    f"Voor '{iid}' staat in het manifest '{mv}' en in het masterregister '{rv}'.",
                    "Zorg dat manifest en masterregister exact dezelfde waarde hebben; werk beide bij in dezelfde commit.",
                )

    for iid in register_by_id:
        if iid not in manifest_by_id:
            report.error(
                "C4.2",
                "Een instructie staat wel in het masterregister maar niet in het manifest.",
                manifest_loc,
                f"De id '{iid}' ontbreekt in instruction_manifest.yaml.",
                f"Voeg een entry toe aan instruction_manifest.yaml voor '{iid}' met versie, pad, status en applies_to.",
            )


def validate_frontmatter(manifest_entries: list[dict], register_by_id: dict[str, dict], report: Report) -> set[str]:
    """Check frontmatter consistency for each manifest entry. Returns set of paths checked."""
    checked: set[str] = set()
    for entry in manifest_entries:
        path = entry.get("path")
        if not path:
            continue
        file_path = REPO_ROOT / path
        if not file_path.exists():
            continue
        checked.add(str(file_path))
        try:
            text = file_path.read_text(encoding="utf-8")
        except OSError as exc:
            report.error(
                "C2.1",
                "Een bronbestand is niet leesbaar.",
                path,
                f"Het bestand kon niet worden gelezen: {exc}.",
                "Controleer de bestandsrechten en encoding (UTF-8).",
            )
            continue

        fm = _parse_frontmatter(text)
        if fm is None:
            # No frontmatter — skip (C8.2).
            continue

        missing = [f for f in REQUIRED_FRONTMATTER_FIELDS if f not in fm]
        if missing:
            report.error(
                "C7.1",
                "De frontmatter van een bronbestand mist verplichte velden.",
                path,
                f"De volgende velden ontbreken in de frontmatter: {', '.join(missing)}.",
                "Vul de frontmatter aan met instruction_id, version, status, owner en last_reviewed.",
            )
            continue

        iid = entry["instruction_id"]
        for field in ("instruction_id", "version", "status"):
            mv = str(entry.get(field, "")).strip()
            fv = str(fm.get(field, "")).strip()
            if mv != fv:
                report.error(
                    "C7.2",
                    f"De frontmatter wijkt af van het manifest op het veld '{field}'.",
                    path,
                    f"In het manifest staat '{mv}', in de frontmatter staat '{fv}'.",
                    "Pas de frontmatter aan zodat instruction_id, version en status overeenkomen met het manifest.",
                )

        row = register_by_id.get(iid)
        if row is not None:
            for field in ("owner", "last_reviewed"):
                rv = str(row.get(field, "")).strip()
                fv = str(fm.get(field, "")).strip()
                if rv and fv and rv != fv:
                    report.warning(
                        "C7.3",
                        f"Het veld '{field}' verschilt tussen frontmatter en masterregister.",
                        path,
                        f"In het masterregister staat '{rv}', in de frontmatter staat '{fv}'.",
                        "Werk één van beide bij zodat eigenaar en review-datum gelijk zijn.",
                    )

        last_reviewed = str(fm.get("last_reviewed", "")).strip()
        if last_reviewed and not DATE_PATTERN.match(last_reviewed):
            report.warning(
                "C7.4",
                "Het veld 'last_reviewed' is geen ISO-datum.",
                path,
                f"De waarde '{last_reviewed}' lijkt geen datum in formaat JJJJ-MM-DD.",
                "Gebruik een datum als '2026-05-11'.",
            )

    return checked


def find_unregistered_files(manifest_entries: list[dict], report: Report) -> None:
    manifest_paths = {str((REPO_ROOT / e["path"]).resolve()) for e in manifest_entries if "path" in e}
    for sub in SOURCE_DIRS:
        base = REPO_ROOT / sub
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.md")):
            if str(path.resolve()) in manifest_paths:
                continue
            rel = path.relative_to(REPO_ROOT)
            try:
                text = path.read_text(encoding="utf-8")
            except OSError:
                continue
            fm = _parse_frontmatter(text)
            if fm is None:
                # C8.2 — silently ignore.
                continue
            iid = fm.get("instruction_id", "<onbekend>")
            report.warning(
                "C8.1",
                "Een bestand met frontmatter is niet opgenomen in het manifest.",
                str(rel),
                f"Het bestand heeft frontmatter met id '{iid}' maar staat niet in instruction_manifest.yaml.",
                "Voeg een entry toe aan het manifest en het masterregister, of verwijder de frontmatter als het bestand niet als instructie geldt.",
            )


def main() -> int:
    report = Report()

    manifest = _load_manifest(report)
    register_rows = _load_register(report)

    if manifest is None:
        report.print()
        return 1

    entries = validate_manifest_entries(manifest, report)

    register_by_id: dict[str, dict] = {}
    if register_rows is not None:
        register_by_id = validate_register(register_rows, report)
        cross_check(entries, register_by_id, report)

    validate_frontmatter(entries, register_by_id, report)
    find_unregistered_files(entries, report)

    report.print()
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
