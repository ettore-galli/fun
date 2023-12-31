from typing import Dict
from unittest.mock import MagicMock, call


from functional.functional_tools.composing_single import (
    ExecutionContext,
    bind,
    bind_all,
)


def test_bind():
    function_a = MagicMock()
    function_a.side_effect = lambda context: ExecutionContext[Dict, Dict](
        environment=context.environment, payload={"x": 3}
    )
    function_b = MagicMock()

    compound = bind(function_a, function_b)

    compound(ExecutionContext[Dict, Dict](environment={"a": 1}, payload={"x": 2}))

    function_a_calls = function_a.mock_calls
    function_b_calls = function_b.mock_calls

    assert function_a_calls == [
        call(ExecutionContext(environment={"a": 1}, payload={"x": 2}, issues=[])),
    ]
    assert function_b_calls == [
        call(ExecutionContext(environment={"a": 1}, payload={"x": 3}, issues=[]))
    ]


def test_bind_all():
    function_a = MagicMock()
    function_a.side_effect = lambda context: ExecutionContext[Dict, Dict](
        environment=context.environment, payload={"x": 3}
    )
    function_b = MagicMock()

    compound = bind_all([function_a, function_b])

    compound(ExecutionContext[Dict, Dict](environment={"a": 1}, payload={"x": 2}))

    function_a_calls = function_a.mock_calls
    function_b_calls = function_b.mock_calls

    assert function_a_calls == [
        call(ExecutionContext(environment={"a": 1}, payload={"x": 2}, issues=[])),
    ]
    assert function_b_calls == [
        call(ExecutionContext(environment={"a": 1}, payload={"x": 3}, issues=[]))
    ]
