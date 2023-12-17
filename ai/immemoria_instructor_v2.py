from openai import OpenAI
from instructor import patch, OpenAISchema
from pydantic import Field
import os
from dotenv import load_dotenv
from ai.system_prompt_builder import SystemPromptBuilder

##################################
############ SCHEMA ##############
##################################

"""
Rather than hoping the correctly structured data is in the response, this script takes a fully structured approach to prompting.
OpenAI's JSON mode is unreliable, necessitating the use of the `instructor` library with `pydantic`.
Using vanilla OpenAI API with function calling and JSON mode, the prompting structure is `(prompt: str, schema: dict) -> str`
The above implementation doesn't guarantee that the desired data is in the response object.
A far more reliable approach is `(prompt: str, schema: Model) -> Model`, allowing for validation of fields.
"""

# NOTE: All content within the schema gets sent to OpenAI's API.
# NOTE: The schema should only contain information that is relevant to the prompt, and nothing else.
# NOTE: The docstrings, attributes, types, and field descriptions are all of equal importance for the prompt.


# Sub-schema for player options
class PlayerOptions(OpenAISchema):
    """
Player options for a scenario in Immemoria.
One action should be Order, one should be Chaos, and one should be Neutral.
    """
    order: str = Field(..., description="Order action option for the player.")
    chaos: str = Field(..., description="Chaos action option for the player.")
    neutral: str = Field(..., description="Neutral action option for the player.")


# Main response schema
class Scenario(OpenAISchema):
    """
Defines a scenario in the game Immemoria, including the description, player options, and a summary.
Each `Scenario` is no more than 3 sentences.
Each `Scenario` has 3 potential `PlayerOptions` in each scenario.
The summary is a succinct long-term narrative overview, capturing key developments and player decisions.
    """
    description: str = Field(..., description="Three-sentence description of the current scenario in Immemoria.")
    actions: PlayerOptions = Field(..., description="Options available to the player in the scenario.")
    summary: str = Field(..., description="One-sentence summary of the player's action and its result.")


##################################
######### Main AI Class ##########
##################################

class ImmemoriaAI():
    """
    A class for generating responses for Immemoria.
    """
    def __init__(self):
        self.model = "gpt-4-1106-preview" # gpt-3.5-turbo-1106
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.client = patch(self.client)
        
    def generate_response(self, player_prompt: str, conversation_history: list, summary: list):
        system_prompt = SystemPromptBuilder.construct_default_gameplay_loop_prompt(conversation_history, summary)
        # Send request to OpenAI with structured system prompt and response model
        response: Scenario = self.client.chat.completions.create(
            model="gpt-4-1106-preview",
            response_model=Scenario,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": player_prompt},
            ],
        )
        return response # .model_dump_json()
