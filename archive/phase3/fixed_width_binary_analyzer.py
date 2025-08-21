# -*- coding: utf-8 -*-
"""
Wow! Signal — Fixed‑Width Binary Analyzer (Variable Bit Width)
-------------------------------------------------------------
Purpose
  • Parse a binary string using a fixed symbol width (e.g., 5 bits), map values to atomic numbers (1–118),
    detect plausible chemical motifs (e.g., H→He, H2→He, H2O, CH4, CO2, NH3, NaCl),
    and produce a timeline plus summary statistics.

Key features
  • Variable bit width: try any n_bits (default 5) and offsets (0..n_bits-1).
  • Scores each (n_bits, offset) parse by % of tokens mapping to real elements (Z in 1..118).
  • Exports a CSV timeline of tokens, mapped elements, and detected reaction motifs.
  • Clean separation of concerns: parsing → mapping → reaction detection → reporting.

Usage (as script)
  • Configure BINARY_STRING below (or load from file/env).
  • Run directly: `python WowSignal_FixedWidth_Binary_Analyzer.py`
  • Adjust N_BITS_DEFAULT to start with 5 (as requested). You can sweep with N_BITS_SWEEP.

Dependencies
  • Python 3.9+
  • pandas (optional; required to export CSV)

Note
  • This performs *fixed‑width* decoding. It avoids the artifact of scanning all substrings of all lengths.
  • Finding meaningful chemistry still requires a *real codebook/delimiters*; until then, this is exploratory.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
from collections import Counter
import itertools
import math

try:
    import pandas as pd  # type: ignore
except Exception:  # pragma: no cover
    pd = None

# ---------------------- CONFIG ----------------------
BINARY_STRING = (
    "1100111111100111100011101111011111000111001001100010110000011000011101011100110110001110000001110010011011100100001001101001101111111111111100000001100010110000011001101110000011100010101111110011010110010111101110100010101100100000110111110111000111000001011100100111111110110111100101110011101111111111"
)

N_BITS_DEFAULT = 5  # requested starting point
N_BITS_SWEEP = [7]  # tweak to [4,5,6,7] to experiment
IGNORE_PARTIAL_TAIL = True  # if True, ignore leftover bits at end that don't fit width
CSV_OUTPUT_PATH = "binary_fixedwidth_timeline.csv"

# ---------------------- PERIODIC TABLE ----------------------
# Atomic numbers 1..118 → element symbols
ELEMENTS: Dict[int, str] = {
    1:"H",2:"He",3:"Li",4:"Be",5:"B",6:"C",7:"N",8:"O",9:"F",10:"Ne",
    11:"Na",12:"Mg",13:"Al",14:"Si",15:"P",16:"S",17:"Cl",18:"Ar",19:"K",20:"Ca",
    21:"Sc",22:"Ti",23:"V",24:"Cr",25:"Mn",26:"Fe",27:"Co",28:"Ni",29:"Cu",30:"Zn",
    31:"Ga",32:"Ge",33:"As",34:"Se",35:"Br",36:"Kr",37:"Rb",38:"Sr",39:"Y",40:"Zr",
    41:"Nb",42:"Mo",43:"Tc",44:"Ru",45:"Rh",46:"Pd",47:"Ag",48:"Cd",49:"In",50:"Sn",
    51:"Sb",52:"Te",53:"I",54:"Xe",55:"Cs",56:"Ba",57:"La",58:"Ce",59:"Pr",60:"Nd",
    61:"Pm",62:"Sm",63:"Eu",64:"Gd",65:"Tb",66:"Dy",67:"Ho",68:"Er",69:"Tm",70:"Yb",
    71:"Lu",72:"Hf",73:"Ta",74:"W",75:"Re",76:"Os",77:"Ir",78:"Pt",79:"Au",80:"Hg",
    81:"Tl",82:"Pb",83:"Bi",84:"Po",85:"At",86:"Rn",87:"Fr",88:"Ra",89:"Ac",90:"Th",
    91:"Pa",92:"U",93:"Np",94:"Pu",95:"Am",96:"Cm",97:"Bk",98:"Cf",99:"Es",100:"Fm",
    101:"Md",102:"No",103:"Lr",104:"Rf",105:"Db",106:"Sg",107:"Bh",108:"Hs",109:"Mt",110:"Ds",
    111:"Rg",112:"Cn",113:"Nh",114:"Fl",115:"Mc",116:"Lv",117:"Ts",118:"Og",
}

# ---------------------- DATA TYPES ----------------------
@dataclass
class Token:
    idx: int            # token index in sequence (not bit index)
    bit_start: int      # start bit position
    bit_end: int        # end bit position (exclusive)
    bits: str           # the raw bits for this token
    value: int          # integer value of bits
    element: Optional[str]  # element symbol if 1..118 else None

# ---------------------- CORE FUNCTIONS ----------------------
def parse_fixed_width(bits: str, width: int, offset: int = 0, ignore_tail: bool = True) -> List[Token]:
    """Parse bits into fixed-width tokens with a starting bit offset.
    Leftover tail is ignored if ignore_tail else padded with zeros.
    """
    if width <= 0:
        raise ValueError("width must be >= 1")
    if not all(c in "01" for c in bits):
        raise ValueError("bits must be a binary string")

    # apply offset by skipping initial bits
    if offset < 0 or offset >= width:
        raise ValueError("offset must be in [0, width-1]")

    usable = bits[offset:]
    length = len(usable)
    remainder = length % width

    if remainder and not ignore_tail:
        # pad with zeros to fill last token
        usable = usable + ("0" * (width - remainder))
    elif remainder and ignore_tail:
        usable = usable[: length - remainder]

    tokens: List[Token] = []
    for i in range(0, len(usable), width):
        chunk = usable[i:i+width]
        val = int(chunk, 2)
        el = ELEMENTS.get(val)
        t = Token(
            idx=i // width,
            bit_start=offset + i,
            bit_end=offset + i + width,
            bits=chunk,
            value=val,
            element=el,
        )
        tokens.append(t)
    return tokens


def score_tokens(tokens: List[Token]) -> float:
    """Return fraction of tokens that map to real elements (1..118)."""
    if not tokens:
        return 0.0
    good = sum(1 for t in tokens if t.element is not None)
    return good / len(tokens)


def best_offset_for_width(bits: str, width: int, ignore_tail: bool = True) -> Tuple[int, float, List[Token]]:
    """Try all offsets 0..width-1, return the one with highest element mapping ratio."""
    best = (-1, -1.0, [])
    for offset in range(width):
        toks = parse_fixed_width(bits, width, offset=offset, ignore_tail=ignore_tail)
        score = score_tokens(toks)
        if score > best[1]:
            best = (offset, score, toks)
    return best


def detect_reactions(symbols: List[str]) -> List[Tuple[int, str]]:
    """Detect simple motif-based reactions in the symbol stream (by token index).
    These are *motifs*, not balanced chemistry.
    """
    rxns: List[Tuple[int, str]] = []
    # Sliding windows
    for i in range(len(symbols)):
        a = symbols[i] if i < len(symbols) else None
        b = symbols[i+1] if i+1 < len(symbols) else None
        c = symbols[i+2] if i+2 < len(symbols) else None
        d = symbols[i+3] if i+3 < len(symbols) else None
        e = symbols[i+4] if i+4 < len(symbols) else None

        # Fusion-like motifs
        if a == "H" and b == "He":
            rxns.append((i, "H → He (fusion motif)"))
        if a == "H" and b == "H" and c == "He":
            rxns.append((i, "H2 → He (fusion motif)"))

        # Common molecules (motifs)
        if a == "C" and b == "O" and c == "O":
            rxns.append((i, "CO2 motif"))
        if a == "N" and b == "H" and c == "H" and d == "H":
            rxns.append((i, "NH3 motif"))
        if a == "C" and b == "H" and c == "H" and d == "H" and e == "H":
            rxns.append((i, "CH4 motif"))
        if a == "H" and b == "H" and c == "O":
            rxns.append((i, "H2O motif"))
        if a == "Na" and b == "Cl":
            rxns.append((i, "NaCl motif"))
    return rxns


def summarize(tokens: List[Token]) -> str:
    total = len(tokens)
    mapped = sum(1 for t in tokens if t.element)
    unmapped = total - mapped
    density = mapped / total if total else 0.0
    counts = Counter(t.element for t in tokens if t.element)
    common = ", ".join(f"{el}:{cnt}" for el, cnt in counts.most_common(10))
    return (
        f"Tokens: {total}\n"
        f"Mapped to elements: {mapped} ({density:.3%})\n"
        f"Unmapped: {unmapped}\n"
        f"Top elements: {common if common else '—'}\n"
    )


def export_csv(tokens: List[Token], reactions: List[Tuple[int, str]], path: str) -> None:
    if pd is None:
        print("pandas not installed; skipping CSV export.")
        return
    rxn_map = {}
    for i, label in reactions:
        rxn_map.setdefault(i, []).append(label)

    rows = []
    for t in tokens:
        rows.append({
            "token_index": t.idx,
            "bit_start": t.bit_start,
            "bit_end": t.bit_end,
            "bits": t.bits,
            "value": t.value,
            "element": t.element or "",
            "reactions": "; ".join(rxn_map.get(t.idx, [])),
        })
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)
    print(f"CSV written: {path} ({len(rows)} rows)")


def analyze_with_width(bits: str, width: int, ignore_tail: bool = True) -> None:
    print("=" * 70)
    print(f"Fixed‑width analysis | width={width}")
    offset, score, tokens = best_offset_for_width(bits, width, ignore_tail=ignore_tail)
    print(f"Best offset: {offset} | Element‑mapping rate: {score:.3%}")
    print(summarize(tokens))

    symbols = [t.element for t in tokens]
    reactions = detect_reactions(symbols)
    print(f"Detected reaction motifs: {len(reactions)}")
    for i, label in reactions[:20]:  # show first 20 only
        print(f"  @token {i}: {label}")

    export_csv(tokens, reactions, CSV_OUTPUT_PATH.replace('.csv', f"_w{width}_o{offset}.csv"))


def sweep_and_report(bits: str, widths: List[int]) -> None:
    for w in widths:
        analyze_with_width(bits, w, ignore_tail=IGNORE_PARTIAL_TAIL)


def main():
    # Start with the requested 5-bit parsing
    analyze_with_width(BINARY_STRING, N_BITS_DEFAULT, ignore_tail=IGNORE_PARTIAL_TAIL)
    # Optionally sweep additional widths
    if N_BITS_SWEEP:
        sweep_and_report(BINARY_STRING, [w for w in N_BITS_SWEEP if w != N_BITS_DEFAULT])


if __name__ == "__main__":
    main()
