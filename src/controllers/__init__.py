from controllers.jobs_controller import jobs
from controllers.users_controller import users
from controllers.applications_controller import applications
from controllers.auth_controller import auth
from controllers.interviews_controller import interviews
from controllers.scorecards_controller import scorecards

controllers = [
    jobs,
    users,
    applications,
    auth,
    interviews,
    scorecards
]