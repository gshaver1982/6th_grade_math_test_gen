from __future__ import annotations

import math
import random
from dataclasses import dataclass
from fractions import Fraction
from typing import Callable, List


@dataclass
class Question:
    prompt: str
    answer: str
    work: str
    category: str


def frac_str(f: Fraction) -> str:
    if f.denominator == 1:
        return str(f.numerator)
    return f"{f.numerator}/{f.denominator}"


def simplify_fraction_text(n: int, d: int) -> str:
    return frac_str(Fraction(n, d))


def make_whole_number_operation(rng: random.Random) -> Question:
    op = rng.choice(["+", "-", "x", "/"])
    if op == "+":
        a = rng.randint(10, 500)
        b = rng.randint(10, 500)
        return Question(f"{a} + {b}", str(a + b), f"{a} + {b} = {a + b}", "whole numbers")
    if op == "-":
        a = rng.randint(50, 500)
        b = rng.randint(10, a)
        return Question(f"{a} - {b}", str(a - b), f"{a} - {b} = {a - b}", "whole numbers")
    if op == "x":
        a = rng.randint(2, 20)
        b = rng.randint(2, 20)
        return Question(f"{a} x {b}", str(a * b), f"{a} x {b} = {a * b}", "whole numbers")
    b = rng.randint(2, 12)
    a = b * rng.randint(2, 15)
    return Question(f"{a} / {b}", str(a // b), f"{a} / {b} = {a // b}", "whole numbers")


def make_fraction_operation(rng: random.Random) -> Question:
    kind = rng.choice(["add", "sub", "mul", "div"])
    denoms = [2, 3, 4, 5, 6, 8, 10, 12]

    if kind in {"add", "sub"}:
        denom = rng.choice(denoms)
        a = rng.randint(1, denom - 1)
        b = rng.randint(1, denom - 1)
        f1 = Fraction(a, denom)
        f2 = Fraction(b, denom)
        if kind == "sub" and f2 > f1:
            f1, f2 = f2, f1
        ans = f1 + f2 if kind == "add" else f1 - f2
        op = "+" if kind == "add" else "-"
        return Question(f"{frac_str(f1)} {op} {frac_str(f2)}", frac_str(ans), f"{frac_str(f1)} {op} {frac_str(f2)} = {frac_str(ans)}", "fractions")

    if kind == "mul":
        f1 = Fraction(rng.randint(1, 9), rng.choice(denoms))
        f2 = Fraction(rng.randint(1, 9), rng.choice(denoms))
        ans = f1 * f2
        return Question(f"{frac_str(f1)} x {frac_str(f2)}", frac_str(ans), f"{frac_str(f1)} x {frac_str(f2)} = {frac_str(ans)}", "fractions")

    f1 = Fraction(rng.randint(1, 9), rng.choice(denoms))
    f2 = Fraction(rng.randint(1, 9), rng.choice(denoms))
    ans = f1 / f2
    return Question(f"{frac_str(f1)} / {frac_str(f2)}", frac_str(ans), f"{frac_str(f1)} / {frac_str(f2)} = {frac_str(ans)}", "fractions")


def make_decimal_operation(rng: random.Random) -> Question:
    kind = rng.choice(["add", "sub", "mul"])
    a = round(rng.uniform(1, 50), 2)
    b = round(rng.uniform(1, 50), 2)
    if kind == "add":
        ans = round(a + b, 2)
        return Question(f"{a:.2f} + {b:.2f}", f"{ans:.2f}", f"{a:.2f} + {b:.2f} = {ans:.2f}", "decimals")
    if kind == "sub":
        if b > a:
            a, b = b, a
        ans = round(a - b, 2)
        return Question(f"{a:.2f} - {b:.2f}", f"{ans:.2f}", f"{a:.2f} - {b:.2f} = {ans:.2f}", "decimals")
    ans = round(a * b, 2)
    return Question(f"{a:.2f} x {b:.2f}", f"{ans:.2f}", f"{a:.2f} x {b:.2f} = {ans:.2f}", "decimals")


def make_percent_ratio_problem(rng: random.Random) -> Question:
    kind = rng.choice(["percent_of", "convert", "ratio"])
    if kind == "percent_of":
        percent = rng.choice([10, 15, 20, 25, 30, 40, 50, 60, 75])
        number = rng.randint(20, 200)
        ans = number * percent / 100
        ans_text = str(int(ans)) if float(ans).is_integer() else f"{ans:.2f}"
        return Question(f"What is {percent}% of {number}?", ans_text, f"{percent}% of {number} = {ans_text}", "percent and ratio")
    if kind == "convert":
        frac_options = [(Fraction(1, 2), "50%"), (Fraction(1, 4), "25%"), (Fraction(3, 4), "75%"), (Fraction(1, 5), "20%"), (Fraction(2, 5), "40%"), (Fraction(1, 10), "10%")] 
        frac, pct = rng.choice(frac_options)
        if rng.choice([True, False]):
            return Question(f"Write {pct} as a fraction in simplest form.", frac_str(frac), f"{pct} = {frac_str(frac)}", "percent and ratio")
        return Question(f"Write {frac_str(frac)} as a percent.", pct, f"{frac_str(frac)} = {pct}", "percent and ratio")
    a = rng.randint(1, 9)
    b = rng.randint(1, 9)
    return Question(f"Write the ratio {a}:{b} in simplest form.", f"{a}:{b}", f"{a}:{b} is already in simplest form if gcd({a},{b}) = 1", "percent and ratio")


def make_order_of_operations(rng: random.Random) -> Question:
    a = rng.randint(2, 12)
    b = rng.randint(2, 12)
    c = rng.randint(2, 12)
    d = rng.randint(2, 12)
    template = rng.choice([
        f"{a} + {b} x {c}",
        f"({a} + {b}) x {c}",
        f"{a} x {b} - {c}",
        f"{a} + {b} x {c} - {d}",
        f"({a} + {b}) x ({c} - {d})",
    ])
    ans = eval(template.replace("x", "*"))
    return Question(template, str(ans), f"{template} = {ans}", "order and algebra")


def make_one_step_equation(rng: random.Random) -> Question:
    kind = rng.choice(["add", "sub", "mul", "div"])
    x = rng.randint(2, 20)
    if kind == "add":
        c = rng.randint(1, 30)
        value = x + c
        return Question(f"x + {c} = {value}", str(x), f"x = {value} - {c} = {x}", "order and algebra")
    if kind == "sub":
        c = rng.randint(1, 30)
        value = x - c
        return Question(f"x - {c} = {value}", str(x), f"x = {value} + {c} = {x}", "order and algebra")
    if kind == "mul":
        c = rng.randint(2, 12)
        value = x * c
        return Question(f"{c}x = {value}", str(x), f"x = {value} / {c} = {x}", "order and algebra")
    c = rng.randint(2, 12)
    value = x * c
    return Question(f"x / {c} = {x}", str(value), f"x = {x} x {c} = {value}", "order and algebra")


def make_geometry_problem(rng: random.Random) -> Question:
    kind = rng.choice(["perimeter", "area", "volume"])
    if kind == "perimeter":
        l = rng.randint(4, 20)
        w = rng.randint(4, 20)
        ans = 2 * (l + w)
        return Question(f"A rectangle has length {l} cm and width {w} cm. What is its perimeter?", f"{ans} cm", f"Perimeter = 2({l} + {w}) = {ans} cm", "geometry")
    if kind == "area":
        side = rng.randint(3, 15)
        ans = side * side
        return Question(f"A square has side length {side} cm. What is its area?", f"{ans} cm^2", f"Area = {side} x {side} = {ans} cm^2", "geometry")
    l = rng.randint(2, 8)
    w = rng.randint(2, 8)
    h = rng.randint(2, 8)
    ans = l * w * h
    return Question(f"A box has length {l} cm, width {w} cm, and height {h} cm. What is its volume?", f"{ans} cm^3", f"Volume = {l} x {w} x {h} = {ans} cm^3", "geometry")


def make_data_question(rng: random.Random) -> Question:
    values = [rng.randint(1, 10) for _ in range(5)]
    kind = rng.choice(["mean", "median", "range"])
    if kind == "mean":
        avg = sum(values) / len(values)
        ans = f"{avg:.1f}" if not avg.is_integer() else str(int(avg))
        return Question(f"Find the mean of these numbers: {', '.join(map(str, values))}.", ans, f"Mean = {sum(values)} / {len(values)} = {ans}", "data")
    if kind == "median":
        med = sorted(values)[len(values) // 2]
        return Question(f"Find the median of these numbers: {', '.join(map(str, values))}.", str(med), f"Sorted: {sorted(values)}; median = {med}", "data")
    r = max(values) - min(values)
    return Question(f"Find the range of these numbers: {', '.join(map(str, values))}.", str(r), f"Range = {max(values)} - {min(values)} = {r}", "data")


def make_word_problem(rng: random.Random) -> Question:
    kind = rng.choice(["money", "rate", "multi_step", "fraction_word", "percent_word"])

    if kind == "money":
        price = rng.randint(3, 25)
        qty = rng.randint(2, 8)
        total = price * qty
        return Question(
            f"Each notebook costs ${price}. How much do {qty} notebooks cost?",
            f"${total}",
            f"{qty} x ${price} = ${total}",
            "word problems",
        )

    if kind == "rate":
        miles = rng.randint(2, 15)
        days = rng.randint(2, 6)
        total = miles * days
        return Question(
            f"Jordan walks {miles} miles each day. How many miles in {days} days?",
            f"{total} miles",
            f"{miles} x {days} = {total} miles",
            "word problems",
        )

    if kind == "fraction_word":
        a = rng.randint(1, 7)
        b = rng.randint(1, 7)
        c = rng.choice([2, 3, 4, 5, 6, 8, 10, 12])
        d = rng.choice([2, 3, 4, 5, 6, 8, 10, 12])
        f1 = Fraction(a, c)
        f2 = Fraction(b, d)
        total = f1 + f2
        prompt = (
            f"A recipe uses {frac_str(f1)} cup of sugar and "
            f"{frac_str(f2)} cup more. How much sugar in all?"
        )
        return Question(
            prompt,
            frac_str(total),
            f"{frac_str(f1)} + {frac_str(f2)} = {frac_str(total)}",
            "word problems",
        )

    if kind == "percent_word":
        percent = rng.choice([10, 15, 20, 25, 30, 40, 50, 60, 75])
        price = rng.randint(20, 200)
        discount = price * percent / 100
        discount_text = str(int(discount)) if float(discount).is_integer() else f"{discount:.2f}"

        return Question(
            f"A jacket costs ${price} and is {percent}% off. What is the discount?",
            f"${discount_text}",
            f"{percent}% of ${price} = ${discount_text}",
            "word problems",
        )

    start = rng.randint(20, 100)
    spend = rng.randint(5, start - 5)
    add = rng.randint(5, 50)
    total = start - spend + add
    return Question(
        f"Elena had {start} stickers. She gave away {spend} stickers and then got {add} more. How many stickers now?",
        str(total),
        f"{start} - {spend} + {add} = {total}",
        "word problems",
    )

def build_question_set(
    num_questions: int = 25,
    seed: int | None = None,
    difficulty: str = "medium",
) -> List[Question]:
    rng = random.Random(seed)

    category_to_generators = {
        "whole numbers": [make_whole_number_operation],
        "fractions": [make_fraction_operation],
        "decimals": [make_decimal_operation],
        "percent and ratio": [make_percent_ratio_problem],
        "order and algebra": [make_order_of_operations, make_one_step_equation],
        "geometry": [make_geometry_problem],
        "data": [make_data_question],
        "word problems": [make_word_problem],
    }

    # Weighted category pool so the mix stays roughly balanced.
    category_pool = [
        "whole numbers", "whole numbers",
        "fractions", "fractions",
        "decimals",
        "percent and ratio",
        "order and algebra", "order and algebra",
        "geometry",
        "data",
        "word problems", "word problems",
    ]

    questions: List[Question] = []
    while len(questions) < num_questions:
        cat = rng.choice(category_pool)
        gen = rng.choice(category_to_generators[cat])
        q = gen(rng)
        q.category = cat
        questions.append(q)

    rng.shuffle(questions)
    return questions[:num_questions]
