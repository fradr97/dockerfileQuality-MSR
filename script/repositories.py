from script.config.constants import *
import script.database.database as db
import script.hadolint as hadolint
import script.dockerfilelint as dockerfilelint
from github import Github
import github
import os
import base64
import json


""" Metodo utilizzato per creare la struttura di cartelle in cui finiranno 
    i file che saranno generati in seguito """

def project_structure():
    if not os.path.isdir(RESOURCES_DIR):
        os.mkdir(RESOURCES_DIR)
        os.mkdir(RESOURCES_DIR + DOCKERFILE_DIR)
        os.mkdir(RESOURCES_DIR + HADOLINT_DIR)
        os.mkdir(RESOURCES_DIR + DOCKERFILELINT_DIR)
    else:
        print(FOLDER_EXISTS_MESSAGE)


""" Metodo utilizzato per ricercare i repository mediante una query (es. 'stars:>1500') e contenenti
    uno specifico file ('Dockerfile') nella root. Viene pertanto scaricato il Dockerfile di ogni repository
    nella cartella /resources/dockerfile e a ciascuno viene assegnato il nome: 'Dockerfile_nomerepository'.
    Dopodiché vengono recuperati i dati necessari, eseguiti i tool di analisi statica sui Dockerfile scaricati 
    (creando dei json con i smell rilevati) e inserito tutto nel database.
    
    Nell'if vengono scartati repositories i cui Dockerfile sono 'misteriosamente' problematici e 
    i tool di analisi non riescono ad analizzarli """

def get_dockerfiles(query, filename):
    g = Github(GITHUB_TOKEN)
    repositories = g.search_repositories(query=query)
    print(DOCKERFILE_NUMBER_MESSAGE, repositories.totalCount)

    for repository in repositories:
        try:
            if repository.full_name != 'apache/superset' and \
                    repository.full_name != 'excalidraw/excalidraw' and \
                    repository.full_name != 'jumpserver/jumpserver' and \
                    repository.full_name != 'errbit/errbit':
                repo = g.get_repo(repository.full_name)
                contents = repo.get_contents(filename)
                
                f = open(RESOURCES_DIR + DOCKERFILE_DIR +
                         DOCKERFILE_BASE_NAME + repository.name, 'w')
                f.write(base64.b64decode(contents.content).decode())
                f.close()

                print('\n*** ' + repo.full_name +
                      ": contiene Dockerfile ***\n")

                contributors = repo.get_contributors().totalCount
                dockerfile_instructions = count_dockerfile_instructions(
                    RESOURCES_DIR + DOCKERFILE_DIR + DOCKERFILE_BASE_NAME + repository.name)

                id_repo = db.insert_repositories_data(repo.full_name, repo.clone_url, repo.stargazers_count,
                                                      dockerfile_instructions, contributors)

                hadolint.exec_hadolint(repository.name, id_repo)
                dockerfilelint.exec_dockerfilelint(repository.name, id_repo)
                get_languages_percentage(repo, id_repo)
        except github.UnknownObjectException:
            print(NO_DOCKERFILE_MESSAGE + repository.full_name)


""" Metodo utilizzato per ottenere il numero di istruzioni di un Dockerfile
    (escluso righe bianche) """

def count_dockerfile_instructions(dockerfile_path):
    dockerfile = open(dockerfile_path, "r")
    line_count = 0

    for line in dockerfile:
        if line != "\n":
            line_count += 1
    dockerfile.close()

    return line_count


""" Metodo utilizzato per recuperare i linguaggi di programmazione utilizzati nel repository
    passato come parametro e le percentuali di utilizzo di ogni linguaggio. Poiché dall'API non arrivano 
    le percentuali (ma i byte scritti in un linguaggio), sulla base di questi byte calcola la 
    percentuale per ogni linguaggio.
    Infine memorizza tutto nel db """

def get_languages_percentage(repo, id_repo):
    parsed = json.loads(json.dumps(repo.get_languages()))
    sum_bytes = 0

    for language in repo.get_languages():
        sum_bytes += parsed[language]
    
    for language in repo.get_languages():
        percentage = float("{:.2f}".format((parsed[language] / sum_bytes) * 100))
        if percentage > 0.00:
            db.insert_languages(language, id_repo, percentage)
