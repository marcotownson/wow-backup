# -*- coding: utf-8 -*-
"""
Wow! Signal — Fixed-Width & Semantic Analyzer (Extended with Chinese Language Support)

This extended master validator builds on the prior "Fixed-Width Binary Analyzer" and
adds semantic dimensions including equation discovery, multi-encoding scans, and
support for potential Mandarin Chinese encodings.

Usage:
  python wow_signal_semantic_analyzer.py

Outputs (validator_out/):
  - semantic_tokens_w{w}_o{o}.csv
  - ascii_mode{m}_o{o}.csv
  - equation_candidates.csv
  - prime_candidates.csv
  - ratio_candidates.csv
  - summary.json
"""
from __future__ import annotations
import os, json, csv, re
from typing import List, Dict, Tuple, Optional
from collections import Counter
import base64
import math

# ------------------ CONFIG ------------------
BINARY_STRING = (
    "110011111110011110001110111101111100011100100110001011000001100001110101110011011000111000000111001001101100100001001101001101111111111111000000011000101100000110011011100000111000101011111100110101100101111011101000101011001000001101111101110001110000010111001001111111101101111001011100111011111111"
)

OUTDIR = "validator_out"
N_BITS_SWEEPS = [5, 6, 7, 8, 9]   # 5-9 bits requested
IGNORE_PARTIAL_TAIL = True
SPECIAL_NUMBERS = [26, 72, 1868, 2, 144, 796, 1420, 4556]
ASCII_MODES = [7, 8]
BASE_ENCODINGS = {
    'base36': 36,
    'base64': 64
}

# --- NEW: Configuration for Chinese language analysis ---
CHINESE_ENCODINGS = ['utf-8', 'gbk', 'gb18030', 'big5']
CHINESE_PATTERNS = {
    'mass_energy_equivalence': r'质能方程|E\s*=\s*mc\s*2', # Search for the term or the formula
    'pi': r'圆周率',
    'prime_number': r'质数|素数',
    'hydrogen': r'氢',
    'helium': r'氦',
    'water': r'水'
}
# ---------------------------------------------------------


# Added new constants to search for
MATHEMATICAL_CONSTANTS = {
    'PI': 3.14159,
    'E': 2.71828,
    'FINE_STRUCTURE': 0.007297
}

os.makedirs(OUTDIR, exist_ok=True)

# ------------------ UTILITIES ------------------
def to_int(bits: str, endian: str = 'big') -> int:
    if endian == 'big':
        return int(bits, 2)
    return int(bits[::-1], 2)  # little endian

def chunk_bits(bits: str, width: int, offset: int = 0, ignore_tail: bool = True) -> List[str]:
    s = bits[offset:]
    rem = len(s) % width
    if rem and ignore_tail:
        s = s[:len(s)-rem]
    elif rem and not ignore_tail:
        s = s + ('0' * (width - rem))
    return [s[i:i+width] for i in range(0, len(s), width) if i+width <= len(s)]

def write_csv(path: str, header: List[str], rows: List[List[object]]) -> None:
    with open(path, 'w', newline='', encoding='utf-8') as f: # Use UTF-8 for CSVs
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)

def find_all(substr: str, s: str) -> List[int]:
    out = []
    i = 0
    while True:
        pos = s.find(substr, i)
        if pos == -1:
            break
        out.append(pos)
        i = pos + 1
    return out

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# ------------------ DECODERS ------------------
def decode_fixed_width(bits: str, width: int, offset: int) -> List[Dict]:
    toks = chunk_bits(bits, width, offset, IGNORE_PARTIAL_TAIL)
    out = []
    for idx, t in enumerate(toks):
        out.append({
            'token_index': idx,
            'bit_start': offset + idx*width,
            'bit_end': offset + (idx+1)*width,
            'bits': t,
            'value_big': to_int(t, 'big'),
            'value_little': to_int(t, 'little')
        })
    return out

