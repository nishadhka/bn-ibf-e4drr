from collections import OrderedDict

def read_acronym_txt_file(in_path):
    """
    This method reads a text file in which each line is of the form
    <acronym>: description. The method creates a dictionary acro_to_desc

    Parameters
    ----------
    in_path: str

    Returns
    -------
    dict[str, str]

    """
    acro_to_desc = OrderedDict()
    with open(in_path, "r") as f:
        for line in f:
            if line.strip():
                acro, desc = line.split(":", 1)
                acro_to_desc[acro.strip()] = desc.strip()
    acro_to_desc = OrderedDict(sorted(acro_to_desc.items(),
                               key=lambda item: item[0].lower()))
    return acro_to_desc


def write_latex_file(acro_to_desc, out_path):
    """
    This method writes a LaTex file at `out_path` in which the items of the
    dictionary acro_to_desc are listed in alphabetical order of the acronyms.

    Parameters
    ----------
    acro_to_desc: dict[str, str]
    out_path: str

    Returns
    -------
    None

    """
    with open(out_path, "w") as f:
        f.write("\\documentclass{article}\n")
        f.write("\\begin{document}\n")
        f.write("\\section*{Acronyms}\n")
        f.write("\\begin{itemize}\n")
        for acro, desc in acro_to_desc.items():
            if desc is None:
                desc = ""
            f.write("\\item {\\bf " + acro + "}: " + desc + "\n")
        f.write("\\end{itemize}\n")
        f.write("\\end{document}\n")


if __name__ == "__main__":
    def main():
        in_path = "acro.txt"
        out_path = "acro.tex"
        write_latex_file(read_acronym_txt_file(in_path),
                         out_path)
    main()
