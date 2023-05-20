import os 
import json
import typer 

app = typer.Typer()

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
        self.project_name = self.data["project_name"]
        self.git_user = self.data["git_credentials"]["username"]
        self.git_password = self.data["git_credentials"]["password"]

        self.actions_list = {
            "setup git" : r"local\git_setup",
            "build template" : r"local\build_template",
            "create page" : r"local\create_page.txt",
            "delete page" : r"local\delete_page.txt",
        }
        self.filter_list = {
            "@username" : self.git_user,
            "@password" : self.git_password,
            "@repository"  : self.repository,
            "@project_name" : self.project_name
        }
    
    def set_up(self,repository,project_name,username,password):
        self.data["configured"] = "true"
        self.data["git_repository"] = repository
        self.data["project_name"] = project_name
        self.data["git_credentials"]["username"] = username
        self.data["git_credentials"]["password"] = password

        new_json_file = json.dumps(self.data,indent=4)

        with open('local\data.json', 'w') as old_json_file:
            old_json_file.write(new_json_file)
        return self
    
    def action(self,action):
        command_list = self.actions_list[action]
        command_list = open(command_list,'r').readlines()

        for command in command_list:
            for string_to_filter in self.filter_list:
                command = command.replace(string_to_filter,self.filter_list[string_to_filter])

            print(command)
            #os.system('powershell.exe ' + command)

    def create_page(self,filename):
        self.page = Page(filename)
        self.filter_list["@filename"] = self.page.file_name 


@app.callback(invoke_without_command=True)
def update():
    manager = Manager()
    

@app.command()
def set_parameters(project : str,repo : str,user : str, password: str):
    manager = Manager()
    manager.set_up(repo,project,user,password)
    manager.action("setup git")
    manager.action("build template")


if __name__ == "__main__":
    app()

