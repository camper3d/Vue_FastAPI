# преобразует задачу в camelcase
def to_camel_case(s: str) -> str:
    words = s.strip().split() # вырезает пробелы по бокам и разделяет слова
    if not words:
        return ""
    return words[0].lower() + ''.join(word.capitalize() for word in words[1:]) # соединяет слова в формате camelcase