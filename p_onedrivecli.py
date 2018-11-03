import onedrivecli
import os

if __name__ == "__main__":
    a = onedrivecli.OneDriveUser()
    a.logging()
    while True:
        command = input(a.current_path + ">")
        if command == "ls":
            a.ls()
        elif command[0:2] == "cd":
            a.super_cd(command[3:])
        elif command == "clear":
            os.system("cls")
        elif command[0:6] == "upload":
            a.upload_file(command[7:])
        elif command[0:5] == "mkdir":
            a.mkdir(command[6:])
        elif command[0:6] == "delete":
            a.d(command[7:], "delete")
        elif command[0:8] == "download":
            a.d(command[9:], "download")
        elif command[0:10] == "changeddir":
            a.set_download_dir(command[11:])
        elif command[0:4] == "quit":
            if a.quit():
                exit()
        elif command[0:6] == "system":
            if os.name == "nt":
                os.system("powershell " + command[7:])
        elif command[0:3] == "gdp":
            a.get_download_progress_all()
        elif command[0:2] == "sd":
            a.stop_download()
        elif command == "help":
            print("Full list of commands:")
            print("-ls: ex. ls / Lists all contents of current directory")
            print("-cd: ex. cd [dir_name] / Change directory")
            print("-help: ex. help / Prints all the commands")
            print("-clear: ex. clear / Clear screen")
            print("-upload: ex. upload [file_name] / Upload a file")
            print("-mkdir: ex. mkdir [folder_name] / Create a new folder")
            print("-delete: ex. delete [file_name1] [file_name2]... / Delete file/s")
            print("-download: ex. download [file_name1] [file_name2]... / Download file/s")
            print("-changeddir: ex. [absolute path]... / change download dir/s")
            print("-quit: Exit from program")
            print("-system: ex. system [cmd command] / Run a command in cmd")
            print("-gdp: ex. gad / check download process")
            print("-sd: ex. sd / terminate all downloads")
            print("")
        else:
            print("Command does not exist type help for a full command list")
