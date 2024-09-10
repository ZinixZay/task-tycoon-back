from typing import List

from dtos.questions import CreateQuestion
from models import QuestionModel, TaskModel


def question_dto_to_model(questions: List[CreateQuestion], task_model: TaskModel) -> List[QuestionModel]:
    question_models: List[QuestionModel] = list()
    for question_schema in questions:
        question_data: dict = question_schema.model_dump()
        question_data["task_id"] = task_model.id
        question_data["type"] = question_data["type"].value
        question_model: QuestionModel = QuestionModel(**question_data)
        question_models.append(question_model)
    return question_models
