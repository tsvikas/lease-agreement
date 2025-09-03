#!/usr/bin/env python3
import argparse
from pathlib import Path

import markdown_strings
from hebrew_numbers import count_prefix
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from parse_toml import get_context_from_toml


def ins(s: str):
    return f"[{markdown_strings.esc_format(s, esc=True)}]{{.underline}}"


def esc(s: str):
    return markdown_strings.esc_format(s, esc=True)


def safe_hebrew_number(value, gender):
    """Safely convert number to Hebrew with fallback for non-integer values."""
    try:
        num = int(value)
        return count_prefix(num, gender)
    except (TypeError, ValueError, AttributeError, Exception):
        return "_" * 20


def date(d):
    if d == "_":
        return r"____.____.________"
    return f"{d.day}.{d.month}.{d.year}"


def day(d):
    if d == "_":
        return r"____"
    return d.day


def month_name(d):
    if d == "_":
        return r"____"
    return {
        1: "ינואר",
        2: "פברואר",
        3: "מרץ",
        4: "אפריל",
        5: "מאי",
        6: "יוני",
        7: "יולי",
        8: "אוגוסט",
        9: "ספטמבר",
        10: "אוקטובר",
        11: "נובמבר",
        12: "דצמבר",
    }[d.month]


def year(d):
    if d == "_":
        return r"________"
    return d.year


class RenderError(Exception):
    pass


def raise_helper(message: str):
    raise RenderError(message)


def render_template(input_fn, template_fn, no_underline, simple):
    env = Environment(
        loader=FileSystemLoader(template_fn.parent), undefined=StrictUndefined
    )
    env.filters["ins"] = esc if no_underline else ins
    env.filters["esc"] = esc
    env.filters["date"] = date
    env.filters["month_name"] = month_name
    env.filters["day"] = day
    env.filters["year"] = year
    env.globals["raise"] = raise_helper
    env.filters["hebrew_count"] = safe_hebrew_number

    context = get_context_from_toml(input_fn)
    template = env.get_template(template_fn.name)
    output = template.render(context)
    if simple:
        lines = output.splitlines()
        output = "\n".join(line for line in lines if not line.startswith(":::"))
        if output[0] == "%":
            output = "#" + output[1:]
    return output


def convert_template(input_fn, template_fn, output_fn, no_underline, simple):
    output = render_template(input_fn, template_fn, no_underline, simple)
    output_fn.write_text(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="insert toml to template")
    parser.add_argument(
        "-i", "--input_fn", type=Path, default=Path("input_files/default.toml")
    )
    parser.add_argument(
        "-t",
        "--template",
        type=Path,
        default=Path("lease-agreement-text/lease.md.jinja"),
    )
    parser.add_argument("-o", "--output_fn", type=Path, default=Path("output/lease.md"))
    parser.add_argument("-U", "--no_underline", action="store_true")
    parser.add_argument("--simple", action="store_true")
    args = parser.parse_args()
    convert_template(
        args.input_fn, args.template, args.output_fn, args.no_underline, args.simple
    )
    reference = Path("templates/template.odt")
    print(
        f"use `pandoc {args.output_fn} -o {args.output_fn.with_suffix('.odt')} --reference-doc {reference}` to convert the file to ODT format"
    )
