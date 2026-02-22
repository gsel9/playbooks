"""
Tool handling including function-call processing and constructing tool definitions.
"""

import json
from typing import Any

from openai.types.responses.response_input_param import (
    FunctionCallOutput,
    ResponseInputParam,
)

from ticketing import submit_support_ticket


def build_code_interpreter_tool():
    pass 


def build_function_tool():
    pass 


def process_function_calls(response: Any, openai_client: Any, agent: Any) -> Any:
    """
    Inspect agent response for tool calls, execute them, and feed results back.
    """
    outputs: ResponseInputParam = []

    for item in response.output:
        if item.type != "function_call":
            continue

        if item.name == "submit_support_ticket":
            result = submit_support_ticket(**json.loads(item.arguments))

            outputs.append(
                FunctionCallOutput(
                    type="function_call_output",
                    call_id=item.call_id,
                    output=result,
                )
            )

    if outputs:
        return openai_client.responses.create(
            input=outputs,
            previous_response_id=response.id,
            extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
        )

    return response


def recent_snowfall(location: str) -> str:
    """
    Fetches recent snowfall totals for a given location.
    :param location: The city name.
    :return: Snowfall details as a JSON string.
    """
    mock_snow_data = {"Seattle": "0 inches", "Denver": "2 inches"}
    snow = mock_snow_data.get(location, "Data not available.")
    return json.dumps({"location": location, "snowfall": snow})


###########################
########   NOTE   #########
###########################
# -> Alternative approach to define a multi-tool agent
# -> Code:
#
#
#user_functions: Set[Callable[..., Any]] = {
#    recent_snowfall, process_function_calls
#}
#
#functions = FunctionTool(user_functions)
#toolset = ToolSet()
#toolset.add(functions)
#agent_client.enable_auto_function_calls(toolset=toolset)
#
#agent = agent_client.create_agent(
#    model="gpt-4o-mini",
#    name="agent",
#    instructions="You are a helpful assistant. Use the provided functions to answer questions.",
#    toolset=toolset
#)
#