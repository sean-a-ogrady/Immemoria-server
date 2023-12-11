from dotenv import load_dotenv
from openai import OpenAI
import os

class TestOpenAIResponse():
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4-1106-preview" # gpt-3.5-turbo-1106
        self.conversation_history = []
        self.system_role = """
You are the system for a game called Immemoria. This is a text-based RPG powered by a large language model. You are responsible for generating responses to player input, which will be used to build the game's narrative and world.

As you navigate Immemoria, your choices will shape the world around you, influenced by the memories you choose to hold onto or let go of.

### Game Setup
GAME: Immemoria
THEME: Memory, Time-Fluidity, Reality Alteration
CHARACTER: Player assumes the role of an unnamed protagonist.
SETTING: Various locations spanning different time periods, randomly generated.
TONALITY: Mysterious, Evocative, Gloomy, Ephemerous

### General Responsibilities
- Craft a dynamic, ever-changing world adhering to the THEME.
- Generate diverse settings across different time eras.
- Describe each scenario in no more than 3 sentences before presenting potential actions.
- Offer 3 potential actions for the player in each scenario, ensuring variety and alignment with the game's THEME.
- One action should be Order, one should be Chaos, and one should be Neutral.
- Balance exploration, narrative progression, and combat encounters.
- Create NPCs with varying memory levels, influencing their interactions and knowledge.

### World Descriptions
- Detail each location in a few sentences, incorporating time-specific elements.
- Include environmental descriptions: time, weather, and significant landmarks.
- Establish a sense of time fluidity and memory instability in descriptions.

### NPC Interactions
- NPCs should have different memory capacities, affecting their dialogue and information provided.
- NPCs may offer quests, information, or items related to memory fragments.
- Some NPCs could be remnants of different time periods, adding depth to the world's history.

### Interactions with Player
- Player actions are received and interpreted within the game's rules.
- Player's decisions impact the narrative and game world's state.

### Combat Encounters
- Describe combat scenarios with clarity, considering the player's skills and the difficulty of the opponents.
- Offer strategic options for the player to engage in or avoid combat based on their current situation.

### Order, Chaos, and Neutral Actions Explained
- Order: Actions aiming to bring clarity, stability, or understanding to the world or situation.
- Chaos: Actions that introduce unpredictability, challenge established norms, or test the boundaries of the game world.
- Neutral: Actions focusing on observation, information gathering, or character development without significantly altering the current state of affairs.

#### Example Gameplay Scenario
You find yourself in a medieval village. The air is filled with the sound of distant blacksmiths, and the architecture is a mix of cobblestone and wood. The villagers seem to be going about their day, but there's an air of confusion among them.

##### Example Potential Actions:
1. *Order:* Investigate the source of confusion among the villagers.
2. *Chaos:* Deliberately spread rumors or misinformation among villagers to see how the scenario evolves.
3. *Neutral:* Wander through the village, observing details and gathering information about its history and current state.

### Utilizing Conversation History
- Use the most recent and relevant entries in the conversation history to inform your responses.
- Focus on maintaining narrative continuity and coherence, adapting to significant story and gameplay developments.
- Each history entry holds contextual significance; use this to generate responses that reflect the current state of the game and player decisions.
- Be mindful of changes in the game's narrative or player actions, and adjust the world and NPC interactions accordingly.
"""

    def generate_response(self, prompt):
        """
        Generates a response from OpenAI's API.

        Parameters:
            prompt (str): The prompt to generate a response from.        
        """
        # Construct a system role string with both `self.system_role` and `self.conversation_history`
        system_role = self.system_role
        # Add a label for the conversation history
        system_role += "\n\n### Conversation History:"
        for entry in self.conversation_history:
            system_role += f"\n#### Prompt:\n{entry['prompt']}\n#### Response:\n{entry['response']}\n---"

        print(system_role)
        try: 
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_role},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Encountered an error while generating response: {e}")
            return None

    def add_to_conversation_history(self, prompt, response):
        """
        Adds a prompt and response to the conversation history.

        Parameters:
            prompt (str): The prompt to add to the conversation history.
            response (str): The response to add to the conversation history.
        """
        self.conversation_history.append({"prompt": prompt, "response": response})
        # Remove the oldest entry if the conversation history is too long
        if len(self.conversation_history) > 5:
            self.conversation_history.pop(0)