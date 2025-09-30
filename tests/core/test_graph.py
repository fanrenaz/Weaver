from langchain_core.messages import HumanMessage
from langchain_core.language_models.fake import FakeListLLM
from weaver.core.graph import WeaverGraph
from weaver.models.state import SpaceState
from langchain_core.messages import AIMessage


class _DeterministicFake(FakeListLLM):
    """Fake LLM that always produces a fixed tool call structure."""

    def __init__(self):
        super().__init__(responses=["(fake) calling reply_privately tool"])

    def bind_tools(self, tools):
        return self

    def invoke(self, messages, **kwargs):  # return plain AI message (no tool call)
        return AIMessage(content=self.responses[0])


def test_graph_invoke_with_fake_llm():
    fake = _DeterministicFake()
    graph = WeaverGraph(system_prompt="SYSTEM", llm=fake)
    state: SpaceState = {"input": [HumanMessage(content="你好", additional_kwargs={"user_id": "u1"})]}
    result = graph.app.invoke(state)
    # The agent node should have appended an AI message
    msgs = result.get("input", [])
    assert any(getattr(m, "type", "") == "ai" for m in msgs)
    # No tool call produced by fake
    assert result.get("action_to_execute") in (None, [])