def decode_ascii(bits: str, mode: int, offset: int = 0) -> List[Dict]:
    toks = chunk_bits(bits, mode, offset, IGNORE_PARTIAL_TAIL)
    out = []
    for idx, t in enumerate(toks):
        v = to_int(t, 'big')
        ch = chr(v) if 32 <= v <= 126 else ''
        out.append({'token_index': idx, 'bits': t, 'ascii_val': v, 'char': ch})
    return out

def decode_base_encoding(bits: str, base: int) -> Optional[str]:
    try:
        if base == 64:
            # Base64 requires byte-like object and is padded to be multiple of 8 bits
            padded_bits = bits + '0' * ((8 - (len(bits) % 8)) % 8)
            byte_string = int(padded_bits, 2).to_bytes((len(padded_bits) + 7) // 8, byteorder='big')
            return base64.b64encode(byte_string).decode('utf-8')
        elif base == 36:
            val = int(bits, 2)
            if val == 0:
                return '0'
            chars = []
            while val > 0:
                chars.append("0123456789abcdefghijklmnopqrstuvwxyz"[val % 36])
                val //= 36
            return ''.join(reversed(chars))
    except (ValueError, IndexError):
        return None

# --- NEW: Chinese Language Decoder ---
def decode_and_search_chinese(bits: str) -> Dict:
    """
    Attempts to decode the entire bitstream using various Chinese character encodings
    and searches for scientific keywords.
    """
    results = {}
    # Pad bits to be a multiple of 8 (a full byte)
    padded_bits = bits + '0' * ((8 - (len(bits) % 8)) % 8)
    try:
        byte_data = int(padded_bits, 2).to_bytes((len(padded_bits) + 7) // 8, byteorder='big')
    except OverflowError:
        return {"error": "Binary string too large to convert to bytes."}

    for encoding in CHINESE_ENCODINGS:
        try:
            decoded_string = byte_data.decode(encoding)
            
            # Remove non-printable characters for cleaner analysis
            printable_string = "".join(c for c in decoded_string if c.isprintable())
            
            if not printable_string:
                continue

            hits = []
            for pattern_name, regex in CHINESE_PATTERNS.items():
                for match in re.finditer(regex, printable_string, flags=re.I):
                    hits.append({
                        'type': pattern_name,
                        'string': match.group(0),
                        'start_index': match.start()
                    })
            
            if hits:
                results[encoding] = {
                    'decoded_string_preview': printable_string[:200] + ('...' if len(printable_string) > 200 else ''),
                    'hits': hits
                }
        except (UnicodeDecodeError, LookupError):
            # This encoding did not work, continue to the next one
            continue
            
    return results
# --------------------------------------

# ------------------ SEARCH HELPERS ------------------
def search_numbers_in_tokens(tokens: List[Dict], numbers: List[int]) -> List[Tuple[int,int,str]]:
    hits = []
    for t in tokens:
        if t['value_big'] in numbers:
            hits.append((t['token_index'], t['value_big'], 'big'))
        if t['value_little'] in numbers and t['value_little'] != t['value_big']:
            hits.append((t['token_index'], t['value_little'], 'little'))
    return hits

def search_numbers_in_ascii(ascii_tokens: List[Dict], numbers: List[int]) -> List[Tuple[int,int,str]]:
    hits = []
    for t in ascii_tokens:
        if t['char'] and t['char'].isdigit():
            # if the ascii char is a digit — check for multi-digit sequences is handled elsewhere
            for n in numbers:
                if str(n) == t['char']:
                    hits.append((t['token_index'], n, 'ascii_char'))
        if t['ascii_val'] in numbers:
            hits.append((t['token_index'], t['ascii_val'], 'ascii_val'))
    return hits

# ------------------ EQUATION DETECTION ------------------
PHYSICS_EQS = [
    (['E','=','m','c','2'], 'E=mc^2'),
    (['F','=','m','a'], 'F=ma'),
    (['e','=','m','c','2'], 'e=mc2'),
    (['p','=','m','v'], 'p=mv')
]

# Fuzzy regex allowing spaces, different casing, and common variations
EQUATION_PATTERNS = {
    'E=mc2': r'E\s*=\s*m\s*c\s*(\^|\*\*)?\s*2',
    'F=ma': r'F\s*=\s*m\s*a',
    'p=mv': r'p\s*=\s*m\s*v',
    'a=bc^2': r'[a-zA-Z]\s*=\s*[a-zA-Z]\s*[a-zA-Z]\s*(\^)?\s*2',
    'f=ma': r'f\s*=\s*m\s*a'
}

def detect_equations_in_ascii_tokens(ascii_tokens: List[Dict]) -> List[Dict]:
    chars = [t['char'] if t['char'] else '.' for t in ascii_tokens]
    S = ''.join(chars)
    results = []
    
    # Fuzzy regex detection
    for eq_type, pattern in EQUATION_PATTERNS.items():
        for m in re.finditer(pattern, S, flags=re.I):
            results.append({'source': 'ascii_regex', 'type': eq_type, 'start_index': m.start(), 'string': m.group(0)})

    return results

def detect_symbolic_equations(tokens: List[Dict], tolerance: float = 0.0) -> List[Dict]:
    results = []
    vals = [t['value_big'] for t in tokens]
    
    # Check for simple algebraic relationships
    # a = b*c, a = b*c^2, a = b/c, etc. within a short window
    WINDOW_SIZE = 5

    for i in range(len(vals) - WINDOW_SIZE):
        window = vals[i:i+WINDOW_SIZE]
        a, b, c, d, e = window
        
        # Check a = b*c
        if a != 0 and b != 0 and c != 0 and abs(a - (b*c)) / abs(a) <= tolerance:
            results.append({'type': 'symbolic_axbc', 'formula': f'{a} = {b} * {c}', 'token_start': i, 'bit_start': tokens[i]['bit_start']})
        
        # Check a = b*c^2
        if a != 0 and b != 0 and c != 0 and abs(a - (b * c**2)) / abs(a) <= tolerance:
            results.append({'type': 'symbolic_axbc2', 'formula': f'{a} = {b} * {c}^2', 'token_start': i, 'bit_start': tokens[i]['bit_start']})
        
        # Check a = b + c
        if a != 0 and abs(a - (b+c)) / abs(a) <= tolerance:
            results.append({'type': 'symbolic_axbpc', 'formula': f'{a} = {b} + {c}', 'token_start': i, 'bit_start': tokens[i]['bit_start']})
        
        # Check a^2 + b^2 = c^2
        if c != 0 and abs(c**2 - (a**2 + b**2)) / c**2 <= tolerance:
            results.append({'type': 'symbolic_pythagorean', 'formula': f'{a}^2 + {b}^2 = {c}^2', 'token_start': i, 'bit_start': tokens[i]['bit_start']})
            
        # Check F=ma
        if a != 0 and b != 0 and c != 0 and abs(a - b*c) / abs(a) <= tolerance:
            results.append({'type': 'symbolic_fma', 'formula': f'{a} = {b} * {c}', 'token_start': i, 'bit_start': tokens[i]['bit_start']})
            
        # Check E=hf
        if a != 0 and b != 0 and c != 0 and abs(a - b*c) / abs(a) <= tolerance:
            results.append({'type': 'symbolic_ehf', 'formula': f'{a} = {b} * {c}', 'token_start': i, 'bit_start': tokens[i]['bit_start']})

    return results

def detect_primes(tokens: List[Dict]) -> List[Dict]:
    results = []
    for token in tokens:
        val = token['value_big']
        if is_prime(val):
            results.append({'type': 'prime', 'value': val, 'token_start': token['token_index'], 'bit_start': token['bit_start']})
    return results

def detect_ratios(tokens: List[Dict], constants: Dict[str, float], tolerance: float = 0.01) -> List[Dict]:
    results = []
    vals = [t['value_big'] for t in tokens]
    
    for i in range(len(vals) - 1):
        if vals[i+1] != 0 and vals[i] != 0:
            ratio = vals[i] / vals[i+1]
            for name, const_val in constants.items():
                if abs(ratio - const_val) / abs(const_val) <= tolerance:
                    results.append({'type': 'ratio', 'ratio_of': f'{vals[i]}/{vals[i+1]}', 'approx_constant': name, 'token_start': i, 'bit_start': tokens[i]['bit_start']})
    return results

# ------------------ ANALYSIS PASSES ------------------
def analyze_widths_and_encodings(bits: str, widths: List[int]) -> Dict:
    summary = {'per_width': {}}
    for w in widths:
        best_offset = 0
        best_tokens = []
        best_score = -1
        for offset in range(w):
            toks = decode_fixed_width(bits, w, offset)
            score = sum(1 for t in toks if 0 <= t['value_big'] <= 255) / (len(toks) if toks else 1)
            if score > best_score:
                best_score = score
                best_offset = offset
                best_tokens = toks
        # write tokens CSV
        csv_path = os.path.join(OUTDIR, f"semantic_tokens_w{w}_o{best_offset}.csv")
        rows = [[t['token_index'], t['bit_start'], t['bit_end'], t['bits'], t['value_big'], t['value_little']] for t in best_tokens]
        write_csv(csv_path, ['token_index','bit_start','bit_end','bits','value_big','value_little'], rows)
        # number hits
        num_hits = search_numbers_in_tokens(best_tokens, SPECIAL_NUMBERS)
        summary['per_width'][w] = {'best_offset': best_offset, 'score': best_score, 'tokens_csv': csv_path, 'num_hits': num_hits}
    # ASCII passes
    summary['ascii'] = {}
    for mode in ASCII_MODES:
        best_offset = 0
        best_print_ratio = -1
        best_atoks = []
        for offset in range(mode):
            atoks = decode_ascii(bits, mode, offset)
            printable_ratio = sum(1 for t in atoks if t['char']) / (len(atoks) if atoks else 1)
            if printable_ratio > best_print_ratio:
                best_print_ratio = printable_ratio
                best_offset = offset
                best_atoks = atoks
        csv_path = os.path.join(OUTDIR, f"ascii_mode{mode}_o{best_offset}.csv")
        write_csv(csv_path, ['token_index','bits','ascii_val','char'], [[t['token_index'], t['bits'], t['ascii_val'], t['char']] for t in best_atoks])
        summary['ascii'][mode] = {'best_offset': best_offset, 'print_ratio': best_print_ratio, 'csv': csv_path, 'equations': detect_equations_in_ascii_tokens(best_atoks)}
    # Alternate encodings
    summary['alternate_encodings'] = {}
    for name, base in BASE_ENCODINGS.items():
        decoded_string = decode_base_encoding(bits, base)
        if decoded_string:
            summary['alternate_encodings'][name] = {'decoded_string': decoded_string, 'eq_matches': []}
            for eq_type, pattern in EQUATION_PATTERNS.items():
                if re.search(pattern, decoded_string, flags=re.I):
                    summary['alternate_encodings'][name]['eq_matches'].append(eq_type)
    
    # --- NEW: Add Chinese analysis to the summary ---
    summary['chinese_analysis'] = decode_and_search_chinese(bits)
    # -----------------------------------------------

    return summary

def analyze_special_numbers(bits: str, numbers: List[int]) -> Dict:
    results = {}
    for n in numbers:
        b = bin(n)[2:]
        hits_be = find_all(b, bits)
        hits_le = find_all(b[::-1], bits)
        results[n] = {'binary': b, 'big_endian_hits': hits_be, 'little_endian_hits': hits_le}
    return results

# ------------------ RUN / DUMP ------------------
def run_all(bits: str) -> Dict:
    out = {'length': len(bits), 'ones': bits.count('1'), 'zeros': bits.count('0')}
    out['semantic'] = analyze_widths_and_encodings(bits, N_BITS_SWEEPS)
    out['special_numbers'] = analyze_special_numbers(bits, SPECIAL_NUMBERS)
    # gather eq candidates from tokens written above
    eq_candidates = []
    prime_candidates = []
    ratio_candidates = []
    
    for w, meta in out['semantic']['per_width'].items():
        csvp = meta['tokens_csv']
        toks = []
        with open(csvp, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                toks.append({
                    'token_index': int(row['token_index']),
                    'bit_start': int(row['bit_start']),
                    'bit_end': int(row['bit_end']),
                    'bits': row['bits'],
                    'value_big': int(row['value_big'])
                })
        
        # New symbolic detection
        eq_candidates += detect_symbolic_equations(toks, tolerance=0.0) # Search for exact matches
        eq_candidates += detect_symbolic_equations(toks, tolerance=0.01) # Search with tolerance
        
        # Prime number detection
        prime_candidates += detect_primes(toks)
        
        # Ratio detection
        ratio_candidates += detect_ratios(toks, MATHEMATICAL_CONSTANTS, tolerance=0.01)

    # Flatten ascii-detected eqs
    for mode, md in out['semantic'].get('ascii', {}).items():
        ascii_eqs = md.get('equations', [])
        for e in ascii_eqs:
            eq_candidates.append({'source': f'ascii_mode{mode}', **e})
    
    # Add alternate encoding hits
    for enc, data in out['semantic'].get('alternate_encodings', {}).items():
        if data['eq_matches']:
            for match in data['eq_matches']:
                eq_candidates.append({'source': enc, 'type': match, 'text': data['decoded_string']})

    # --- NEW: Add Chinese analysis hits to equation candidates ---
    for enc, data in out['semantic'].get('chinese_analysis', {}).items():
        if data.get('hits'):
            for hit in data['hits']:
                eq_candidates.append({
                    'source': f'chinese_{enc}',
                    'type': hit['type'],
                    'text': hit['string'],
                    'start': hit['start_index']
                })
    # -------------------------------------------------------------

    out['equation_candidates'] = eq_candidates
    out['prime_candidates'] = prime_candidates
    out['ratio_candidates'] = ratio_candidates

    with open(os.path.join(OUTDIR, 'summary.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    
    # write eq CSV
    rows = []
    for e in eq_candidates:
        rows.append([e.get('source', 'numeric_symbolic'), e.get('type',''), e.get('formula') or e.get('text') or e.get('string',''), e.get('token_start', e.get('start_index', ''))])
    write_csv(os.path.join(OUTDIR, 'equation_candidates.csv'), ['source','type','text','start'], rows)
    
    # write prime CSV
    rows = []
    for p in prime_candidates:
        rows.append([p['type'], p['value'], p['token_start'], p['bit_start']])
    write_csv(os.path.join(OUTDIR, 'prime_candidates.csv'), ['type','value','token_start','bit_start'], rows)
    
    # write ratio CSV
    rows = []
    for r in ratio_candidates:
        rows.append([r['type'], r['ratio_of'], r['approx_constant'], r['token_start'], r['bit_start']])
    write_csv(os.path.join(OUTDIR, 'ratio_candidates.csv'), ['type','ratio_of','approx_constant','token_start','bit_start'], rows)
    
    return out

if __name__ == '__main__':
    print('Running semantic analyzer (extended with Chinese support)')
    summary = run_all(BINARY_STRING)
    print('Done. Summary written to:', os.path.join(OUTDIR, 'summary.json'))
    print('Equation candidates CSV:', os.path.join(OUTDIR, 'equation_candidates.csv'))
    print('Prime candidates CSV:', os.path.join(OUTDIR, 'prime_candidates.csv'))
    print('Ratio candidates CSV:', os.path.join(OUTDIR, 'ratio_candidates.csv'))