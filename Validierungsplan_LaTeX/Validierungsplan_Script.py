import os

# Prompt variable input date


def createLaTeXDirectory():
    currentworkingdir = os.getcwd()
    path = ("%s/Validierungsplan_LaTeX" % currentworkingdir)
    
    try:
         os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Succesfully created the directory %s" % path)

def createLaTeXFile():
    date_release = input("Datum des Titels: ")
    currentworkingdir = os.getcwd()
    path = ("%s/Validierungsplan_LaTeX" % currentworkingdir)
    os.chdir(path)
    texfile = open("ValidierungsplanPHYDENT%s.tex" % date_release, "x")
    texfile.close()
    os.system("pdflatex ValidierungsplanPHYDENT%s.tex" % date_release)

#createLaTeXDirectory()

createLaTeXFile()

def save_var_latex(key,value):
    import csv
    import os

    dict_var = {}

    file_path = os.path.join(os.getcwd(), "pythonvariables.dat")

    try:
        with open(file_path, newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                dict_var[row[0]] = row[1]
    except FileNotFoundError:
        pass

    dict_var[key] = value

    with open(file_path, "w") as f:
        for key in dict_var.keys():
            f.write(f"{key},{dict_var[key]}\n")


save_var_latex("document_version", 21)