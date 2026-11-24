from pathlib import Path
import joblib
import pandas as pd
import pytest

from pipeline import build_pipeline, evaluate_model


def test_build_pipeline():
    pipe_lr = build_pipeline("logistic_regression")
    assert "tfidf" in pipe_lr.named_steps
    assert "clf" in pipe_lr.named_steps

    pipe_nb = build_pipeline("multinomial_nb")
    assert "tfidf" in pipe_nb.named_steps
    assert "clf" in pipe_nb.named_steps

    with pytest.raises(ValueError):
        build_pipeline("unsupported_model")


def test_pipeline_fit_and_predict():
    train_texts = [
        "call win prize cash now win prize",
        "call win prize free entry text win",
        "hello see you at dinner tonight home",
        "hello see you at dinner tomorrow home",
    ]
    train_labels = ["spam", "spam", "ham", "ham"]

    pipe = build_pipeline("logistic_regression")
    pipe.fit(train_texts, train_labels)

    predictions = pipe.predict(["win cash prize", "dinner tomorrow"])
    assert len(predictions) == 2
    assert set(predictions).issubset({"ham", "spam"})


def test_saved_model_persistence(tmp_path):
    train_texts = [
        "urgent call free prize cash now prize",
        "urgent call free claim cash now prize",
        "meeting tomorrow morning office review notes",
        "meeting tomorrow afternoon office review notes",
    ]
    train_labels = ["spam", "spam", "ham", "ham"]

    pipe = build_pipeline("logistic_regression")
    pipe.fit(train_texts, train_labels)

    model_file = tmp_path / "test_model.joblib"
    joblib.dump(pipe, model_file)

    loaded_pipe = joblib.load(model_file)
    prediction = loaded_pipe.predict(["urgent free call"])[0]
    assert prediction in ("ham", "spam")
