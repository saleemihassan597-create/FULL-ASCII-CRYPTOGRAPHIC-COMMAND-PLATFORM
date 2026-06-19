import math
import string
import hashlib
import base64
import re
from collections import Counter


# ─────────────────────────────────────────────────────────
#  UTILITIES
# ─────────────────────────────────────────────────────────

PRINTABLE_CHARS = [chr(i) for i in range(32, 127)]   # 95 printable ASCII chars
PRINTABLE_SET   = set(PRINTABLE_CHARS)

ENGLISH_FREQ = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97,
    'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25,
    'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36,
    'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.49,
    'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07
}

COMMON_WORDS = {"the","and","for","are","but","not","you","all","any","can","had",
                "her","was","one","our","out","day","get","has","him","his","how",
                "man","new","now","old","see","two","way","who","boy","did","its",
                "let","put","say","she","too","use","this","that","with","from"}


def english_score(text: str) -> float:
    """Chi-squared-style fitness score; lower = more English-like."""
    letters = [c.upper() for c in text if c.isalpha()]
    if not letters:
        return 9999.0
    total = len(letters)
    observed = Counter(letters)
    score = 0.0
    for ch, expected_pct in ENGLISH_FREQ.items():
        expected = (expected_pct / 100) * total
        obs = observed.get(ch, 0)
        if expected > 0:
            score += ((obs - expected) ** 2) / expected
    # Bonus: common word hits
    words = re.findall(r"[a-zA-Z']+", text.lower())
    hits  = sum(1 for w in words if w in COMMON_WORDS)
    score -= hits * 3          # reward common words
    return score


def calculate_entropy(text: str) -> float:
    if not text:
        return 0.0
    total = len(text)
    freq  = Counter(text)
    ent   = 0.0
    for count in freq.values():
        p    = count / total
        ent -= p * math.log2(p)
    return round(ent, 4)


def get_character_frequencies(text: str) -> dict:
    return dict(Counter(c for c in text if c.isalnum()))


# ─────────────────────────────────────────────────────────
#  CAESAR CIPHER  (Modulo-95 full ASCII)
# ─────────────────────────────────────────────────────────

class CaesarCipher:

    @staticmethod
    def _shift_char(char: str, shift: int) -> str:
        if char in PRINTABLE_SET:
            return chr(((ord(char) - 32 + shift) % 95) + 32)
        return char

    @staticmethod
    def encrypt(text: str, shift: int):
        result, steps = [], []
        for ch in text:
            enc = CaesarCipher._shift_char(ch, shift)
            result.append(enc)
            steps.append({
                "Input Char": repr(ch),
                "ASCII In": ord(ch),
                "Shift": shift,
                "ASCII Out": ord(enc),
                "Output Char": repr(enc),
            })
        return "".join(result), steps

    @staticmethod
    def decrypt(text: str, shift: int):
        return CaesarCipher.encrypt(text, -shift)

    @staticmethod
    def brute_force_crack(ciphertext: str):
        results = []
        for shift in range(1, 95):
            dec, _ = CaesarCipher.decrypt(ciphertext, shift)
            score  = english_score(dec)
            preview = dec[:80].replace("\n", " ")
            results.append({
                "Shift Key": shift,
                "Fitness Score": round(score, 2),
                "Decrypted Preview": preview,
            })
        results.sort(key=lambda x: x["Fitness Score"])
        return results[:20]

    @staticmethod
    def calculate_entropy(text: str) -> float:
        return calculate_entropy(text)

    @staticmethod
    def get_character_frequencies(text: str) -> dict:
        return get_character_frequencies(text)


# ─────────────────────────────────────────────────────────
#  VIGENÈRE CIPHER  (full ASCII)
# ─────────────────────────────────────────────────────────

class VigenereCipher:

    @staticmethod
    def derive_crypto_key(passphrase: str, length: int) -> str:
        """SHA-256 KDF → printable ASCII key of given length."""
        hashed = hashlib.sha256(passphrase.encode()).hexdigest()
        key    = "".join(PRINTABLE_CHARS[(int(c, 16) * 6) % 95] for c in hashed)
        # extend by repeating hash with salt
        while len(key) < length:
            hashed = hashlib.sha256((hashed + passphrase).encode()).hexdigest()
            key   += "".join(PRINTABLE_CHARS[(int(c, 16) * 6) % 95] for c in hashed)
        return key[:length]

    @staticmethod
    def encrypt(text: str, key: str) -> str:
        result, ki = [], 0
        for ch in text:
            if ch in PRINTABLE_SET:
                k_shift = ord(key[ki % len(key)]) - 32
                enc     = chr(((ord(ch) - 32 + k_shift) % 95) + 32)
                result.append(enc)
                ki += 1
            else:
                result.append(ch)
        return "".join(result)

    @staticmethod
    def decrypt(text: str, key: str) -> str:
        result, ki = [], 0
        for ch in text:
            if ch in PRINTABLE_SET:
                k_shift = ord(key[ki % len(key)]) - 32
                dec     = chr(((ord(ch) - 32 - k_shift) % 95) + 32)
                result.append(dec)
                ki += 1
            else:
                result.append(ch)
        return "".join(result)


