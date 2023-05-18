import os 
import json
# reading the json files 
with open('data.json', 'r') as jsonfile:
    data = json.load(jsonfile)

class Page():
    def __init__(self,path,markdown_file):
        #self.data = DATA["Page_commands"]
        self.path = path
        self.file =  markdown_file

    def action(self,action_type):
        self.commands = self.data[action_type]
        for command in self.commands:
            command = command.replace("path",self.path)
            command = command.replace("filename",self.file)
            
            os.system('powershell.exe ' + command)

class Manager(Page):
    def __init__(self):
        self.data = data
        self.repository = self.data["git_repository"]
        self.git_user = self.data["git_credentials"]["username"]
        self.git_password = self.data["git_credentials"]["password"]
    
    def set_up(self,repository,username,password):
        self.data["configured"] = "true"
        self.data["git_repository"] = repository
        self.data["git_credentials"]["username"] = username
        self.data["git_credentials"]["password"] = password

        new_json_file = json.dumps(self.data,indent=4)
        with open('data.json', 'w') as old_json_file:
            old_json_file.write(new_json_file)
        
        return self
