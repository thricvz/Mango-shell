import os 
import json
# reading the json files 
with open('local\data.json', 'r') as jsonfile:
    data = json.load(jsonfile)

class Page():
    def __init__(self,path,markdown_file):
        self.file =  markdown_file

class Manager(Page):
    def __init__(self):
        self.data = data
        self.repository = self.data["git_repository"]
        self.git_user = self.data["git_credentials"]["username"]
        self.git_password = self.data["git_credentials"]["password"]

        self.full_command_list = {
            "setup git" : "local\git_setup",
            "build template" : "local\build_template",
            "create page" : "local\create_page.txt",
            "delete page" : "local\delete_page.txt",
        }
        self.filter_list = {
            "@username" : self.git_user,
            "@password" : self.git_password,
            "@repository"  : self.repository
        }
    
    def set_up(self,repository,username,password):
        self.data["configured"] = "true"
        self.data["git_repository"] = repository
        self.data["git_credentials"]["username"] = username
        self.data["git_credentials"]["password"] = password

        new_json_file = json.dumps(self.data,indent=4)
        with open('local\data.json', 'w') as old_json_file:
            old_json_file.write(new_json_file)
        return self
    
    def manage(self,action):
        command_list = self.full_command_list[action]
        command_list = open(command_list,'r').readlines()

        for command in command_list:
            for string_to_filter in self.filter_list:
                command = command.replace(string_to_filter,self.filter_list[string_to_filter])

            os.system('powershell.exe ' + command)

    def create_page(self,filename):
        self.page = Page(filename)
        self.filter_list["@filename"] = self.page.file_name 


