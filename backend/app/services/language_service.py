from langdetect import detect, LangDetectException

LANGUAGE_NAMES = {
    "nl": "Dutch",
    "en": "English",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "it": "Italian",
    "pt": "Portuguese",
    "ar": "Arabic",
    "zh-cn": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "ru": "Russian",
    "pl": "Polish",
    "tr": "Turkish",
}


def detect_language(text: str) -> tuple[str, str]:
    """
    Returns (language_code, language_name_in_english).
    Defaults to English if detection fails.
    """
    try:
        code = detect(text)
        name = LANGUAGE_NAMES.get(code, "English")
        return code, name
    except LangDetectException:
        return "en", "English"
