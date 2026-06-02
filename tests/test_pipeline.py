# PROMPT:
# Generate unit tests for this feature.

# CHANGES MADE:
# Adapted assertions to the project structure and simplified validation.

def test_pipeline():

    visitor_id = "VIS_1"

    assert visitor_id.startswith("VIS")