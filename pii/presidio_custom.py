from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_analyzer import PatternRecognizer
from presidio_analyzer import Pattern



analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

def analyze_pii(text):

    results = analyzer.analyze(
        text=text,
        language='en'
    )

    return results

def anonymize_text(text, results):

    return anonymizer.anonymize(
        text=text,
        analyzer_results=results
    ).text
cnic_pattern = Pattern(
    name="cnic_pattern",
    regex=r"\d{5}-\d{7}-\d",
    score=0.9
)

cnic_recognizer = PatternRecognizer(
    supported_entity="CNIC",
    patterns=[cnic_pattern]
)

analyzer.registry.add_recognizer(cnic_recognizer)
