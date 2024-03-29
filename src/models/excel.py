from dataclasses import dataclass
from typing import Union

from .test import TestAnswerValue, TestAnswerType


@dataclass
class WrittenTestStudentAnswer:
    value: TestAnswerValue
    mark: Union[float, None]

@dataclass
class WrittenTestQuestionData:
    question: str
    answer: TestAnswerValue
    max_mark: float
    type: TestAnswerType

@dataclass
class WrittenTestStudentData:
    name: str
    group: str
    id: int
    answers: list[WrittenTestStudentAnswer]

@dataclass
class WrittenTestVariantSheet:
    name: str
    questions: list[WrittenTestQuestionData]
    students: list[WrittenTestStudentData]

@dataclass
class WrittenTestGroup:
    group: str
    students: list[WrittenTestStudentData]

@dataclass
class WrittenTestSummarySheet:
    groups: list[WrittenTestGroup]

@dataclass
class WrittenTestExcel:
    name: str
    date: str
    variants: list[WrittenTestVariantSheet]
    summary: WrittenTestSummarySheet

@dataclass
class UpdatedStudentData:
    name: str
    marks: list[Union[float, None]]

@dataclass
class UpdatedTestExcel:
    name: str
    date: str
    students: list[UpdatedStudentData]

