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

from enum import Enum
import peewee as pw
from peewee_migrate import Migrator

class UserRolesEnum(Enum):
    PUPIL = 'pupil'
    TEACHER = 'teacher'


class TableNamesEnum(Enum):
    USER_ENTITY = 'users'
    TASK_QUESTIONS_ENTITY = 'task_questions'
    TASK_FILES_ENTITY = 'task_files'
    TASK_ENTITY = 'tasks'
    ANSWER_ENTITY = 'answers'
    ATTEMPT_ENTITY = 'attempts'
    GROUP_ENTITY = 'groups'
    GROUP_FILES_ENTITY = 'group_files'
    GROUP_PERMISSIONS_ENTITY = 'group_permissions'
    GROUP_TASKS_ENTITY = 'group_tasks'
    QUESTION_ENTITY = 'questions'
    QUESTION_FILES_ENTITY = 'question_files'
    QUESTION_HINTS_ENTITY = 'question_hints'


def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    permissions_str: str = '0' * 128

    migrator.sql(f'''
    CREATE TABLE {TableNamesEnum.USER_ENTITY.value} (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        email VARCHAR(62) UNIQUE NOT NULL,
        hashed_password VARCHAR(1024) NOT NULL,
        nickname VARCHAR(62),
        name VARCHAR(50),
        surname VARCHAR(50),
        role VARCHAR(50) DEFAULT '{UserRolesEnum.PUPIL.value}',
        created_at BIGINT DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000),
        is_active BOOLEAN DEFAULT FALSE,
        is_superuser BOOLEAN DEFAULT FALSE,
        is_verified BOOLEAN DEFAULT FALSE
    );
''')
    migrator.sql(f'''
    CREATE TABLE {TableNamesEnum.GROUP_ENTITY.value} (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        user_id UUID REFERENCES {TableNamesEnum.USER_ENTITY.value}(id) ON DELETE CASCADE,
        title VARCHAR(256) NOT NULL,
        type VARCHAR(256) NOT NULL,
        parent_id UUID,
        price SMALLINT,
        created_at BIGINT DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)
    );''')
    migrator.sql(f'''
    CREATE TABLE {TableNamesEnum.TASK_ENTITY.value} (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        user_id UUID REFERENCES {TableNamesEnum.USER_ENTITY.value}(id) ON DELETE CASCADE,
        title VARCHAR(256) NOT NULL,
        description_full TEXT,
        description_short VARCHAR(2048),
        created_at BIGINT DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)
);''')
    migrator.sql(f'''
                 CREATE TABLE {TableNamesEnum.TASK_FILES_ENTITY.value} (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID REFERENCES {TableNamesEnum.TASK_ENTITY.value}(id) ON DELETE CASCADE,
    file_path VARCHAR(1024) NOT NULL
);''')
    migrator.sql(f'''CREATE TABLE {TableNamesEnum.GROUP_FILES_ENTITY.value} (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    group_id UUID REFERENCES {TableNamesEnum.GROUP_ENTITY.value}(id) ON DELETE CASCADE,
    file_path VARCHAR(1024) NOT NULL
);''')
    migrator.sql(f'''
    CREATE TABLE {TableNamesEnum.GROUP_PERMISSIONS_ENTITY.value} (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        user_id UUID REFERENCES {TableNamesEnum.USER_ENTITY.value}(id) ON DELETE CASCADE,
        group_id UUID REFERENCES {TableNamesEnum.GROUP_ENTITY.value}(id) ON DELETE CASCADE,
        permissions VARCHAR(128) DEFAULT '{permissions_str}' NOT NULL
);
''')
    migrator.sql(f'''
CREATE TABLE {TableNamesEnum.GROUP_TASKS_ENTITY.value} (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    group_id UUID REFERENCES {TableNamesEnum.GROUP_ENTITY.value}(id) ON DELETE CASCADE,
    task_id UUID REFERENCES {TableNamesEnum.TASK_ENTITY.value}(id) ON DELETE CASCADE,
    attempts_count SMALLINT DEFAULT 3,
    execution_time SMALLINT DEFAULT 3600,
    expires_on BIGINT,
    is_educational BOOLEAN DEFAULT FALSE,
    created_at BIGINT DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)
);''')
    migrator.sql(f"""CREATE TABLE {TableNamesEnum.ATTEMPT_ENTITY.value} (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID REFERENCES {TableNamesEnum.GROUP_TASKS_ENTITY.value}(id) ON DELETE CASCADE,
    user_id UUID REFERENCES {TableNamesEnum.USER_ENTITY.value}(id) ON DELETE CASCADE,
    result SMALLINT DEFAULT 0,
    stats JSONB DEFAULT '{{}}'::jsonb,
    content JSONB DEFAULT '{{}}'::jsonb,
    created_at BIGINT DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000),
    is_expired BOOLEAN DEFAULT FALSE
);
""")
    migrator.sql(f'''CREATE TABLE {TableNamesEnum.QUESTION_ENTITY.value} (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES {TableNamesEnum.USER_ENTITY.value}(id) ON DELETE CASCADE,
    question_body VARCHAR(1024) NOT NULL,
    type VARCHAR NOT NULL,
    content JSONB DEFAULT '[]',
    created_at BIGINT DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000) NOT NULL
);
''')
    migrator.sql(f'''CREATE TABLE {TableNamesEnum.TASK_QUESTIONS_ENTITY.value} (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID REFERENCES {TableNamesEnum.TASK_ENTITY.value}(id) ON DELETE CASCADE,
    question_id UUID REFERENCES {TableNamesEnum.QUESTION_ENTITY.value}(id) ON DELETE CASCADE,
    "order" SMALLINT NOT NULL,
    cost SMALLINT DEFAULT 1,
    created_at BIGINT DEFAULT (EXTRACT(EPOCH FROM NOW()) * 1000)
);''')
    migrator.sql(f'''CREATE TABLE {TableNamesEnum.ANSWER_ENTITY.value} (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    attempt_id UUID REFERENCES {TableNamesEnum.ATTEMPT_ENTITY.value}(id) ON DELETE CASCADE,
    question_id UUID REFERENCES {TableNamesEnum.QUESTION_ENTITY.value}(id) ON DELETE CASCADE,
    status VARCHAR NOT NULL,
    content JSONB DEFAULT '{{}}'::jsonb
);''')
    migrator.sql(f'''CREATE TABLE {TableNamesEnum.QUESTION_FILES_ENTITY.value} (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question_id UUID REFERENCES {TableNamesEnum.QUESTION_ENTITY.value}(id) ON DELETE CASCADE,
    file_path VARCHAR(1024) NOT NULL
);''')
    migrator.sql(f'''CREATE TABLE {TableNamesEnum.QUESTION_HINTS_ENTITY.value} (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question_id UUID REFERENCES {TableNamesEnum.QUESTION_ENTITY.value}(id) ON DELETE CASCADE,
    message VARCHAR(512) NOT NULL,
    "order" SMALLINT
);
''')



