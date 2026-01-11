"""Add user roles and job board models"""

from alembic import op
import sqlalchemy as sa


def upgrade():
    # Add role, name, avatar to users
    op.add_column('users', sa.Column('role', sa.Enum('job_seeker', 'employer', name='userrole'), nullable=False, server_default='job_seeker'))
    op.add_column('users', sa.Column('name', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('avatar', sa.String(500), nullable=True))

    # Create jobs table
    op.create_table('jobs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('company', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('location', sa.String(255), nullable=False),
        sa.Column('salary_min', sa.Float(), nullable=True),
        sa.Column('salary_max', sa.Float(), nullable=True),
        sa.Column('job_type', sa.String(50), nullable=False),
        sa.Column('requirements', sa.Text(), nullable=True),
        sa.Column('posted_at', sa.DateTime(), nullable=True),
        sa.Column('employer_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['employer_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_jobs_id'), 'jobs', ['id'], unique=False)

    # Update applications table
    op.add_column('applications', sa.Column('cover_letter', sa.Text(), nullable=True))
    op.add_column('applications', sa.Column('resume_url', sa.String(500), nullable=True))
    op.add_column('applications', sa.Column('job_id', sa.Integer(), nullable=False))
    op.create_foreign_key('fk_applications_job_id', 'applications', 'jobs', ['job_id'], ['id'], ondelete='CASCADE')

    # Remove old columns
    op.drop_column('applications', 'company')
    op.drop_column('applications', 'role')
    op.drop_column('applications', 'date')


def downgrade():
    # Revert applications table
    op.add_column('applications', sa.Column('date', sa.String(), nullable=True))
    op.add_column('applications', sa.Column('role', sa.String(150), nullable=False))
    op.add_column('applications', sa.Column('company', sa.String(150), nullable=False))
    op.drop_constraint('fk_applications_job_id', 'applications', type_='foreignkey')
    op.drop_column('applications', 'job_id')
    op.drop_column('applications', 'resume_url')
    op.drop_column('applications', 'cover_letter')

    # Drop jobs table
    op.drop_index(op.f('ix_jobs_id'), table_name='jobs')
    op.drop_table('jobs')

    # Remove user columns
    op.drop_column('users', 'avatar')
    op.drop_column('users', 'name')
    op.drop_column('users', 'role')