import script.repositories as r

def main():
    # Assicurarsi di essere nella root (msr_dockerfile) prima di eseguire
    
    query = 'stars:>1500'
    filename = 'Dockerfile'

    r.project_structure()    
    r.get_dockerfiles(query, filename)


if __name__ == '__main__':
    main()