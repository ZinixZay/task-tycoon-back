"""Peewee migrations -- 001_init.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['table_name']            # Return model in current state by name
    > Model = migrator.ModelClass                   # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.run(func, *args, **kwargs)           # Run python function with the given args
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.add_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)
    > migrator.add_constraint(model, name, sql)
    > migrator.drop_index(model, *col_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.drop_constraints(model, *constraints)

"""

from contextlib import suppress

import peewee as pw
from peewee_migrate import Migrator
from importlib import import_module

entities = import_module('src.entity')


with suppress(ImportError):
    import playhouse.postgres_ext as pw_pext


def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your migrations here."""
    migrator.create_model(entities.User)
    migrator.create_model(entities.Group)
    migrator.create_model(entities.Task)
    migrator.create_model(entities.TaskFiles)
    migrator.create_model(entities.GroupFiles)
    migrator.create_model(entities.GroupPermission)
    migrator.create_model(entities.GroupTasks)
    migrator.create_model(entities.Attempt)
    migrator.create_model(entities.Question)
    migrator.create_model(entities.TaskQuestions)
    migrator.create_model(entities.Answer)
    migrator.create_model(entities.QuestionFiles)
    migrator.create_model(entities.QuestionHints)
    


def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your rollback migrations here."""
    migrator.drop_table(entities.QuestionHints)
    migrator.drop_table(entities.QuestionFiles)
    migrator.drop_table(entities.Answer)
    migrator.drop_table(entities.TaskQuestions)
    migrator.drop_table(entities.Question)
    migrator.drop_table(entities.Attempt)
    migrator.drop_table(entities.GroupTasks)
    migrator.drop_table(entities.GroupPermission)
    migrator.drop_table(entities.GroupFiles)
    migrator.drop_table(entities.TaskFiles)
    migrator.drop_table(entities.Task)
    migrator.drop_table(entities.Group)
    migrator.drop_table(entities.User)
    
