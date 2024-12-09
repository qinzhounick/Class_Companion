import openai

class Prompter:
    def __init__(self, condensed_transcript = ""):
        self.messages = [{"role": "user", "content": "Condensed Transcript: " + condensed_transcript}]
        self.client = openai.OpenAI(api_key=openai.api_key)

        self.model_thought = ""

    
    def append(self, content): 
        content = "provide a 10 word or less summary of the following content, given the condensed transcript: " + content
        self.messages.append({"role": "user", "content": content})

        self.summary = self.prompt()
        self.messages[0]['content'] += self.summary
        return self.summary 

    def ask(self, content):
        self.messages.append({"role":"user", "content": content})
        resp = self.prompt() 
        return resp 

    def get_model_thought(self):
        ## what we want 
        pass 

    def prompt(self, messages=None):
        if messages:
            self.messages = messages
        else: 
            self.messages = [self.messages[0], self.messages[-1]] # may introduce concurrency issues. condensed summary + recentmost prompt.
        completion = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=self.messages
        )
        assistant_response = completion.choices[0].message.content
        return assistant_response
    