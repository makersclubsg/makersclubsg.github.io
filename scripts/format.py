
import os
import glob
import markdown

title, author, section = '', '', ''

with open("articles/article_template.html") as f:
    template = f.read()

for f in glob.iglob('markdown_content/*.txt'):
    body = ""

    with open(f, 'r') as file:
        raw = file.read()
        lines = raw.split("\n")

        for line in lines:
            stripped = line.lstrip()
            indentation = line[:len(line) - len(stripped)]

            if stripped.startswith('^'):
                command,_,args = stripped.rstrip('\n').lstrip('^').partition(' ')
                args = args.strip()

                if command == 'title':
                    title = args

                elif command == 'section':
                    section = args
                elif command == 'author':
                    author = args
                else:
                    print("UNKNOWN COMMAND:", command, args)

            else:
                body += line + "\n\n"

    file_name = os.path.basename(f)
    destination = os.path.join("articles", os.path.splitext(file_name)[0] + ".html")

    with open(destination, 'w') as file:
        output = template
        output = output.replace("{{body}}", markdown.markdown(body))
        output = output.replace("{{title}}", title)
        output = output.replace("{{author}}", author)

        file.write(output)
