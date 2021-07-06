# ************** TOKEN e DATABASE ************** #

GITHUB_TOKEN = '*********************'

HOST = 'localhost'
USER_DB = 'root'
PASSWORD_DB = ''
DATABASE = 'msr_dockerfile'


# ************** DIRECTORIES ************** #

RESOURCES_DIR = 'resources/'

DOCKERFILE_DIR = 'dockerfile/'
DOCKERFILE_BASE_NAME = 'Dockerfile_'

HADOLINT_DIR = 'hadolint/'
HADOLINT_BASE_NAME = 'hadolint_'

DOCKERFILELINT_DIR = 'dockerfilelint/'
DOCKERFILELINT_BASE_NAME = 'dockerfilelint_'


# ************** MESSAGGI ************** #

FOLDER_EXISTS_MESSAGE = 'Folders exists!'
DOCKERFILE_NUMBER_MESSAGE = 'Numero totale di repositories (con Dockerfile e senza): '
NO_DOCKERFILE_MESSAGE = 'Nessun Dockerfile nella root del repository: '
NUMBER_HADOLINT_ISSUES_MESSAGE = 'Number of hadolint issues: '
NUMBER_DOCKERFILELINT_ISSUES_MESSAGE = 'Number of dockerfilelint issues: '
NO_HADOLINT_ISSUES_MESSAGE = 'No hadolint issues!'
NO_DOCKERFILELINT_ISSUES_MESSAGE = 'No dockerfilelint issues!\n'

JSON = '.json'