import argparse
import sys
import json
from json import JSONDecodeError

import requests
from pydantic import BaseSettings, Field, validator
from typing import Optional

from sqlalchemy.sql.coercions import expect

from config.core import settings


class CLISettings(BaseSettings):
    host: str = Field("http://localhost:8000")
    repeat: int = Field(1)
    input: str = Field("-")
    json_input: Optional[str] = Field(None)
    input: str = Field("-")

    @validator("repeat")
    def validate_repeat(cls, v):
        if v < 1:
            raise ValueError("repeat must be >= 1")
        return v


def parse_arg():
    parser =argparse.ArgumentParser(prog="cache-cli")
    parser.add_argument("-H", "--host", help="service host URL", default=None)
    parser.add_argument("-r", "--repeat", help="number of iterations", type=int, default=None)
    parser.add_argument("-i", "--input", help='input file path or "-" for stdin', default=None)
    parser.add_argument("-j", "--json", dest="json_input", help="input JSON string", default=None)
    parser.add_argument("-o", "--output", help='output file path or "-" for stdout', default=None)
    return parser.parse_args()


def parse_args() -> CLISettings:
    args = parse_arg()

    settings_values = {}
    if args.host is not None:
        settings_values["host"] = args.host
    if args.repeat is not None:
        settings_values["repeat"] = args.repeat
    if args.input is not None:
        settings_values["input"] = args.input
    if args.json_input is not None:
        settings_values["json_input"] = args.json_input
    if args.output is not None:
        settings_values["output"] = args.output

    return CLISettings(**settings_values)


def load_payload_from_input(settings: CLISettings) -> dict:
    if settings.json_input:
        try:
            return json.loads(settings.json_input)
        except json.JSONDecodeError:
            print("Invalid JSON passed to --json", file=sys.stderr)
            sys.exit(2)

    if settings.input == "-" or settings.input is None:
        data = sys.stdin.read()
        if not data.strip():
            print("no input provided (stdin is empty)", file=sys.stderr)
            sys.exit(2)
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            print("Invalid JSON from stdin", file=sys.stderr)
            sys.exit(2)

    try:
        with open(settings.input, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {settings.input}", file=sys.stderr)
        sys.exit(2)
    except JSONDecodeError:
        print(f"Invalid JSON in file: {settings.input}", file=sys.stderr)
        sys.exit(2)


def main():
    settings = parse_args()
    payload = load_payload_from_input(settings)

    url = settings.host.rstrip("/") + "/payload"
    results = []

    for _ in range(settings.repeat):
        r = requests.post(url, json=payload)
        r.raise_for_status()
        res = r.json()

        pid = res.get("id")
        g = requests.get(f"{settings.host.rstrip('/')}/payload/{pid}")
        g.raise_for_status()

        out = g.json()
        results.append({
            "id": pid,
            "output": out.get("output"),
            "reused": res.get("reused", False),
        })

        out_text = json.dumps(results, indent=2, ensure_ascii=False)
        if not settings.output or settings.output == "-":
            print(out_text)
        else:
            with open(settings.output, "w", encoding="utf-8") as f:
                f.write(out_text)
