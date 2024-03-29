
import os
import glob
import markdown
import json

title, section = '', ''

with open("article/article_template.html") as f:
    template = f.read()

with open('scripts/articles.json') as json_file:
    article_data = json.load(json_file)


for f in glob.iglob('markdown_content/*.md'):
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

                elif command == 'category':
                    category = args

                elif command == 'tags':
                    tag_names = args.split(', ')
                    tags = []
                    for name in tag_names:
                        tags.append("<span class='tag'>" + name + "</span>")

                else:
                    print("UNKNOWN COMMAND:", command, args)

            else:
                body += line + "\n\n"

    file_name = os.path.basename(f)
    destination = os.path.join("article", title.lower() + ".html")

    with open(destination, 'w') as file:
        output = template
        output = output.replace("{{body}}", markdown.markdown(body))
        output = output.replace("{{title}}", title)
        output = output.replace("{{tags}}", ''.join(tags))


        file.write(output)

    # update data json dict

    if title not in article_data.keys():
        article_data[title] = {}
    article_data[title]["title"] = title
    article_data[title]["index"] = int(os.path.splitext(file_name)[0].split('_')[0])
    article_data[title]["tags"] = tags


    json_string = json.dumps(article_data)

    with open('scripts/articles.json', 'w') as outfile:
        outfile.write(json_string)



# rebuild the article pages
# rebuild tag pages
# rebuild user pages
