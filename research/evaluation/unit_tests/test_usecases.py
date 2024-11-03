import pytest
from unit_tests.lib.llm import get_llm_response, compare_result, map_response_to_dict

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from opik import track, llm_unit

import logging

# Configurer le logging
logging.basicConfig(level=logging.INFO)


# @llm_unit()
def test_llm(prompt_item, llm_chain):
    # Arrange
    print("")
    logging.info(f"Call llm : {prompt_item['name']}")

    llm_test = {
        "testNumber": len(pytest.llm_results),
        "name": prompt_item['name'],
        "user_prompt": prompt_item['user_prompt'],
        "context": prompt_item['context'] if 'context' in prompt_item else "",
        "expected_answer": prompt_item['expected_answer']
    }

    name = llm_test['name']
    user_prompt = llm_test['user_prompt']
    context = llm_test['context']

    # prompt = f"you must be concise and directly answers without additional context. Answer the question based on the following context: {context}\n\nQuestion: {question}\nAnswer:"

    # Act
    response = llm_chain.invoke(
        {
            "user_prompt": user_prompt
        }
    )
    print(response)
    map_response_to_dict(response, llm_test)
    pytest.llm_results[name] = llm_test

    assert response is not None, f"No response from llm call"
    assert not llm_test[ "filtered_hate" ], f"Response filtered due to hate detection"
    assert not llm_test[ "filtered_protected_material_code" ], f"Response filtered due to protected material code detection"
    assert not llm_test[ "filtered_protected_material_text" ], f"Response filtered due to protected material text detection"
    assert not llm_test[ "filtered_self_harm" ], f"Response filtered due to self harm detection"
    assert not llm_test[ "filtered_sexual" ], f"Response filtered due to sexual detection"
    assert not llm_test[ "filtered_violence" ], f"Response filtered due to violence detection"

def test_compare_llm_answer(prompt_name):

    # Arrange
    print("")
    logging.info(f"compare result : {prompt_name}")

    if prompt_name not in pytest.llm_results:
        pytest.skip(f"The test is skipped because '{prompt_name}' is not found in llm_results.")

    llm_test = pytest.llm_results[prompt_name]
    question = llm_test['user_prompt']
    context = llm_test['context']
    expected_answer = llm_test['expected_answer']
    answer = llm_test['answer']

    # Act
    comparison = compare_result(question=question, expected=expected_answer, current=answer)
    logging.debug(f"comparison result {comparison}")

    llm_test["comparison_score"] = comparison["score"]
    llm_test["best_answer"] = comparison["best_answer"]
    llm_test["comparison_reason"] = comparison["reason"]

    # Assert
    assert comparison["score"] > 0.8
    assert comparison["best_answer"] == "current" or comparison["best_answer"] == "both"
