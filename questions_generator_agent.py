from pydantic import BaseModel, Field
from agents import Agent


INSTRUCTIONS = """Your are a helpful research assistant. You are given a research query that another assistant will use to search the web for relative information
Your jobs is to make 3 helpful questions based on the query given that they will be answered by the user that gave this query. 
These 3 questions and answers will be passed to the research assistant and will help and clarify better his job on searching relative information on the internet
You should only reply with the 3 questions"""

class Question(BaseModel):
    question: str = Field(description="A meaningful question based on the search query that the user gave, that its answer will help on the research")
 
class Questions(BaseModel):
    questions: list[Question] = Field(description="A list meaningful questions based on the search query that the user gave")
    
questions_generator_agent = Agent(
    name="Questions Generator Agent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=Questions,
)