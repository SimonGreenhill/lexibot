
def test_valid(cldf_dataset, cldf_logger):
    assert cldf_dataset.validate(log=cldf_logger)


def test_parameters(cldf_dataset):
    assert len(list(cldf_dataset["ParameterTable"])) == 9


def test_languages(cldf_dataset):
    assert len(list(cldf_dataset["LanguageTable"])) == 189


def test_forms(cldf_dataset):
    # Yinhawangka-1_black-1,,Yinhawangka,1_black,warru/waru[76],warru,,,Haynie2016,,
    # Yinhawangka-1_black-2,,Yinhawangka,1_black,warru/waru[76],waru,,,Haynie2016,,

    forms = [
        f for f in cldf_dataset["FormTable"] if f["Value"] == 'warru/waru[76]'
    ]
    assert len(forms) == 2
    assert set([f["Form"] for f in forms]) == set(["waru", "warru"])


def test_cognates(cldf_dataset):
    assert len(list(cldf_dataset["CognateTable"])) == 0  # no cognates
