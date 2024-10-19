"""Peewee migrations -- 002_default_users.py.

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
from enum import Enum
import time

from argon2 import PasswordHasher
import peewee as pw
from peewee_migrate import Migrator
from src.env.env_variables_enum import EnvVariablesEnum


HASHER = PasswordHasher()

class TableNamesEnum(Enum):
    USER_ENTITY = 'users'


def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your migrations here."""
    database.execute_sql(f'''INSERT INTO 
                                {TableNamesEnum.USER_ENTITY.value} 
                                    (id, email, hashed_password, role, created_at, is_active, is_superuser, is_verified)
                                VALUES
                                    (gen_random_uuid(), 
                                    '{EnvVariablesEnum.SUPERUSER_LOGIN.value}', 
                                    '{HASHER.hash(EnvVariablesEnum.SUPERUSER_PASSWORD.value)}',
                                    'teacher',
                                    {time.time()},
                                    true,
                                    true, 
                                    true)''')
    database.execute_sql(f'''INSERT INTO 
                                users 
                                    (id, email, hashed_password, role, created_at, is_active, is_superuser, is_verified)
                                VALUES
                                    (gen_random_uuid(), 
                                    '{EnvVariablesEnum.TEST_USER.value}', 
                                    '{HASHER.hash(EnvVariablesEnum.TEST_USER_PASSWORD.value)}',
                                    'pupil',
                                    {time.time()},
                                    true,
                                    true, 
                                    true)''')
    


def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your rollback migrations here."""
    database.execute_sql(f'''
                         DELETE FROM 
                            {TableNamesEnum.USER_ENTITY.value} 
                        WHERE 
                            email = '{EnvVariablesEnum.SUPERUSER_LOGIN.value}'
                        ''')
    database.execute_sql(f'''
                         DELETE FROM 
                            users 
                        WHERE 
                            email = '{EnvVariablesEnum.TEST_USER.value}'
                        ''')
    
