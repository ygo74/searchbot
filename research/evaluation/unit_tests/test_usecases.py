import pytest
from unit_tests.llm import get_llm_response, compare_result

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from opik import track, llm_unit


@llm_unit()
def test_llm(sample):
    # Arrange
    question = sample['question']
    context = sample['context']
    answer = sample['answers']['text'][0]

    prompt = f"you must be concise and directly answers without additional context. Answer the question based on the following context: {context}\n\nQuestion: {question}\nAnswer:"

    # Act
    response = get_llm_response(prompt)


    # Assert
    comparison = compare_result(question=prompt, expected=answer, current=response.content)
    print(comparison)
    assert comparison["score"] > 0.8
    assert comparison["best_answer"] == "current" or comparison["best_answer"] == "both"
