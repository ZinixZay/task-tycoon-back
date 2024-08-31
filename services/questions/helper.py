from dtos import CreateQuestion
from models import QuestionModel, TaskModel


def question_dto_to_model(question: CreateQuestion, task_entity: TaskModel) -> QuestionModel:
    question_data: dict = question.model_dump()
    question_data["task_id"] = task_entity.id
    question_data["type"] = question_data["type"].value
    question_model: QuestionModel = QuestionModel(**question_data)
    return question_model