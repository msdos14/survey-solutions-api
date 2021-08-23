import ssaw
from ssaw import InterviewsApi
from dotenv import dotenv_values
from ssaw.headquarters_schema import Boolean
from ssaw.exceptions import NotAcceptableError

config = dotenv_values(".env")

WORKSPACE = "primary"
QUESTIONNAIRE_TITLE = "fiche_recensement"
QUESTIONNAIRE_VERSION = 3

client = ssaw.Client(url=config['SERVER_URL'], api_user=config['API_USER'], api_password=config['API_PASSWORD'])

path = r"FICHES - Resultat.txt" # FIchier à valider
print(path)
f = open(path, "r")
data = f.read()
lignes = data.split('\n')

# remove header
lignes = lignes[1:]

lignes = list(map(lambda l: l.split('\t'), lignes))

for ligne in lignes:
  print(ligne)
  if ligne[5] == '-1':
    print("Skipping")
    continue

  interviewID = ligne[1]

  isRejected = True if ligne[5] == '0' else False
  if not isRejected:
    isRejected = True if ligne[2] == '' else False

  print("IsRejected: %r" % isRejected)

  history = InterviewsApi(client, WORKSPACE).history(interview_id=interviewID)
  history = filter(lambda line: line['OriginatorName'] == 'DefaultAPI', history)
  history = list(history)
  status = None
  if len(history) > 0:
    lastLine = history[-1]
    print(lastLine)
    status = lastLine['Action']

  try:
    if isRejected: # status will be set to 'RejectedByHeadquarter'
      comment = ligne[7]
      if status != 'RejectedByHeadquarter':
        print('It will be rejected')
        InterviewsApi(client, WORKSPACE).hqreject(interviewid=interviewID, comment=comment)
      else:
        print('Already rejected')
    else: # status will be set to 'ApproveByHeadquarter'
      if (status) != 'ApproveByHeadquarter':
        print('It will be approved')
        InterviewsApi(client, WORKSPACE).hqapprove(interviewid=interviewID)
      else:
        print('Already approved')
  except NotAcceptableError:
    print('Skipping cuz of error')
