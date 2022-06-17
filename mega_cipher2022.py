import random

class Alphabet:
    """
    Класс для быстрого вычисления номера символа или нахождения символа по его номеру
    """
    def __init__(self, symbols):
        """
        Конструктор
        symbols: Строка или список с символами алфавита
        """
        if type(symbols) == str:
            symbols = list(symbols)
        self.symbol_to_index = {symbols[x]: x for x in range(len(symbols))}
        self.index_to_symbol = {x: symbols[x] for x in range(len(symbols))}

    def __getitem__(self, item):
        """
        Оператор индексации ищет номер символа в алфавите или символ по его номеру
        item: Номер символа в алфавите или символ
        return: Символ или номер символа в алфавите
        """
        try:
            if type(item) == int:
                return self.index_to_symbol[item]
            if type(item) == chr or type(item) == str:
                return self.symbol_to_index[item]
        except:
            return None

    def __len__(self):
        return len(self.index_to_symbol)


symbols = [chr(x) for x in range(ord("а"), ord("я") + 1)] + [chr(x) for x in range(ord("a"), ord("z") + 1)] + \
          [str(i) for i in range(10)]
alphabet = Alphabet(symbols)
eng_symbols = [chr(x) for x in range(ord("a"), ord("z") + 1)]
eng_alphabet = Alphabet(eng_symbols)


def vigenere_cipher_encode(message: str, key: str, alphabet=eng_alphabet):
    """
    Кодирование с помощью шифра Вижнера
    message: Текст сообщения
    key: Ключ
    alphabet: Обьект класса Alphabet для вычисления номера символа
    return: Закодированное сообщение
    """
    message = list(message)
    key = list(key)
    m = len(key)
    alphabet_size = len(alphabet)

    encoded_message = []

    # число символов из message которых нет в alphabet
    number_of_bad_characters = 0
    for i in range(len(message)):
        P = alphabet[message[i]]
        if P is None:
            number_of_bad_characters += 1
            encoded_message.append(message[i])
            continue
        K = alphabet[key[(i - number_of_bad_characters) % m]]
        encoded_message.append(alphabet[(P + K) % alphabet_size])
    return "".join(encoded_message)


def vigenere_cipher_decode(encoded_message: str, key: str, alphabet=eng_alphabet):
    """
    Декодирование с помощью шифра Вижнера
    encoded_message: Закодированный текст сообщения
    key: Ключ
    alphabet: Обьект класса Alphabet для вычисления номера символа
    return: Разкодированное сообщение
    """
    encoded_message = list(encoded_message)
    key = list(key)
    m = len(key)
    alphabet_size = len(alphabet)

    decoded_message = []

    # число символов из message которых нет в alphabet
    number_of_bad_characters = 0
    for i in range(len(encoded_message)):
        P = alphabet[encoded_message[i]]
        if P is None:
            number_of_bad_characters += 1
            encoded_message.append(encoded_message[i])
            continue
        K = alphabet[key[(i - number_of_bad_characters) % m]]
        decoded_message.append(alphabet[(P - K) % alphabet_size])
    return "".join(decoded_message)


def nod(a, b):
    # Наибольший общий делитель
    if a != 0 and b != 0:
        if a > b:
            return nod(a % b, b)
        return nod(a, b % a)
    return a + b


def extendGcd(a, b):
    # Расширенный алгоритм Евклида
    if b == 0:
        x = 1
        y = 0
        return x, y
    else:
        x1, y1 = extendGcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return x, y


def rsa_get_keys(p=13433879, q=18859111):
    """
    Генерация ключей
    :param p: Первое простое число
    :param q: Второе простое число
    :return: Приватная и публичная пары ключей
    """
    n = p * q
    fn = (p - 1) * (q - 1)
    e = random.randint(2, fn - 1)
    while nod(e, fn) != 1:
        e = random.randint(2, fn - 1)
    x, y = extendGcd(e, fn)
    if x < 0:
        x = x + fn
    d = x
    return (n, e), (n, d)


def rsa_encode(message, public_key):
    """
    Шифрование сообщения
    :param message: Целое число
    :param public_key: Публичный ключ
    :return: Зашифрованное сообщение
    """
    n, e = public_key
    return pow(message, e, n)


def rsa_decode(decoded_message, private_key):
    """
    Разшифрование сообщения
    :param decoded_message: Зашифрованное сообщение
    :param private_key: Приватный ключ
    :return: Исходное сообщение
    """
    n, d = private_key
    return pow(decoded_message, d, n)


if __name__ == "__main__":
    vigenere_tests = ["hello world", "i like pizza", "message", "asfsgashs"]
    rsa_tests = [12, 512, 1523125125, 7893220143053]
    public_key, private_key = rsa_get_keys()
    print("RSA test:\n")
    print("num -> encoding_num -> decoding_num")
    for x in rsa_tests:
        enc = rsa_encode(x, public_key)
        print(x, "->", enc, "->", rsa_decode(enc, private_key))
    print("\nPublic key:", public_key, "\nPrivate key:", private_key)
    print("-" * 100)

    print("Vigenere cipher test:\n")
    print("num -> encoding_num -> decoding_num")
    key = "pizza"
    for x in vigenere_tests:
        enc = vigenere_cipher_encode(x, key, eng_alphabet)
        print(x, "->", enc, "->", vigenere_cipher_decode(enc, key, eng_alphabet))

    print("\nKey:", key)
