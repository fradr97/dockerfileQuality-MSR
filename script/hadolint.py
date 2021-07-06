from script.config.constants import *
import os
import json
import script.database.database as db


""" Metodo utilizzato per eseguire hadolint sul dockerfile dato in input e genera
    un file .json (output 'sporco' e non formattato in json). Tale file viene successivamente
    elaborato per estrarre solo le informazioni necessarie:
        - codice dello smell hadolint (es. DL3000 o SC2164)
        - descrizione corrispondente allo smell.
    A tal fine viene creato un json ben formattato. Infine memorizza per ogni dockerfile 
    di un repository (id_repo) gli smell nel db """

def exec_hadolint(dockerfile_name, id_repo):
    dockerfile_path = RESOURCES_DIR + DOCKERFILE_DIR + DOCKERFILE_BASE_NAME + dockerfile_name
    new_hadolint_json_path = RESOURCES_DIR + HADOLINT_DIR + HADOLINT_BASE_NAME + dockerfile_name + JSON
    
    os.system('cmd /c "hadolint "' + dockerfile_path + '">"' + new_hadolint_json_path)
    
    finput = open(new_hadolint_json_path, 'rt')
    line = finput.readline()

    data = {}
    data['issues'] = []

    while line:
        start_line = 0
        end_line = len(line)
        smell_id = ''
        smell_description = ''

        if line.find('DL', start_line, end_line) != -1:
            smell_id = line[line.find('DL', start_line, end_line):line.find('DL', start_line, end_line) + 6]

        if line.find('SC', start_line, end_line) != -1:
            smell_id = line[line.find('SC', start_line, end_line):line.find('SC', start_line, end_line) + 6]

        if line.find('m: ', start_line, end_line) != -1:
            smell_description = line[line.find('m: ', start_line, end_line) + 3:end_line]

        data['issues'].append({
            'category': smell_id,
            'description': smell_description.replace('\n', '')})

        line = finput.readline()

    with open(new_hadolint_json_path, 'w') as outfile:
        json.dump(data, outfile)

    finput.close()
    
    parse_hadolint_dokerfile_json(new_hadolint_json_path, id_repo)


""" Metodo utilizzato per recuperare le informazioni necessarie dai json generati da hadolint
    e memorizzarle nel db """

def parse_hadolint_dokerfile_json(hadolint_file_path, id_repo):
    with open(hadolint_file_path, 'r') as json_file:
        data = json.load(json_file)

    count = len(data['issues'])
    if count > 0:
        print(NUMBER_HADOLINT_ISSUES_MESSAGE, count)
        for issue in range(count):
            db.insert_smells(data['issues'][issue]['category'], data['issues'][issue]['description'], 'hadolint', id_repo)
    else:
        print(NO_HADOLINT_ISSUES_MESSAGE)