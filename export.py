from datetime import datetime, timedelta
import ssaw
from dotenv import dotenv_values
from ssaw import interviews

config = dotenv_values(".env")

WORKSPACE = "primary"
QUESTIONNAIRE_TITLE = "fiche_recensement"
QUESTIONNAIRE_VERSION = 3

# :param interview_status: What interviews to include in the export:
# ``All``, ``SupervisorAssigned``, ``InterviewerAssigned``, ``Completed``,
# ``RejectedBySupervisor``, ``ApprovedBySupervisor``, ``RejectedByHeadquarters``, ``ApprovedByHeadquarters``
INTERVIEW_STATUS = "ApprovedBySupervisor"


client = ssaw.Client(url=config['SERVER_URL'], api_user=config['API_USER'], api_password=config['API_PASSWORD'])
questionnaire = next(q for q in ssaw.QuestionnairesApi(client).get_list() if q.variable == QUESTIONNAIRE_TITLE and q.version == QUESTIONNAIRE_VERSION)

today = datetime.now()
yesterday = today - timedelta(days=1)

if (questionnaire):
  print(questionnaire)
  # export = ssaw.ExportApi(client, WORKSPACE).get(
  #   questionnaire_identity=questionnaire.id,
  #   export_type="Tabular",
  #   interview_status=INTERVIEW_STATUS,
  #   export_path="exports",
  #   generate=True,
  #   show_progress=True,
  #   limit_date=yesterday
  # )
  # print(export)
  export = ssaw.ExportApi(client, WORKSPACE).get(
    questionnaire_identity=questionnaire.id,
    export_type="Binary",
    interview_status=INTERVIEW_STATUS,
    export_path="exports",
    generate=True,
    show_progress=True,
    limit_date=yesterday,
    limit_age=1,
  )
  print(export)