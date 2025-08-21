# -*- coding: utf-8 -*-
"""
Wow! Signal — Master Validator & Consistency Checker
====================================================
Purpose
  • Unify and verify your prior results in one auditable run:
      1) Structural checks (lengths, counts, entropy).
      2) Mathematical markers (probabilistic Miller–Rabin primality).
      3) Chemistry/element motifs (H2He, H2O, CH4, selected atomic numbers).
      4) 5-bit parsing across all offsets; delimiter '11111' analysis.
      5) Command-language verification of ACTIVATE/DEACTIVATE deltas.
      6) Optional state evolution (DFT/QFT-like) to derive timestep deltas.
      7) Variable-bit-change trials (up to MAX_FLIPS=5) to test stability of findings.
      8) Consistency checks for constants you've used across scripts.

Inputs
  • Default binary string below (edit/replace as needed).
  • Hard-coded patterns you’ve referenced previously.

Outputs
  • Console report with PASS/FAIL flags per test.
  • CSV files for tokens, motif hits, and delta catalog (in ./validator_out).

Notes mapping to your prior work
  • ACTIVATE / DEACTIVATE 300-bit patterns & '11111' delimiter appear in your “final translation” code.  [See your Rosetta Stone + final translation ref]  # ref: files
  • TIMESTEPS=72 is consistent, but FREQUENCY_OFFSET_KEY is defined two ways (1420.4556 vs 50000) — we flag that.  # ref: files
  • 5-bit chunking & '11111' as a spacer/delimiter is baked in.  # ref: files
"""

from __future__ import annotations
import os, sys, math, random, csv, itertools, statistics
from typing import List, Dict, Tuple, Optional
from collections import Counter

# --- Try optional heavy deps gracefully (DFT/QFT step) ---
try:
    import numpy as np
    from scipy.linalg import dft
    HAVE_SCI = True
except Exception:
    HAVE_SCI = False
    np = None  # type: ignore

# ========== Configuration (edit as needed) ==========

# Candidate 300-bit message (replace with your latest)
BINARY_STRING = (
    "11001111111001111000111011110111110001110010011000101100000110000111010111001101100011100000011100100110110010000100110100110111111111111100000001100010110000011001101110000011100010101111110011010110010111101110100010101100100000110111110111000111000001011100100111111110110111100101110011101111111"
)

# Time evolution config seen across your scripts
TIMESTEPS_DECLARED = 72  # consistent across files
FREQS_SEEN = [1420.4556, 50000]  # conflicting values found across files

# Rosetta Stone / Command patterns you referenced (long 300-bit deltas)
COMMAND_ACTIVATE = "001110101001100100101101110000101111110011100001000110011100010011000111011110001001110000111110000011111110010011101101110100011101011101011001010110000010010101010011001000001011001011010101011100101111101000001010111010011110100100010100000110100110001011010111000110111011100001110111000110101000"
COMMAND_DEACTIVATE = "000010101100011101110000111011101100011101011010001100101100000101000100101111001011101010000010111110100111010101011010011010000010011001010101001000001101010011010111010111000101110110111001001111111000001111100001110010001111011100011001000111001100010000111001111110100001110110100100110010101110"
DELIMITER_5BIT = "11111"  # frequently treated as spacer/delimiter

# Chemistry motifs you referenced
CHEM_FORMULAE = {
    "1110": "H2He (Fusion blueprint)",  # H2He per your files
    "111000": "H2O (Water)",
    "1101111": "CH4 (Methane)",
}

# Element encodings you listed (selected)
ELEMENT_CODES = {
    "10": "He (2)", "11": "Li (3)", "101": "B (5)", "110": "C (6)", "111": "N (7)",
    "1011": "Na (11)", "1101": "Al (13)", "10001": "Cl (17)", "10011": "K (19)",
    "10111": "V (23)", "11101": "Cu (29)", "11111": "Ga (31) / Delimiter",
}

# Variable bit changing search (randomized trials)
MAX_FLIPS = 5
FLIP_TRIALS = 400  # increase for deeper search; watch runtime
RNG_SEED = 1337

OUTDIR = "validator_out"


# ========== Utilities ==========

