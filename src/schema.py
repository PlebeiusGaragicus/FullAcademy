from typing import List, Union, Optional
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, EmailStr

# Spaced Repetition System

class User(BaseModel):
    name: str = Field(...)
    # email: EmailStr = Field(...)
    # password: str = Field(...)


class UserAttempt(BaseModel):
    user_id: str = Field(...)
    problem_id: str = Field(...)
    attempt_date: datetime = Field(default_factory=datetime.utcnow)
    was_correct: bool = Field(...)


class ShortAnswerProblem(BaseModel):
    question: str
    answer: str
    prompt: str  


class SpellingProblem(BaseModel):
    word: str
    example_usage: str


class MathProblem(BaseModel):
    equation: str
    answer: str


class DefinitionProblem(BaseModel):
    word: str
    definition: str


class ProblemType(Enum):
    # ANY = "any"
    SPELLING = "spelling"
    MATH = "math"
    SHORT_ANSWER = "short_answer"
    DEFINITION = "definition"


# Has a list of problems of different possible types
class ProblemSet(BaseModel):
    user_id: str = Field(...)
    title: str = Field(...)
    description: str = Field(...)
    # type: Optional[ProblemType] = None  # Enum field set to optional
    type: Optional[str] = None  # Enum field set to optional
    problems: List[Union[ShortAnswerProblem, SpellingProblem, MathProblem, DefinitionProblem]] = []
