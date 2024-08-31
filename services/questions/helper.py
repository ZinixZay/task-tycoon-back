from dtos import CreateQuestion
from models import UserModel, QuestionModel, TaskModel


def question_dto_to_model(question: CreateQuestion, task_entity: TaskModel) -> QuestionModel:
    question_data = question.model_dump()
    question_data["task_id"] = task_entity.id
    question_data["type"] = question_data["type"].value
    question_model = QuestionModel(**question_data)
    return question_model