import Webserver

Prefix = "Start"
Quit = "Stop"

Input = None
def Compare(String): return str.lower(Input).startswith(str.lower(String))

while not ((type(Input) == str) and (Compare(Prefix) or Compare(Quit))): Input = input(f"Say \"{Prefix}\" to start the webserver or \"{Quit}\" to quit\n")
if Compare(Quit): exit()

Webserver.API.add_resource(Webserver.Cache, "/")
Webserver.Start()