#!/usr/bin/python
import os
import httplib
import json
import sys, getopt
import subprocess
import shutil


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
    pipe = subprocess.Popen(cmd, shell=True, cwd=work_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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

def init_makefile(path):
	file = open(path, 'w+')
	text = "NAME = \n"
	text += "FILES = \n"
	text += "INCLUDES = includes/\n"
	text += "OBJECTS = $(FILES:srcs/%.c=./%.o)\n"
	text += "./libft/libft.a\n"
	text += "FLAGS = -Wall -Wextra -Werror\n"
	text += "HDR = libft.h\n"
	text += ".PHONY: all clean fclean re\n\n"
	text += "all: $(NAME)\n"
	text += "#$(NAME): $(LIBFT)\n"
	text += "\t#@gcc -c $(FLAGS) $(FILES) -I$(INCLUDES) -I./libft\n"
	text += "\t#@gcc -o $(NAME) $(FLAGS) $(OBJECTS) $(LIBFT) -I./libft -I$(INCLUDES)\n\n"
	text += "#$(LIBFT):\n"
	text += "\t#@make -C ./libft\n\n"
	text += "clean:\n"
	text += "\t#@make clean -C ./libft\n"
	text += "\t@/bin/rm -f $(OBJECTS)\n\n"
	text += "fclean: clean\n"
	text += "\t#@make fclean -C ./libft\n"
	text += "\t@/bin/rm -f $(NAME)\n"
	text += "re: fclean all\n"
	file.write(text)
	file.close()



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
	return project_path + project_name

def process_language(project_language, project_path):
	if project_language == "c" or project_language == "C":
		with open(project_path + '/' + "Makefile", 'w+'): pass
		init_makefile(project_path + '/' + "Makefile")
		os.makedirs(project_path + '/' + "src")
		os.makedirs(project_path + '/' + "includes")
		with open(project_path + '/' + ".gitignore", 'w+'): pass
		file = open(project_path + '/' + ".gitignore", 'w+')
		file.write("*.out")
		file.close()

def process_include(include, project_path):
	if (include == "libft"):
		os.makedirs(project_path + "/" + "libft")
		print "Cloning libft ..."
		git_clone("https://github.com/anmatsuk/libft.git", project_path + "/libft")
		shutil.rmtree(project_path + "/libft/" + ".git")

def main(argv):
	name = ''
	path = ''
	language = ''
	include = ''
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'n:p:l:i:')
	except getopt.GetoptError:
		print 'setup.py -n <project_name> [-p <path> -l <language>]'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'setup.py -n <project_name> [-p <path> -l <language>]'
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
		print 'setup.py -n <project_name> [-p <path> -l <language>]'
		sys.exit(2)
	
	path = create_dir(path, name)
	print "Created project: " + bcolors.OKGREEN + name + bcolors.ENDC + " path: " + bcolors.OKGREEN + path + bcolors.ENDC
	process_language(language, path)
	process_include(include, path)

if __name__ == "__main__":
	if (len(sys.argv) - 1 == 0):
		print 'setup.py -n <project_name> [-p <path> -l <language> -i <include>]'
		sys.exit()
	main(sys.argv[1:])
