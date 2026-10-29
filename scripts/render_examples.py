#!/usr/bin/env python3
"""Render saved fictional cases. No model, network, ranking engine or live MCP calls."""

import argparse
import csv
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DISCLOSURE = "> Fictional worked example. All events, companies, people, metrics and assessments below are synthetic fixtures, not live Lensmor results.\n"


def cell(value):
    if value is None or value == "":
        return "Not available"
    return str(value).replace("\r", " ").replace("\n", " ").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("|", "\\|")


def table(headers, rows):
    return "\n".join(["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |", *["| " + " | ".join(cell(value) for value in row) + " |" for row in rows]]) + "\n"


def csv_content(headers, rows):
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\r\n")
    writer.writerow(headers)
    for row in rows:
        safe = []
        for value in row:
            text = "" if value is None else str(value)
            if text.lstrip(" \t\r\n").startswith(("=", "+", "-", "@")) or text.startswith(("\t", "\r")):
                text = "'" + text
            safe.append(text)
        writer.writerow(safe)
    return "\ufeff" + output.getvalue()


def check_fixture(data):
    if data.get("data_mode") != "synthetic" or data.get("live_data") is not False:
        raise ValueError("Examples must be explicitly fictional and offline.")


def percent(metric):
    if not metric or metric.get("status") != "available":
        return "Not available"
    numerator, denominator = metric["numerator"], metric["denominator"]
    if type(numerator) is not int or type(denominator) is not int or denominator <= 0 or not 0 <= numerator <= denominator:
        raise ValueError("Invalid saved audience metric.")
    return f"{100 * numerator / denominator:.1f}% ({numerator}/{denominator} profiles; unknowns stay in the denominator)"


def render_events(data):
    check_fixture(data)
    rows = [[event["name"], event["dates"], event["location"], event["evidence"], percent(event.get("director_plus")), event["assessment"]] for event in data["events"]]
    return "# Worked example 1: choose an event\n\n" + DISCLOSURE + "\n" + data["request"] + "\n\n" + table(["Event", "Dates", "Location", "Supplied evidence", "Director+ sample metric", "Saved illustrative assessment"], rows) + "\nAssessment source: a saved example of model judgment, not the REST API's 0–10 fit score. This is a two-event candidate comparison, not an exhaustive market search. Missing metrics remain unknown. Confirm real editions and sources before making plans.\n"


COMPANY_HEADERS = ["Company Name", "Company URL", "Industry", "Company HQ", "Employee Size", "Company LinkedIn URL", "Match evidence"]
PERSON_HEADERS = ["Name", "Job Title", "Company Name", "Management Level", "LinkedIn URL", "Role evidence"]


def selection(data):
    check_fixture(data)
    limit = data["requested_limit"]
    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
        raise ValueError("Invalid requested result limit.")
    all_companies = data["companies"]
    if any(company["qualification"] not in {"MATCH", "UNKNOWN", "NO_MATCH"} for company in all_companies):
        raise ValueError("Unrecognized company qualification state.")
    if len({company["id"] for company in all_companies}) != len(all_companies):
        raise ValueError("Duplicate company identifiers in fixture.")
    companies = [company for company in all_companies if company["qualification"] == "MATCH"][:limit]
    companies_by_id = {company["id"]: company for company in companies}
    all_ids = {company["id"] for company in all_companies}
    if any(person["company_id"] not in all_ids or person["role_status"] not in {"MATCH", "UNKNOWN", "NO_MATCH"} for person in data["contacts"]):
        raise ValueError("Invalid contact company or role state.")
    people = [person for person in data["contacts"] if person["company_id"] in companies_by_id and person["role_status"] == "MATCH"][:limit]
    if len({person["id"] for person in data["contacts"]}) != len(data["contacts"]):
        raise ValueError("Duplicate contact identifiers in fixture.")
    return companies, people, companies_by_id


