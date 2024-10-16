#!/usr/bin/env python3

import argparse
import datetime
import tomllib
from pathlib import Path
from typing import Any

from dateutil.relativedelta import relativedelta


def parse_amount(s: str | int, ils_per_month: int) -> int:
    if isinstance(s, str) and s.startswith("<months> "):
        months = int(s.removeprefix("<months> "))
        return months * ils_per_month
    return int(s)


def parse_date(
    s: str | datetime.date, special_date: dict[str, datetime.date | None] | None = None
) -> datetime.date or None:
    special_date = special_date or {}
    if isinstance(s, datetime.date):
        return s
    if not isinstance(s, str):
        raise TypeError(f"Unknown date type: {s}")
    for name in special_date:
        if s == f"<{name}>":
            return special_date[name]
    if s == "<today>":
        return datetime.date.today()
    if s.startswith("<today_plus> "):
        n = int(s.removeprefix("<today_plus> "))
        return datetime.date.today() + relativedelta(days=n)
    if s == "<blank_date>":
        return None
    return datetime.date.fromisoformat(s)


def none_to_str(d: datetime.date | None) -> datetime.date | str:
    if d is None:
        return "_"
    if not isinstance(d, datetime.date):
        raise ValueError("unsupported type for date")
    return d


def add_to_date(date: datetime.date | None, delta: relativedelta):
    if date is None:
        return date
    if isinstance(date, datetime.date):
        return date + delta
    raise ValueError("unsupported value for date")


def parse_payment_day(s: str, start_date: datetime.date | None) -> str:
    if isinstance(s, int):
        return str(s)
    if s == "<start_date|day>":
        if not isinstance(start_date, datetime.date):
            return "____"
        return str(start_date.day)
    if s == "<blank_digit>":
        return "____"
    raise ValueError("can't parse payment_day")


def get_item(d: dict, k: str) -> Any:
    try:
        item = d
        for k_part in k.split("."):
            item = item[k_part]
    except KeyError as e:
        raise KeyError(f"{k}:{k_part}") from e
    return item


def get_context_from_toml(filename: Path):
    # load data
    with filename.open("rb") as f:
        toml_data = tomllib.load(f)

    # parse special values
    if (
        toml_data["assurance"]["promissory"]["form"]["sign_location"]
        == "<sign_location>"
    ):
        toml_data["assurance"]["promissory"]["form"]["sign_location"] = toml_data[
            "sign"
        ]["location"]

    toml_data["assurance"]["bank_guarantee"]["amount"] = parse_amount(
        toml_data["assurance"]["bank_guarantee"]["amount"],
        toml_data["payment"]["ils_per_month"],
    )
    toml_data["assurance"]["promissory"]["form"]["amount"] = parse_amount(
        toml_data["assurance"]["promissory"]["form"]["amount"],
        toml_data["payment"]["ils_per_month"],
    )

    sign_date = parse_date(toml_data["sign"]["date"])
    toml_data["sign"]["date"] = none_to_str(sign_date)

    protocol_date = parse_date(
        toml_data["sign"]["protocol_date"], {"sign_date": sign_date}
    )
    toml_data["sign"]["protocol_date"] = none_to_str(protocol_date)

    start_date = parse_date(toml_data["period"]["start_date"], {"sign_date": sign_date})
    toml_data["period"]["start_date"] = none_to_str(start_date)

    from_start_date = add_to_date(
        start_date, relativedelta(months=toml_data["period"]["n_months"], days=-1)
    )
    end_date = parse_date(
        toml_data["period"]["end_date"], {"from_start_date": from_start_date}
    )
    toml_data["period"]["end_date"] = none_to_str(end_date)

    toml_data["assurance"]["promissory"]["guarantee"]["date"] = none_to_str(
        parse_date(toml_data["assurance"]["promissory"]["guarantee"]["date"])
    )
    toml_data["assurance"]["promissory"]["form"]["date"] = none_to_str(
        parse_date(
            toml_data["assurance"]["promissory"]["form"]["date"],
            {"sign_date": sign_date},
        )
    )

    toml_data["payment"]["day"] = parse_payment_day(
        toml_data["payment"]["day"], start_date
    )

    # validate values
    keys_with_options = {
        "contract.version": ["2016", "2023"],
        "payment.mode": ["bank-transfer", "checks"],
        "assurance.mode": ["promissory", "bank-guarantee"],
    }
    for k, v in keys_with_options.items():
        if get_item(toml_data, k) not in v:
            raise TypeError(f"value of {k} not in {v}")

    keys_boolean = ["contract.require_insurance", "contract.require_tenants_insurance"]
    for k in keys_boolean:
        if not isinstance(get_item(toml_data, k), bool):
            raise TypeError(f"value of {k} is not boolean")

    keys_int = [
        "period.n_months",
        "payment.ils_per_month",
        "extend_option.n_months",
        "extend_option.max_raise_percent",
        "assurance.bank_guarantee.amount",
        "assurance.promissory.form.amount",
    ]
    for k in keys_int:
        if not isinstance(get_item(toml_data, k), int):
            raise TypeError(f"value of {k} is not integer")

    keys_date = [
        "sign.date",
        "sign.protocol_date",
        "period.start_date",
        "period.end_date",
        "assurance.promissory.guarantee.date",
        "assurance.promissory.form.date",
    ]
    for k in keys_date:
        v = get_item(toml_data, k)
        if not (isinstance(v, (datetime.date, str))):
            raise TypeError(f"value of {k} is not date")
    # return
    return toml_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="convert an input toml file to a context"
    )
    parser.add_argument(
        "-i", "--input_fn", type=Path, default=Path("input_files/default.toml")
    )
    args = parser.parse_args()
    print(get_context_from_toml(filename=args.input_fn))
