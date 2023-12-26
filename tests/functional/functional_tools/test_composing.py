from typing import Dict, Generator
from unittest.mock import MagicMock, call


from functional.functional_tools.composing import (
    ExecutionContext,
    Issue,
    IssueType,
    ItemProcessingContext,
    ItemProcessingResult,
    QueueExecutionContext,
    StreamExecutionContext,
    bind,
    bind_all,
    bind_stream_all,
    stream_processing,
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


ExampleItemProcessingResult = ItemProcessingResult[str]
ExampleStreamExecutionContext = StreamExecutionContext[
    Dict, ExampleItemProcessingResult
]


def test_bind_stream():
    def data_source() -> Generator[str, None, None]:
        return (str(100 + item) for item in range(10))

    def source_step(
        context: ExampleStreamExecutionContext,
    ) -> ExampleStreamExecutionContext:
        return ExampleStreamExecutionContext(
            environment=context.environment,
            stream=(
                ItemProcessingResult(item=element, issues=[])
                for element in data_source()
            ),
        )

    def process_step(
        context: ExampleStreamExecutionContext,
    ) -> ExampleStreamExecutionContext:
        return ExampleStreamExecutionContext(
            environment=context.environment,
            stream=(
                ExampleItemProcessingResult(
                    item=f"**{element.item}**", issues=element.issues
                )
                for element in context.stream or []
            ),
        )

    def filter_step(
        context: ExampleStreamExecutionContext,
    ) -> ExampleStreamExecutionContext:
        return ExampleStreamExecutionContext(
            environment=context.environment,
            stream=(
                ExampleItemProcessingResult(
                    item=element.item,
                    issues=element.issues + []
                    if "7" not in element.item
                    else [
                        Issue(
                            issue_type=IssueType.ERROR,
                            message=f"Discarded: {element.item}",
                        )
                    ],
                )
                for element in context.stream or []
            ),
        )

    compound = bind_stream_all([source_step, filter_step, process_step])

    result = compound(StreamExecutionContext(environment={}))

    assert list(result.stream or []) == [
        ItemProcessingResult(item="**100**", issues=[]),
        ItemProcessingResult(item="**101**", issues=[]),
        ItemProcessingResult(item="**102**", issues=[]),
        ItemProcessingResult(item="**103**", issues=[]),
        ItemProcessingResult(item="**104**", issues=[]),
        ItemProcessingResult(item="**105**", issues=[]),
        ItemProcessingResult(item="**106**", issues=[]),
        ItemProcessingResult(
            item="**107**",
            issues=[Issue(issue_type=IssueType.ERROR, message="Discarded: 107")],
        ),
        ItemProcessingResult(item="**108**", issues=[]),
        ItemProcessingResult(item="**109**", issues=[]),
    ]


def test_stream_processing():
    def data_source() -> Generator[ItemProcessingContext, None, None]:
        return (
            ItemProcessingContext[Dict, str](
                item=str(100 + item), issues=[], environment={}
            )
            for item in range(10)
        )

    def item_processor(
        item_processing_context: ItemProcessingContext,
    ) -> ItemProcessingContext:
        result_context = ItemProcessingContext(
            environment=item_processing_context.environment,
            item=f"==>{item_processing_context.item}<==",
            issues=item_processing_context.issues,
        )
        print(f"{item_processing_context.item} ==> {result_context.item}")
        return result_context

    strt_context = QueueExecutionContext[Dict, ItemProcessingContext](environment={})
    context = stream_processing(
        context=strt_context, source=data_source(), item_processor=item_processor
    )

    print(context)
