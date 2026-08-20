import textstat

def compute_readability(text: str) -> dict:
    """Compute deterministic readability benchmarks via textstat."""
    return {
        "flesch_reading_ease":  round(textstat.flesch_reading_ease(text), 1),
        "gunning_fog":          round(textstat.gunning_fog(text), 1),
        "avg_sentence_length":  round(textstat.avg_sentence_length(text), 1),
        "word_count":           textstat.lexicon_count(text, removepunct=True),
        "sentence_count":       textstat.sentence_count(text),
        "syllable_count":       textstat.syllable_count(text),
        "smog_index":           round(textstat.smog_index(text), 1),
    }
