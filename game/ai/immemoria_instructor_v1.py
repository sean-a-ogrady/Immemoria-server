from openai import OpenAI
from instructor import patch, OpenAISchema
from pydantic import Field, field_validator
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

client = patch(client)

# Sub-schema for player options
class PlayerOptions(OpenAISchema):
    """
    Player options for a scenario
    """
    order: str = Field(..., description="Order option")
    chaos: str = Field(..., description="Chaos option")
    neutral: str = Field(..., description="Neutral option")

# Main response schema
class Scenario(OpenAISchema):
    """
    A scenario in the game Immemoria.
    """
    description: str = Field(..., description="Description of the scenario")
    actions: PlayerOptions = Field(..., description="Player options for the scenario")
    summary: str = Field(..., description="One-sentence summary of the scenario")

print(Scenario.openai_schema)

# scenario: Scenario = client.chat.completions.create(
#     model="gpt-4-1106-preview",
#     response_model=Scenario,

# )