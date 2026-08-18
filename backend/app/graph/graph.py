# build_graph() – wires nodes + conditional edges
from langgraph.graph import StateGraph, END
from app.graph.nodes.research_node import research_node
from app.graph.nodes.deduplication_node import deduplication_node
from app.graph.nodes.ranking_node import ranking_node
from app.graph.nodes.summary_node import summary_node
from app.graph.nodes.image_prompt_node import image_prompt_node
from app.graph.nodes.validate_node import validate_node
from app.graph.state import NewsState


def build_news_graph():
    workflow = StateGraph(NewsState)

    workflow.add_node("research", research_node)
    workflow.add_node("deduplicate", deduplication_node)
    workflow.add_node("rank", ranking_node)          # YOUR original – unchanged
    workflow.add_node("summary", summary_node)
    workflow.add_node("image_prompt", image_prompt_node)
    workflow.add_node("validate", validate_node)

    workflow.set_entry_point("research")
    workflow.add_edge("research", "deduplicate")
    workflow.add_edge("deduplicate", "rank")
    workflow.add_edge("rank", "summary")
    workflow.add_edge("summary", "image_prompt")
    workflow.add_edge("image_prompt", "validate")

    def route_after_validate(state):
        if state.get("should_retry", False):
            return "summary"
        else:
            return END

    workflow.add_conditional_edges(
        "validate",
        route_after_validate,
        {
            "summary": "summary",
            END: END
        }
    )

    return workflow.compile()


def get_graph():
    return build_news_graph()