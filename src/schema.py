from typing import List, Union, Optional
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

# Spaced Repetition System

class User(BaseModel):
    name: str = Field(...)


class UserAttempt(BaseModel):
    user_id: str = Field(...)
    problem_id: str = Field(...)
    attempt_date: datetime = Field(default_factory=lambda: datetime.now())
    was_correct: bool = Field(...)


class Problem(BaseModel):
    problem_set_id: str = Field(...),
    problem_type: str = Field(...)



class ShortAnswerProblem(Problem):
    question: str
    answer: str
    prompt: str


class SpellingProblem(Problem):
    word: str
    example_usage: str


class MathProblem(Problem):
    equation: str
    answer: str


class DefinitionProblem(Problem):
    word: str
    definition: str


class ProblemType(Enum):
    # ANY = "any"
    SPELLING = "spelling"
    MATH = "math"
    SHORT_ANSWER = "short_answer"
    DEFINITION = "definition"


class ProblemSet(BaseModel):
    user_id: str = Field(...)
    title: str = Field(...)
    description: str = Field(...)
    type: Optional[str] = None  # Enum field set to optional
    # type: Optional[ProblemType] = None  # Enum field set to optional

    # problems: List[Union[ShortAnswerProblem, SpellingProblem, MathProblem, DefinitionProblem]] = []