def ensure_outdir() -> None:
    if not os.path.exists(OUTDIR):
        os.makedirs(OUTDIR)

def is_binary(s: str) -> bool:
    return all(ch in "01" for ch in s)

def shannon_entropy(bits: str) -> float:
    c = Counter(bits)
    n = len(bits)
    return -sum((v/n)*math.log2(v/n) for v in c.values())

def miller_rabin(n: int, k: int = 16) -> bool:
    """Probabilistic primality test appropriate for large ints."""
    if n < 2:
        return False
    # small primes
    smalls = [2,3,5,7,11,13,17,19,23,29]
    for p in smalls:
        if n == p:
            return True
        if n % p == 0:
            return False
    # write n-1 = d*2^r
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    rng = random.Random(99991)
    for _ in range(k):
        a = rng.randrange(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for __ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def find_all(pattern: str, s: str) -> List[int]:
    out = []
    start = 0
    while True:
        idx = s.find(pattern, start)
        if idx == -1:
            return out
        out.append(idx)
        start = idx + 1

def save_csv(path: str, rows: List[List[object]], header: Optional[List[str]] = None) -> None:
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        if header:
            w.writerow(header)
        w.writerows(rows)


# ========== 1) Structural sanity checks ==========

def structural_checks(bits: str) -> Dict[str, object]:
    results = {}
    results["valid_binary"] = is_binary(bits)
    results["length"] = len(bits)
    cnt = Counter(bits)
    results["ones"] = cnt.get("1", 0)
    results["zeros"] = cnt.get("0", 0)
    results["ones_pct"] = (results["ones"] / len(bits)) if len(bits) else 0.0
    results["entropy"] = shannon_entropy(bits) if len(bits) else 0.0
    return results


# ========== 2) Prime marker check ==========

def prime_check(bits: str) -> Dict[str, object]:
    if not is_binary(bits) or not bits:
        return {"checked": False, "is_probable_prime": False, "detail": "Non-binary or empty."}
    n = int(bits, 2)
    is_p = miller_rabin(n)
    return {"checked": True, "is_probable_prime": is_p, "num_digits_decimal": len(str(n))}


# ========== 3) Chemistry / element motif scans ==========

def scan_patterns(bits: str, patterns: Dict[str, str]) -> List[Tuple[str, str, int]]:
    """Return [(name, pattern, index), ...] for each match."""
    hits = []
    for pat, name in patterns.items():
        for idx in find_all(pat, bits):
            hits.append((name, pat, idx))
    hits.sort(key=lambda t: t[2])
    return hits


# ========== 4) 5-bit parsing & delimiter analysis ==========

def parse_fixed_width(bits: str, width: int, offset: int) -> List[str]:
    chunked = []
    i = offset
    while i + width <= len(bits):
        chunked.append(bits[i:i+width])
        i += width
    return chunked

def five_bit_survey(bits: str) -> Dict[str, object]:
    rows = []
    delim_counts = {}
    for offset in range(5):
        toks = parse_fixed_width(bits, 5, offset)
        count = len(toks)
        delim = toks.count(DELIMITER_5BIT)
        delim_counts[offset] = delim
        rows += [[offset, i, tok, int(tok == DELIMITER_5BIT)] for i, tok in enumerate(toks)]
    ensure_outdir()
    save_csv(os.path.join(OUTDIR, "five_bit_tokens.csv"),
             rows, header=["offset","index","token","is_delimiter"])
    return {"tokens_csv": os.path.join(OUTDIR, "five_bit_tokens.csv"),
            "delimiter_counts": delim_counts}


# ========== 5) Command language verification ==========

def verify_command_lengths() -> Dict[str, object]:
    return {
        "activate_len": len(COMMAND_ACTIVATE),
        "deactivate_len": len(COMMAND_DEACTIVATE),
        "equal_length": len(COMMAND_ACTIVATE) == len(COMMAND_DEACTIVATE)
    }

def search_command_patterns(bits: str) -> Dict[str, List[int]]:
    return {
        "ACTIVATE_hits": find_all(COMMAND_ACTIVATE, bits),
        "DEACTIVATE_hits": find_all(COMMAND_DEACTIVATE, bits)
    }


# ========== 6) Optional timestep evolution + delta catalog ==========

def evolve_and_catalog(bits: str, timesteps: int, freq_key: float) -> Dict[str, object]:
    if not HAVE_SCI:
        return {"available": False, "reason": "NumPy/SciPy not available; skipping evolution."}
    # Initial +/-1 state
    init = np.array([1 if b == "1" else -1 for b in bits], dtype=np.complex128)
    n = len(init)
    q = dft(n, scale="sqrtn")
    states = [init.copy()]
    for t in range(timesteps):
        evolved = q @ states[-1]
        phase = np.exp(1j * 2 * np.pi * freq_key * t / (timesteps * 1e6))
        states.append(evolved * phase)
    bin_states = ["".join("1" if np.real(v) >= 0 else "0" for v in st) for st in states]
    deltas = ["".join('1' if a != b else '0' for a, b in zip(bin_states[i], bin_states[i+1]))
              for i in range(len(bin_states)-1)]
    # Catalog deltas
    cat = Counter(deltas)
    rows = [[d, c] for d, c in cat.most_common()]
    ensure_outdir()
    out_csv = os.path.join(OUTDIR, f"delta_catalog_{freq_key}.csv")
    save_csv(out_csv, rows, header=["delta_bits", "count"])
    return {"available": True, "deltas_csv": out_csv, "unique_deltas": len(cat)}


# ========== 7) Variable bit changing (random flip trials) ==========

def random_flip(bits: str, positions: List[int]) -> str:
    lst = list(bits)
    for p in positions:
        lst[p] = "1" if lst[p] == "0" else "0"
    return "".join(lst)

def flip_search(bits: str,
                motifs: Dict[str, str],
                max_flips: int = MAX_FLIPS,
                trials: int = FLIP_TRIALS,
                seed: int = RNG_SEED) -> Dict[str, object]:
    """
    Randomly flip up to `max_flips` bits (uniformly sampled count in [1..max_flips])
    and record if motif hits strictly increase; repeat for `trials`.
    """
    rng = random.Random(seed)
    base_hits = scan_patterns(bits, motifs)
    base_count = len(base_hits)
    improved = 0
    examples = []
    n = len(bits)
    for _ in range(trials):
        k = rng.randint(1, max_flips)
        pos = sorted(rng.sample(range(n), k))
        mutated = random_flip(bits, pos)
        new_hits = scan_patterns(mutated, motifs)
        if len(new_hits) > base_count:
            improved += 1
            examples.append({"flip_positions": pos, "gain": len(new_hits) - base_count})
    return {"baseline_hits": base_count, "improved_trials": improved, "examples": examples[:10]}


# ========== 8) Cross-script consistency checks (constants) ==========

def consistency_checks() -> Dict[str, object]:
    issues = []
    # Timesteps expectation
    if TIMESTEPS_DECLARED != 72:
        issues.append(f"Expected TIMESTEPS=72, got {TIMESTEPS_DECLARED}.")
    # Conflicting frequency offset keys observed across your scripts:
    # (1420.4556 vs 50000) – keep both available and report.
    if len(set(FREQS_SEEN)) > 1:
        issues.append(f"Conflicting FREQUENCY_OFFSET_KEY values observed: {FREQS_SEEN}.")
    # Command length sanity
    cl = verify_command_lengths()
    if not cl["equal_length"]:
        issues.append("ACTIVATE/DEACTIVATE commands are different lengths.")
    if cl["activate_len"] != 300 or cl["deactivate_len"] != 300:
        issues.append(f"Command lengths not 300 bits (A={cl['activate_len']}, D={cl['deactivate_len']}).")
    return {"issues": issues, "freq_keys": FREQS_SEEN, "timesteps": TIMESTEPS_DECLARED}


# ========== Main orchestration ==========

def main():
    ensure_outdir()
    print("="*70)
    print("WOW! SIGNAL — MASTER VALIDATOR & CONSISTENCY CHECKER")
    print("="*70)

    # 1) Structural
    s = structural_checks(BINARY_STRING)
    print("\n[STRUCTURE]")
    print(f"  Valid binary: {s['valid_binary']}  |  Length: {s['length']}")
    print(f"  Ones: {s['ones']}  Zeros: {s['zeros']}  Ones%: {s['ones_pct']:.2%}")
    print(f"  Shannon entropy: {s['entropy']:.5f}")

    # 2) Prime
    p = prime_check(BINARY_STRING)
    print("\n[PRIME MARKER]")
    if p["checked"]:
        print(f"  Probable prime: {p['is_probable_prime']}  |  Decimal digits: {p['num_digits_decimal']}")
    else:
        print(f"  Skipped: {p['detail']}")

    # 3) Chemistry & elements
    chem_hits = scan_patterns(BINARY_STRING, CHEM_FORMULAE)
    elem_hits = scan_patterns(BINARY_STRING, ELEMENT_CODES)
    print("\n[CHEMISTRY MOTIFS]")
    if chem_hits:
        for name, pat, idx in chem_hits:
            print(f"  Found {name}  (pattern={pat}) at bit {idx}")
    else:
        print("  No chemistry motifs found.")

    print("\n[ELEMENT CODES]")
    if elem_hits:
        for name, pat, idx in elem_hits[:50]:
            print(f"  Found {name}  (pattern={pat}) at bit {idx}")
        if len(elem_hits) > 50:
            print(f"  ... and {len(elem_hits) - 50} more")
    else:
        print("  No element codes found.")

    # 4) 5-bit survey
    five = five_bit_survey(BINARY_STRING)
    print("\n[5-BIT SURVEY]")
    print(f"  Tokens CSV: {five['tokens_csv']}")
    print(f"  Delimiter '11111' counts by offset: {five['delimiter_counts']}")

    # 5) Command search
    cmd_lens = verify_command_lengths()
    cmd_hits = search_command_patterns(BINARY_STRING)
    print("\n[COMMAND PATTERNS]")
    print(f"  ACTIVATE length={cmd_lens['activate_len']}, DEACTIVATE length={cmd_lens['deactivate_len']}, equal={cmd_lens['equal_length']}")
    print(f"  ACTIVATE occurrences: {cmd_hits['ACTIVATE_hits']}")
    print(f"  DEACTIVATE occurrences: {cmd_hits['DEACTIVATE_hits']}")

    # 6) Evolution & delta catalog (run both freq keys if SciPy available)
    if HAVE_SCI:
        for fk in FREQS_SEEN:
            evo = evolve_and_catalog(BINARY_STRING, TIMESTEPS_DECLARED, fk)
            print(f"\n[EVOLUTION] freq_key={fk}")
            if evo["available"]:
                print(f"  Unique deltas: {evo['unique_deltas']}")
                print(f"  Delta catalog: {evo['deltas_csv']}")
            else:
                print(f"  Skipped: {evo['reason']}")
    else:
        print("\n[EVOLUTION] Skipped — NumPy/SciPy not available.")

    # 7) Variable bit changing trials (default up to 5 flips)
    improv = flip_search(BINARY_STRING, CHEM_FORMULAE, max_flips=MAX_FLIPS, trials=FLIP_TRIALS, seed=RNG_SEED)
    print("\n[VARIABLE BIT CHANGING — RANDOM TRIALS]")
    print(f"  Baseline motif hits: {improv['baseline_hits']}")
    print(f"  Trials with increased motif hits: {improv['improved_trials']} / {FLIP_TRIALS}")
    if improv["examples"]:
        print("  Examples (first 10):")
        for ex in improv["examples"]:
            print(f"    flips={ex['flip_positions'][:8]}...  gain=+{ex['gain']}")

    # 8) Cross-script consistency
    cons = consistency_checks()
    print("\n[CONSISTENCY CHECKS]")
    if cons["issues"]:
        for issue in cons["issues"]:
            print(f"  ISSUE: {issue}")
    else:
        print("  No issues detected.")
    print(f"  Timesteps={cons['timesteps']}  |  Observed frequency keys={cons['freq_keys']}")

    print("\n--- DONE ---")
    print(f"Artifacts written to: ./{OUTDIR}")

if __name__ == "__main__":
    main()
