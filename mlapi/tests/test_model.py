from model import IrisClassifier


def test_classifier_loads():
    clf = IrisClassifier()
    assert clf.model is not None


def test_single_prediction():
    clf = IrisClassifier()
    result = clf.predict([5.1, 3.5, 1.4, 0.2])
    assert "species" in result
    assert "confidence" in result
    assert 0.0 <= result["confidence"] <= 1.0


def test_batch_prediction():
    clf = IrisClassifier()
    samples = [[5.1, 3.5, 1.4, 0.2], [6.2, 3.4, 5.4, 2.3]]
    results = clf.predict_batch(samples)
    assert len(results) == 2
    for r in results:
        assert "species" in r
        assert "confidence" in r