# ─────────────────────────────────────────────────────────
#  ATBASH CIPHER  (full ASCII mirror)
# ─────────────────────────────────────────────────────────

class AtbashCipher:

    @staticmethod
    def process(text: str) -> str:
        """Symmetric: encrypt == decrypt."""
        result = []
        for ch in text:
            if ch in PRINTABLE_SET:
                mirrored = chr(126 - (ord(ch) - 32))
                result.append(mirrored)
            else:
                result.append(ch)
        return "".join(result)


# ─────────────────────────────────────────────────────────
#  ROT13 (letters only, classic)
# ─────────────────────────────────────────────────────────

class ROT13Cipher:

    @staticmethod
    def process(text: str) -> str:
        return text.translate(str.maketrans(
            string.ascii_uppercase + string.ascii_lowercase,
            string.ascii_uppercase[13:] + string.ascii_uppercase[:13] +
            string.ascii_lowercase[13:] + string.ascii_lowercase[:13]
        ))


# ─────────────────────────────────────────────────────────
#  XOR CIPHER
# ─────────────────────────────────────────────────────────

class XORCipher:

    @staticmethod
    def process(text: str, key: str) -> str:
        if not key:
            return text
        result = []
        for i, ch in enumerate(text):
            k   = key[i % len(key)]
            xored = chr(ord(ch) ^ ord(k))
            # keep printable
            if xored in PRINTABLE_SET:
                result.append(xored)
            else:
                result.append(ch)  # fallback: keep original
        return "".join(result)


# ─────────────────────────────────────────────────────────
#  RAIL FENCE CIPHER
# ─────────────────────────────────────────────────────────

class RailFenceCipher:

    @staticmethod
    def encrypt(text: str, rails: int) -> str:
        if rails < 2:
            return text
        fence = [[] for _ in range(rails)]
        rail, direction = 0, 1
        for ch in text:
            fence[rail].append(ch)
            if rail == 0:        direction = 1
            elif rail == rails-1: direction = -1
            rail += direction
        return "".join("".join(r) for r in fence)

    @staticmethod
    def decrypt(text: str, rails: int) -> str:
        if rails < 2:
            return text
        n      = len(text)
        pattern = []
        rail, direction = 0, 1
        for i in range(n):
            pattern.append(rail)
            if rail == 0:        direction = 1
            elif rail == rails-1: direction = -1
            rail += direction
        indices = sorted(range(n), key=lambda i: (pattern[i], i))
        result  = [""] * n
        for pos, ch in zip(indices, text):
            result[pos] = ch
        return "".join(result)


# ─────────────────────────────────────────────────────────
#  HASH TOOLS
# ─────────────────────────────────────────────────────────

class HashTools:

    @staticmethod
    def compute(text: str) -> dict:
        enc = text.encode()
        return {
            "MD5":    hashlib.md5(enc).hexdigest(),
            "SHA-1":  hashlib.sha1(enc).hexdigest(),
            "SHA-256": hashlib.sha256(enc).hexdigest(),
            "SHA-512": hashlib.sha512(enc).hexdigest(),
        }


# ─────────────────────────────────────────────────────────
#  BASE64 TOOLS
# ─────────────────────────────────────────────────────────

class Base64Tools:

    @staticmethod
    def encode(text: str) -> str:
        return base64.b64encode(text.encode()).decode()

    @staticmethod
    def decode(text: str) -> str:
        try:
            return base64.b64decode(text.encode()).decode()
        except Exception:
            return "[ERROR] Invalid Base64 input."


# ─────────────────────────────────────────────────────────
#  CIPHER COMPARE ENGINE
# ─────────────────────────────────────────────────────────

class CipherCompare:

    @staticmethod
    def compare_all(text: str, shift: int = 13, v_key: str = "AEGIS") -> list:
        derived_key = VigenereCipher.derive_crypto_key(v_key, 16)
        caesar_enc, _ = CaesarCipher.encrypt(text, shift)
        results = [
            {"Cipher": "Caesar",       "Output": caesar_enc,                         "Key": f"shift={shift}"},
            {"Cipher": "Vigenère",     "Output": VigenereCipher.encrypt(text, derived_key), "Key": derived_key[:12]+"…"},
            {"Cipher": "Atbash",       "Output": AtbashCipher.process(text),           "Key": "mirror"},
            {"Cipher": "ROT13",        "Output": ROT13Cipher.process(text),            "Key": "13"},
            {"Cipher": "Rail Fence 3", "Output": RailFenceCipher.encrypt(text, 3),     "Key": "rails=3"},
            {"Cipher": "Base64",       "Output": Base64Tools.encode(text),             "Key": "base64"},
        ]
        return results