from dotenv import load_dotenv
from openai import OpenAI
import os

class TestOpenAIResponse():
    """
    A class for testing OpenAI's API response.

    NOTE: NOT FOR PRODUCTION USE

    In production:
    - The `generate_response` method should be called from a separate thread to avoid blocking the main thread?
    - The `conversation_history` should be stored in a database.
    - Conversation history needs to be managed per user.
    
    """
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4-1106-preview" # gpt-3.5-turbo-1106
        self.summarizer_model = "gpt-3.5-turbo-1106"
        self.conversation_history = []
        self.summary = ""
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
- If the player opts for none of the presented options, generate a response that reflects their decision, emphasizing an alteration of the timeline.
- If this is a humorous option, ensure that the system response is also humorous balances the tone of it with the game.

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

### Using Summary
In 'Immemoria', the summary serves as your long-term memory, capturing key developments and player decisions that shape the game's evolving world. It provides a succinct narrative overview, enabling you to maintain consistency and coherence in responses. Use the summary alongside the conversation history, which acts as short-term memory, to guide immediate responses and anticipate future story paths. This combination ensures a seamless and dynamic player experience in 'Immemoria', where each choice profoundly influences the ongoing narrative.
"""

    def generate_response(self, prompt):
        """
        Generates a response from OpenAI's API.

        Parameters:
            prompt (str): The prompt to generate a response from.        
        """
        # Construct a system role string with both `self.system_role` and `self.conversation_history`
        system_role = self.system_role
        # Add a label for the summary
        system_role += "\n\n### Summary:\n"
        # Add the summary
        system_role += self.summary
        # Add a label for the conversation history
        system_role += "\n\n### Conversation History:\n"
        for entry in self.conversation_history:
            system_role += f"---\n#### Prompt:\n{entry['prompt']}\n#### Response:\n{entry['response']}\n"

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

    def add_to_summary(self, prompt, response):
        """
        Adds detail about the current interaction to the summary

        Takes in a prompt and response, sends them to the OpenAI API with the
        current summary, and returns the new summary.

        The summary should never exceed two paragraphs.
        """

        current_interaction = f"#### Prompt: {prompt}\n\n#### Response: {response}"

        summarize_system_prompt = f"""
You are an AI summarizer for 'Immemoria', a text-based RPG where player choices shape an ever-changing world themed around memory, time-fluidity, and reality alteration. The player, assuming the role of an unnamed protagonist, explores various time periods and interacts with diverse NPCs, whose memories influence their knowledge and interactions. The game balances exploration, narrative progression, and combat encounters, offering scenarios with three types of actions: Order, Chaos, and Neutral, each having distinct impacts on the game world.

Based on the interaction that the user will provide, summarize the current state of the game, highlighting how the player's decision aligns with the game's themes and influences the narrative. Keep the summary concise, fitting within only TWO PARAGRAPHS, and ensure it captures the essence of the recent developments and the potential implications for future interactions in the game world.
"""

        try:
            response = self.client.chat.completions.create(
                model=self.summarizer_model,
                messages=[
                    {"role": "system", "content": summarize_system_prompt},
                    {"role": "user", "content": current_interaction}
                ],
                max_tokens=1000
            )
            self.summary = response.choices[0].message.content
        except Exception as e:
            print(f"Encountered an error while generating response: {e}")
            return None


    def clear_conversation_history(self):
        """Clears the conversation history."""
        self.conversation_history = []
