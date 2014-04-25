githelper
=========

This is a recommender system for git hub repositories. It classifies the current repository
and displays the top repositories of that class.

Structure of a each repository Object crawled:
curr_repo['description'] = repo['description']
curr_repo['name'] = repo['full_name']
curr_repo['url'] = repo['clone_url']
curr_repo['readme'] = readfile.read()
