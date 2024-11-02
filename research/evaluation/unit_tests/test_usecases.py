import pytest
from unit_tests.lib.llm import get_llm_response, compare_result

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from opik import track, llm_unit

import logging

# Configurer le logging
logging.basicConfig(level=logging.INFO)


# @llm_unit()
def test_llm(prompt_item):
    # Arrange
    print("")
    logging.info(f"Call llm : {prompt_item['name']}")

    llm_prompt = {
        "testNumber": len(pytest.llm_results),
        "user_prompt": prompt_item['user_prompt'],
        "context": prompt_item['context'] if 'context' in prompt_item else "",
        "expected_answer": prompt_item['expected_answer']
    }

    question = llm_prompt['user_prompt']
    context = llm_prompt['context']
    answer = llm_prompt['expected_answer']

    prompt = f"you must be concise and directly answers without additional context. Answer the question based on the following context: {context}\n\nQuestion: {question}\nAnswer:"

    # Act
    response = get_llm_response(prompt)

    # Assert
    comparison = compare_result(question=prompt, expected=answer, current=response.content)
    print(comparison)

    assert comparison["score"] > 0.8
    assert comparison["best_answer"] == "current" or comparison["best_answer"] == "both"
