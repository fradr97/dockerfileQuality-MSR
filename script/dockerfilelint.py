from script.config.constants import *
import os
import json
import script.database.database as db


""" Metodo utilizzato per eseguire dockerfilelint sul dockerfile dato in input e genera
    un file json, mediante il tag '--json'
    Infine memorizza per ogni dockerfile di un repository (id_repo) gli smell nel db """

def exec_dockerfilelint(dockerfile_name, id_repo):
    dockerfile_path = RESOURCES_DIR + DOCKERFILE_DIR + DOCKERFILE_BASE_NAME + dockerfile_name
    new_dockerfilelint_json_path = RESOURCES_DIR + DOCKERFILELINT_DIR + DOCKERFILELINT_BASE_NAME + dockerfile_name + JSON

    os.system('cmd /c "dockerfilelint "' + dockerfile_path + '" --json > "' + new_dockerfilelint_json_path)
    parse_dockerfilelint_json(new_dockerfilelint_json_path, id_repo)


""" Metodo utilizzato per recuperare le informazioni necessarie dai json generati da dockerfilelint
    e memorizzarle nel db """
    
def parse_dockerfilelint_json(dockerfilelint_file_path, id_repo):
    with open(dockerfilelint_file_path, 'r') as json_file:
        data = json.load(json_file)

    count = len(data['files'][0]['issues'])
    if count > 0:
        print(NUMBER_DOCKERFILELINT_ISSUES_MESSAGE, count, '\n')
        for issue in range(count):
            db.insert_smells(data['files'][0]['issues'][issue]['category'], data['files'][0]['issues'][issue]['description'], 'dockerfilelint', id_repo)
    else:
        print(NO_DOCKERFILELINT_ISSUES_MESSAGE)