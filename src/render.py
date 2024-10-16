#!/usr/bin/env python3
import argparse
from pathlib import Path

import markdown_strings
import tomllib
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from hebrew_numbers import verbal_number


def ins(s: str):
    return f"[{markdown_strings.esc_format(s, esc=True)}]{{.underline}}"


def esc(s: str):
    return markdown_strings.esc_format(s, esc=True)


def verbal_male(i: int):
    i = int(i)
    return verbal_number(i, male=True)


def verbal_female(i: int):
    i = int(i)
    return verbal_number(i, male=False)


def date(d):
    if d == "_":
        return r"\_\_\_\_.\_\_\_\_.\_\_\_\_\_\_\_\_"
    return f"{d.day}.{d.month}.{d.year}"


def day(d):
    if d == "_":
        return r"\_\_\_\_"
    return d.day


def month_name(d):
    if d == "_":
        return r"\_\_\_\_"
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
        return r"\_\_\_\_\_\_\_\_"
    return d.year


class RenderError(Exception):
    pass


def raise_helper(message: str):
    raise RenderError(message)


def render_template(input_fn, template_fn):
    env = Environment(
        loader=FileSystemLoader(template_fn.parent), undefined=StrictUndefined
    )
    env.filters["ins"] = ins
    env.filters["esc"] = esc
    env.filters["verbal_male"] = verbal_male
    env.filters["verbal_female"] = verbal_female
    env.filters["date"] = date
    env.filters["month_name"] = month_name
    env.filters["day"] = day
    env.filters["year"] = year
    env.globals["raise"] = raise_helper

    context = get_user_input(input_fn)
    template = env.get_template(template_fn.name)
    output = template.render(context)
    return output


def get_user_input(input_fn):
    return tomllib.loads(input_fn.read_text())


def convert_template(input_fn, template_fn, output_fn):
    output = render_template(input_fn, template_fn)
    output_fn.write_text(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="insert toml to template")
    parser.add_argument(
        "-i", "--input_fn", type=Path, default=Path("output/context.toml")
    )
    parser.add_argument(
        "-t", "--template", type=Path, default=Path("lease-agreement-text/lease.md")
    )
    parser.add_argument("-o", "--output_fn", type=Path, default=Path("output/lease.md"))
    args = parser.parse_args()
    convert_template(args.input_fn, args.template, args.output_fn)
