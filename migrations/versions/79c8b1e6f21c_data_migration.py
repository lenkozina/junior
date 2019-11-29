"""data migration

Revision ID: 79c8b1e6f21c
Revises: 79c8b1e6f21d
Create Date: 2019-11-29 15:04:01.866710

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79c8b1e6f21c'
down_revision = '79c8b1e6f21d'
branch_labels = None
depends_on = None


def upgrade():
    t_answers = sa.Table(
        'answers',
        sa.MetaData(),
        sa.Column('id', sa.Integer()),
        sa.Column('created', sa.DateTime()),
        sa.Column('text', sa.Text()),
        sa.Column('likes_count', sa.Integer()),
    )
    connection = op.get_bind()
    results = connection.execute(sa.select([
        t_answers.c.id,
        t_answers.c.text,
    ])).fetchall()
    for id_, _ in results:
        connection.execute(t_answers.update().where(t_answers.c.id == id_).values(
            likes_count=0,
        ))


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
