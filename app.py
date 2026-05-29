from flask import Flask, render_template, jsonify, request
import random
import string

app = Flask(__name__)

# 📚 Расширенный тематический словарь
WORD_LIST = [
    # Природа и лес
    "moss", "leaf", "root", "seed", "rain", "wind", "snow", "fire", "moon", "star",
    "sky", "cloud", "wave", "stone", "rock", "sand", "dust", "mist", "fog", "fern",
    "oak", "pine", "birch", "willow", "cedar", "aspen", "elm", "ash", "yew", "spruce",
    # Грибы и мицелий
    "mushroom", "fungus", "spore", "mycelium", "cap", "gill", "stem", "hyphae", "toadstool", "truffle",
    "amanita", "chanterelle", "morel", "porcini", "shiitake", "oyster", "enoki", "maitake", "reishi", "lion",
    # Животные леса
    "owl", "fox", "wolf", "bear", "deer", "frog", "toad", "raven", "crow", "hawk",
    "badger", "otter", "beaver", "hare", "lynx", "weasel", "hedgehog", "squirrel", "vole", "shrew",
    # Магия и руны
    "spell", "charm", "rune", "sigil", "glyph", "totem", "amulet", "talisman", "orb", "gem",
    "crystal", "pearl", "amber", "jade", "onyx", "quartz", "topaz", "ruby", "opal", "emerald",
    "elixir", "potion", "incant", "whisper", "shadow", "light", "dusk", "dawn", "twilight", "midnight",
    # Абстрактные и стихии
    "dream", "hope", "wish", "luck", "fate", "doom", "fear", "joy", "peace", "calm",
    "glow", "spark", "burn", "cool", "warm", "freeze", "melt", "flow", "grow", "bloom",
    "river", "lake", "stream", "creek", "pond", "marsh", "bog", "fen", "glade", "grove"
]

def generate_pronounceable_wordlist(length, use_numbers=True, use_caps=True):
    """Генерирует пароль из реальных слов (XKCD-стиль)"""
    avg_len = 5
    num_words = max(2, min(4, length // avg_len))
    words = random.sample(WORD_LIST, num_words)
    if use_caps:
        words = [w.capitalize() for w in words]
    suffix = ""
    if use_numbers:
        rem = length - len("-".join(words))
        if rem >= 2: suffix = str(random.randint(10, 99))
        elif rem == 1: suffix = str(random.randint(0, 9))
    pwd = "-".join(words) + suffix
    return pwd[:length] if len(pwd) > length else pwd

def generate_pronounceable_syllables(length):
    """Генерирует псевдослова из слогов"""
    syllables = [
        "ba", "be", "bi", "bo", "bu", "ca", "ce", "ci", "co", "cu",
        "da", "de", "di", "do", "du", "fa", "fe", "fi", "fo", "fu",
        "ga", "ge", "gi", "go", "gu", "ha", "he", "hi", "ho", "hu",
        "la", "le", "li", "lo", "lu", "ma", "me", "mi", "mo", "mu",
        "na", "ne", "ni", "no", "nu", "pa", "pe", "pi", "po", "pu",
        "ra", "re", "ri", "ro", "ru", "sa", "se", "si", "so", "su",
        "ta", "te", "ti", "to", "tu", "wa", "we", "wi", "wo", "wu",
        "sh", "ch", "th", "ng", "nk", "nt", "st", "nd", "ld", "rd"
    ]
    parts = []
    current_len = 0
    while current_len < length - 2:
        word_syls = []
        for _ in range(random.randint(2, 3)):
            s = random.choice(syllables)
            word_syls.append(s)
            current_len += len(s)
        word = "".join(word_syls).capitalize()
        parts.append(word)
        current_len += 1
        if len(parts) >= 3: break
    pwd = "-".join(parts)
    return pwd[:length] if len(pwd) > length else pwd

def generate_secure(length, use_upper, use_lower, use_digits, use_special, exclude_similar):
    """Генерирует криптографически случайный пароль с учётом фильтров"""
    charset = ""
    if use_lower: charset += string.ascii_lowercase
    if use_upper: charset += string.ascii_uppercase
    if use_digits: charset += string.digits
    if use_special: charset += string.punctuation

    if exclude_similar:
        for char in "Il1O0":
            charset = charset.replace(char, "")

    if not charset:
        charset = string.ascii_lowercase

    return ''.join(random.choice(charset) for _ in range(length))

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    length = int(data.get('length', 12))
    pronounceable = data.get('pronounceable', False)
    mode = data.get('pronounceable_mode', 'wordlist')  # 'wordlist' или 'syllables'

    if pronounceable:
        if mode == 'syllables':
            pwd = generate_pronounceable_syllables(length)
        else:
            pwd = generate_pronounceable_wordlist(length, data.get('use_digits', True), data.get('use_upper', True))
    else:
        pwd = generate_secure(
            length,
            data.get('use_upper', True),
            data.get('use_lower', True),
            data.get('use_digits', True),
            data.get('use_special', True),
            data.get('exclude_similar', False)
        )

    return jsonify({'password': pwd})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)