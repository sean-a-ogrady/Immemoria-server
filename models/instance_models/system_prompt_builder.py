# NOTE: DEPRECATED
class SystemPromptBuilder:
    def __init__(self, system_role: str = "", directions: str = "", context: list = [], max_chat_context_length: int = 5, additional_instructions: str = ""):
        # Initialize variables to store different parts of the prompt
        self.system_role = system_role
        self.directions = directions
        self.context = context
        self.max_chat_context_length = max_chat_context_length
        self.additional_instructions = additional_instructions
        # self.max_context_length = 2048

    def set_system_role(self, role):
        """Set the system's role for the prompt."""
        self.system_role = role

    def set_directions(self, directions):
        """set directions or instructions to the prompt."""
        self.directions = directions

    def add_context(self, system_message: str, user_message: str):
        """Add context to the end of the context list and remove the first element if the list is too long."""
        # Label the system and user messages
        system_message = f"System: {system_message}"
        user_message = f"User: {user_message}"
        # Combine the messages into a single string
        context = f"{system_message}\n{user_message}"
        # Add the context to the end of the context list
        self.context.append(context)
        # Remove the first element if the context list is too long
        if len(self.context) > self.max_chat_context_length:
            self.context.pop(0)

    def add_additional_instructions(self, additional_instructions: str):
        """Add additional instructions to the prompt."""
        self.additional_instructions = additional_instructions

    def set_max_chat_context_length(self, max_chat_context_length: int):
        """Set the maximum length of the chat context."""
        self.max_chat_context_length = max_chat_context_length

    def build_prompt(self):
        """Build the prompt from the different parts."""
        # Combine the context list into a single string
        context = "\n".join(self.context)
        # Delimit the context with a title
        context = f"Chat Context:\n{context}"
        # Combine the different parts of the prompt into a single string
        prompt = f"{self.system_role}\n\n{self.directions}\n\n{context}\n\n{self.additional_instructions}"
        return prompt

    def build_default_prompt(self):
        """Build the default prompt."""
        # Combine the context list into a single string
        context = "\n".join(self.context)
        # Default system role string
        system_role = "System: Welcome to Immemoria! This is a test of the system prompt builder."
        # Default directions string
        directions = "Directions: Please respond to the system's messages with a short message of your own."
        # Default additional instructions string
        additional_instructions = "Additional Instructions: This is a test of the system prompt builder."
        # Combine the different parts of the prompt into a single string
        prompt = f"{system_role}\n\n{directions}\n\n{context}\n\n{additional_instructions}"