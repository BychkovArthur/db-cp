"""smth

Revision ID: 778724678cd0
Revises: 
Create Date: 2024-12-14 09:20:25.327769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '778724678cd0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('battle_type',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_battle_type_id'), 'battle_type', ['id'], unique=False)
    op.create_table('card',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('type', sa.Text(), nullable=False),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_card_id'), 'card', ['id'], unique=False)
    op.create_table('clan',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('tag', sa.Text(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_clan_id'), 'clan', ['id'], unique=False)
    op.create_table('user_detailed_info',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('crowns', sa.Integer(), nullable=False),
    sa.Column('max_crowns', sa.Integer(), nullable=False),
    sa.Column('clan_id', sa.Integer(), nullable=True),
    sa.Column('updated_ts', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['clan_id'], ['clan.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_detailed_info_id'), 'user_detailed_info', ['id'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('tag', sa.Text(), nullable=False),
    sa.Column('is_super_user', sa.Boolean(), nullable=False),
    sa.Column('user_detailed_info_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_detailed_info_id'], ['user_detailed_info.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_table('subscribe',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id1', sa.Integer(), nullable=False),
    sa.Column('user_id2', sa.Integer(), nullable=False),
    sa.Column('battle_type_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['battle_type_id'], ['battle_type.id'], ),
    sa.ForeignKeyConstraint(['user_id1'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_id2'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subscribe_id'), 'subscribe', ['id'], unique=False)
    op.create_table('battle_record',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('subscribe_id', sa.Integer(), nullable=False),
    sa.Column('user1_score', sa.Integer(), nullable=False),
    sa.Column('user2_score', sa.Integer(), nullable=False),
    sa.Column('user1_get_crowns', sa.Integer(), nullable=False),
    sa.Column('user2_get_crowns', sa.Integer(), nullable=False),
    sa.Column('user1_card_ids', sa.ARRAY(sa.Integer()), nullable=False),
    sa.Column('user2_card_ids', sa.ARRAY(sa.Integer()), nullable=False),
    sa.Column('replay', sa.Text(), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.Column('winner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['subscribe_id'], ['subscribe.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['winner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_battle_record_id'), 'battle_record', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_battle_record_id'), table_name='battle_record')
    op.drop_table('battle_record')
    op.drop_index(op.f('ix_subscribe_id'), table_name='subscribe')
    op.drop_table('subscribe')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_user_detailed_info_id'), table_name='user_detailed_info')
    op.drop_table('user_detailed_info')
    op.drop_index(op.f('ix_clan_id'), table_name='clan')
    op.drop_table('clan')
    op.drop_index(op.f('ix_card_id'), table_name='card')
    op.drop_table('card')
    op.drop_index(op.f('ix_battle_type_id'), table_name='battle_type')
    op.drop_table('battle_type')
    # ### end Alembic commands ###
