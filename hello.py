import ssaw
from dotenv import dotenv_values
from ssaw import interviews
from ssaw.headquarters_schema import String

config = dotenv_values(".env")

client = ssaw.Client(url=config['SERVER_URL'], api_user=config['API_USER'], api_password=config['API_PASSWORD'])
questionnaire = next(q for q in ssaw.QuestionnairesApi(client).get_list() if q.title == "Fiche de recensement" and q.version == 1)
statuses = ssaw.QuestionnairesApi(client, workspace="primary").statuses()
print(statuses)

interviews = ssaw.InterviewsApi(client, workspace="primary").get_list(questionnaire_id=questionnaire.questionnaire_id, status="APPROVEDBYHEADQUARTERS")
for i in interviews:
  print(i)
  info = ssaw.InterviewsApi(client, workspace="primary").get_info(i.id)
  for ligne in info:
    if (ligne['Answer']):
      print(ligne['VariableName'] + ': ' + ligne['Answer'])
    else:
      print(ligne['VariableName'] + ': ' + '- VIDE -')