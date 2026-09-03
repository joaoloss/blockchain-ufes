from hashlib import sha256

base = 'joaoloss'
options = list('1234567890qwertyuiopasdfghjklzxcvbnm')
n_zeros = 6

def enc(text: str) -> str:
    return sha256(text.encode()).hexdigest()

def check(enc_text: str) -> bool:
    return enc_text[:n_zeros] == '0'*n_zeros

max_sz = len(base) + 5

def go(text: str, count: int = 0) -> tuple[str | None, int]:
    count += 1

    enc_text = enc(text)

    if check(enc_text):
        return text, count

    if len(text) >= max_sz:
        return None, count

    for opt in options:
        r, count = go(text + opt, count)

        if r is not None:
            return r, count

    return None, count


final, n = go(base)

if final is None:
    print(f'Failed (trys: {n})')
else:
    print(f'===>>> {final} (trys: {n})')
    print(f'===>>> hash: {enc(final)}')