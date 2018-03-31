#!/usr/bin/python

import os
import sys
import getopt
import subprocess
import shutil

git_url = "https://github.com/anmatsuk/libft.git"


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


"""
Shell command execution:
"""


def execute_shell_command(cmd, work_dir):
    pipe = subprocess.Popen(cmd, shell=True, cwd=work_dir,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, error) = pipe.communicate()
    print out, error
    pipe.wait()


"""
    Clone remote repo:
    :param repo_url: URL of remote git repository.
    :param repo_dir: Directory which to clone the remote repository into.
"""


def git_clone(repo_url, repo_dir):
    cmd = 'git clone ' + repo_url + ' ' + repo_dir
    execute_shell_command(cmd, repo_dir)


"""
filling out Makefile with regular rules
"""


def init_makefile(path):
    text = """NAME = 
FILES = 
INCLUDES = includes/
OBJECTS = $(FILES:srcs/%.c=./%.o)
./libft/libft.a
FLAGS = -Wall -Wextra -Werror
HDR = libft.h
.PHONY: all clean fclean re

all: $(NAME)
#$(NAME): $(LIBFT)
    #@gcc -c $(FLAGS) $(FILES) -I$(INCLUDES) -I./libft
    #@gcc -o $(NAME) $(FLAGS) $(OBJECTS) $(LIBFT) -I./libft -I$(INCLUDES)

#$(LIBFT):
    #@make -C ./libft

clean:
    #@make clean -C ./libft
    @/bin/rm -f $(OBJECTS)

fclean: clean
    #@make fclean -C ./libft
    @/bin/rm -f $(NAME)
re: fclean all
"""
    with open(path, "w+") as file:
        file.write(text)


"""
Create main directory for the project with gitignore , src and includes
"""


def create_dir(project_path, project_name):

    if project_path == "" or not os.path.isdir(project_path):
        project_path = os.path.dirname(os.path.realpath(__file__))
    project_name = project_name.replace(" ", "_")
    if not project_path[:-1].endswith('/'):
        project_path += "/"

    if os.path.exists(project_path + project_name):
        print "Project already exists"
        sys.exit()
    else:
        os.makedirs(project_path + project_name)
    project_path += project_name
    os.makedirs(project_path + '/' + "src")
    os.makedirs(project_path + '/' + "includes")
    with open(project_path + '/' + "author", 'w+'):
        pass
    file = open(project_path + '/' + "author", 'w+')
    file.write("amatsuk")
    file.close()
    with open(project_path + '/' + ".gitignore", 'w+'):
        pass
    file = open(project_path + '/' + ".gitignore", 'w+')
    file.write("*.out")
    file.write("\n")
    file.write("*.o")
    file.close()
    return project_path


"""
Create Makefile
"""


def process_language(project_language, project_path):
    if project_language == "c" or project_language == "C":
        with open(project_path + '/' + "Makefile", 'w+'):
            pass
        init_makefile(project_path + '/' + "Makefile")


"""
clone repo for libft
"""


def process_include(include, project_path):
    line = ""
    if (include != "libft"):
        line = raw_input("Would you like to add libft ? [y/n] ")
        if (line == "y" or line == "yes"):
            include = "libft"
    if (include == "libft"):
        os.makedirs(project_path + "/" + "libft")
        print "Cloning libft ..."
        git_clone(git_url, project_path + "/libft")
        shutil.rmtree(project_path + "/libft/" + ".git")


def print_help():
    print 'setup.py -n <project_name> [-p <path> -l <language> -i <libft>]'


def main(argv):
    name = ''
    path = ''
    language = ''
    include = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'n:p:l:i:')
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ("-n", "--name"):
            name = arg
        elif opt in ("-p", "--path"):
            path = arg
        elif opt in ("-l", "--language"):
            language = arg
        elif opt in ("-i", "--include"):
            include = arg
    if name == "":
        print_help()
        sys.exit(2)
    path = create_dir(path, name)
    print "Created project: {name} path: {path}".format(name=bcolors.OKGREEN + name + bcolors.ENDC,
                                                        path=bcolors.OKGREEN + path + bcolors.ENDC)
    process_language(language, path)
    process_include(include, path)


if __name__ == "__main__":
    if (len(sys.argv) - 1 == 0):
        print_help()
        sys.exit()
    main(sys.argv[1:])