def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your rollback migrations here."""
    migrator.sql(f'''DROP TABLE {TableNamesEnum.QUESTION_HINTS_ENTITY.value}''')
    migrator.sql(f'''DROP TABLE {TableNamesEnum.QUESTION_FILES_ENTITY.value}''')
    migrator.sql(f'''DROP TABLE {TableNamesEnum.ANSWER_ENTITY.value}''')
    migrator.sql(f'''DROP TABLE {TableNamesEnum.TASK_QUESTIONS_ENTITY.value}''')
    migrator.sql(f'''DROP TABLE {TableNamesEnum.QUESTION_ENTITY.value}''')
    migrator.sql(f'''DROP TABLE {TableNamesEnum.ATTEMPT_ENTITY.value}''')
    migrator.sql(f'''DROP TABLE {TableNamesEnum.GROUP_TASKS_ENTITY.value}''')
    migrator.sql(f'''DROP TABLE {TableNamesEnum.GROUP_PERMISSIONS_ENTITY.value}''')
    migrator.sql(f'''DROP TABLE {TableNamesEnum.GROUP_FILES_ENTITY.value}''')
    migrator.sql(f'''DROP TABLE {TableNamesEnum.TASK_FILES_ENTITY.value}''')
    migrator.sql(f'''DROP TABLE {TableNamesEnum.TASK_ENTITY.value}''')
    migrator.sql(f'''DROP TABLE {TableNamesEnum.GROUP_ENTITY.value}''')
    migrator.sql(f'''DROP TABLE {TableNamesEnum.USER_ENTITY.value}''')