def render_prospects(data):
    companies, people, indexed = selection(data)
    company_rows = [[company.get(field) for field in ("name", "website", "industry", "hq", "employee_size", "linkedin_url", "evidence")] for company in companies]
    person_rows = [[person["name"], person["title"], indexed[person["company_id"]]["name"], person.get("management_level"), person.get("linkedin_url"), person["evidence"]] for person in people]
    unknown = sum(company["qualification"] == "UNKNOWN" for company in data["companies"])
    excluded = sum(company["qualification"] == "NO_MATCH" for company in data["companies"])
    report = "# Worked example 2: build a researched shortlist\n\n" + DISCLOSURE + "\n" + data["request"] + "\n\n## Companies\n\n" + table(COMPANY_HEADERS, company_rows)
    report += "\n## Related contacts\n\n" + table(PERSON_HEADERS, person_rows)
    report += f"\nRequested up to {data['requested_limit']}; delivered {len(companies)} qualified companies and {len(people)} role-matching contacts. {unknown} company candidate remains unverified; {excluded} was excluded.\n"
    report += "\nThe saved fixture order illustrates a selected shortlist, not a backend recommendation score. Company records and role relevance do not establish registered attendance, purchasing authority or purchase intent. Email and phone have not been checked or unlocked. No purchase or outreach occurred.\n"
    report += "\nThe accompanying accounts.csv and contacts.csv contain exactly these displayed rows in the same order. They are shortlist exports, not full-directory exports.\n"
    return {"output.md": report, "accounts.csv": csv_content(COMPANY_HEADERS, company_rows), "contacts.csv": csv_content(PERSON_HEADERS, person_rows)}


def render_drafts(data, prospects):
    check_fixture(data)
    _, people, companies = selection(prospects)
    available = {person["id"]: person for person in people}
    chosen = data["selected_contact_ids"]
    if len(chosen) != len(set(chosen)) or set(chosen) != set(data["drafts"]):
        raise ValueError("Saved drafts must exactly match the explicitly selected contacts.")
    if set(chosen) - set(available):
        raise ValueError("A draft recipient is outside the final qualified shortlist.")
    result = "# Worked example 3: prepare outreach drafts\n\n" + DISCLOSURE + "\n" + data["request"] + "\n\nSender facts supplied in this fictional brief: " + data["sender_facts"] + "\n\nStatus: drafts only. No email or LinkedIn message was sent; no meeting was booked; no contact field was purchased.\n"
    for index, person_id in enumerate(chosen, 1):
        person = available[person_id]
        draft = data["drafts"][person_id]
        company = companies[person["company_id"]]
        result += f"\n## {index}. {cell(person['name'])} — {cell(company['name'])}\n\n"
        result += "Personalization basis: " + person["evidence"] + " " + company["evidence"] + "\n\n"
        result += "Subject: " + draft["subject"] + "\n\n" + draft["body"] + "\n"
    result += "\nEvidence gaps: actual attendance, meeting availability, booth location and email/phone availability are unknown. The saved copy deliberately does not claim any of those facts. These are illustrative drafts, not an email-delivery integration.\n"
    return result


def render_all(root=ROOT):
    base = Path(root) / "examples"
    ids = ["01-choose-events", "02-build-shortlist", "03-prepare-outreach"]
    data = [json.loads((base / name / "input.json").read_text(encoding="utf-8")) for name in ids]
    outputs = {f"{ids[0]}/output.md": render_events(data[0]), f"{ids[2]}/output.md": render_drafts(data[2], data[1])}
    outputs.update({f"{ids[1]}/{name}": content for name, content in render_prospects(data[1]).items()})
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        outputs = render_all()
        for name, text in outputs.items():
            path = ROOT / "examples" / name
            encoded = text.encode("utf-8")
            if args.check:
                if not path.exists() or path.read_bytes() != encoded:
                    raise ValueError(f"Saved output differs: {name}")
            else:
                path.write_bytes(encoded)
    except (ValueError, KeyError, OSError) as exc:
        parser.exit(1, f"Example rendering failed: {exc}\n")
    print(f"{'Checked' if args.check else 'Rendered'} {len(outputs)} offline sample artifacts. No API or model calls.")


if __name__ == "__main__":
    main()
