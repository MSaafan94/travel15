import logging
_logger = logging.getLogger(__name__)
from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    # Custom fields
    subtask_percentage = fields.Integer(compute='_compute_subtask_percentage')
    parent_task_count = fields.Integer(compute='_compute_parent_task_count')

    @api.depends('child_ids.subtask_percentage')
    def _compute_project_percentage(self):
        """
        Compute the project completion percentage based on subtask percentages.
        """
        for task in self:
            total_subtasks = len(task.child_ids)
            if total_subtasks:
                subtask_percentages = [subtask.subtask_percentage for subtask in task.child_ids]
                task.project_percentage = sum(subtask_percentages) / total_subtasks
                _logger.info('Project Percentage: %s', task.project_percentage)
            else:
                task.project_percentage = 0
                _logger.info('No subtasks found.')

    @api.depends('child_ids.stage_id')
    def _compute_subtask_percentage(self):
        """
        Compute the subtask completion percentage based on the stage of child tasks.
        """
        for task in self:
            total_subtasks = len(task.child_ids)
            if total_subtasks:
                in_progress_subtasks = task.child_ids.filtered(lambda t: t.stage_id.name == 'Done')
                task.subtask_percentage = (len(in_progress_subtasks) / total_subtasks) * 100
                _logger.info('Subtask Percentage: %s', task.subtask_percentage)
            else:
                task.subtask_percentage = 0
                _logger.info('No subtasks found.')

    @api.depends('project_id.task_ids')
    def _compute_parent_task_count(self):
        """
        Compute the total number of parent tasks in a project.
        """
        for task in self:
            project = task.project_id
            task.parent_task_count = len(project.task_ids.filtered(lambda t: not t.parent_id))
            _logger.info('Parent Task Count: %s', task.parent_task_count)

    parent_percentage = fields.Float(string='parent percentage',)

class ProjectProject(models.Model):
    _inherit = 'project.project'

    project_percentage = fields.Float(string="Project Percentage", compute='_compute_project_percentage',)
    parent_percentage = fields.Float(string='parent percentage',)

    @api.depends('task_ids.subtask_percentage')
    def _compute_project_percentage(self):
        """
        Compute the project completion percentage based on subtask percentages.
        """
        for project in self:
            parent_tasks = project.task_ids.filtered(lambda t: not t.parent_id)
            total_tasks = len(parent_tasks)
            total_done_tasks = project.task_ids.filtered(lambda t: t.stage_id.name == 'Done' and not t.parent_id)
            len_total_done_tasks = len(total_done_tasks)
            for item in total_done_tasks:
                print(item.name)
            print(len(total_done_tasks))
            print(total_tasks)
            if total_tasks:
                completed_task_percentages = [task.subtask_percentage for task in parent_tasks]
                project.parent_percentage = (len_total_done_tasks/total_tasks)*100
                if completed_task_percentages:
                    project_percentage = sum(completed_task_percentages) / total_tasks
                    project.project_percentage = project_percentage
                    _logger.info('Project Percentage: %s', project_percentage)
                else:
                    project.project_percentage = 0.0
                    _logger.info('No completed tasks found.')
            else:
                project.project_percentage = 0.0
                _logger.info('No tasks found.')
