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
    problem_set_id: str = Field(...)
    problem_type: str = Field(...)


class ShortAnswerProblem(Problem):
    question: str = Field(...)
    answer: str = Field(...)
    prompt: str = Field(...)


class SpellingProblem(Problem):
    word: str = Field(...)
    example_usage: str


class MathProblem(Problem):
    equation: str = Field(...)
    answer: str = Field(...)


class DefinitionProblem(Problem):
    word: str = Field(...)
    definition: str = Field(...)
    prompt: str = Field(...)


class MultipleChoiceProblem(Problem):
    question: str = Field(...)
    choices: List[str] = Field(...)
    answer: int = Field(...) # index of the correct answer


class ProblemType(Enum):
    # ANY = "any"
    SPELLING = "spelling"
    MATH = "math"
    SHORT_ANSWER = "short_answer"
    DEFINITION = "definition"
    MULTIPLE_CHOICE = "multiple_choice"


class ProblemSet(BaseModel):
    user_id: str = Field(...)
    title: str = Field(...)
    description: str = Field(...)
    type: Optional[str] = None  # Enum field set to optional
    # type: Optional[ProblemType] = None  # Enum field set to optional


class TestSet(BaseModel):
    user_ids: List[str] = Field(...) # list of users who can access this test set
    title: str = Field(...)
    description: str = Field(...)
    problem_ids: List[str] = Field(...)
