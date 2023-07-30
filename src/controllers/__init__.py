"""Initialises all controllers.

This module imports each controller from their respective individual files, and creates one combined variable for all controllers that is used to initialise in main.py.
"""

from controllers.jobs_controller import jobs
from controllers.users_controller import users
from controllers.applications_controller import applications
from controllers.auth_controller import auth
from controllers.interviews_controller import interviews
from controllers.scorecards_controller import scorecards
from controllers.staff_controller import staff
from controllers.candidates_controller import candidates

controllers = [
    jobs,
    users,
    applications,
    auth,
    interviews,
    scorecards,
    staff, 
    candidates
]