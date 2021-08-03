import ssaw
from dotenv import dotenv_values
from ssaw import interviews
from ssaw.headquarters_schema import String

config = dotenv_values(".env")

WORKSPACE = "primary"
QUESTIONNAIRE_TITLE = "Fiche de recensement"
QUESTIONNAIRE_VERSION = 1
INTERVIEW_STATUS = "Completed"


client = ssaw.Client(url=config['SERVER_URL'], api_user=config['API_USER'], api_password=config['API_PASSWORD'])
questionnaire = next(q for q in ssaw.QuestionnairesApi(client).get_list() if q.title == QUESTIONNAIRE_TITLE and q.version == QUESTIONNAIRE_VERSION)

if (questionnaire):
  print(questionnaire)
  export = ssaw.ExportApi(client, WORKSPACE).get(
    questionnaire_identity=questionnaire.id,
    export_type="Tabular",
    interview_status=INTERVIEW_STATUS,
    export_path="exports",
    generate=True
  )
  print(export)
  export = ssaw.ExportApi(client, WORKSPACE).get(
    questionnaire_identity=questionnaire.id,
    export_type="Binary",
    interview_status=INTERVIEW_STATUS,
    export_path="exports",
    generate=True
  )
  print(export)