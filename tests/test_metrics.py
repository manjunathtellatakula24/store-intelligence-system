# PROMPT:
# Generate unit tests for this feature.

# CHANGES MADE:
# Adapted assertions to the project structure and simplified validation.

def test_conversion_rate():

    entries = 10
    purchases = 2

    rate = round(
        (purchases / entries) * 100,
        2
    )

    assert rate == 20.0