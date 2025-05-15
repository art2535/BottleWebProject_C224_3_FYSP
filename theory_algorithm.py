import markdown
def get_theory(pathToFile):
    try:
        with open(pathToFile) as file:
            theory_md = file.read()
        theory_html = markdown.markdown(theory_md)
        return theory_html
    except Exception as e:
        return f"Error loading theory: {e}"
