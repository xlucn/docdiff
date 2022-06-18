import argparse
import difflib
import re


def diffsplit(diff, prefix, suffix):
    """
    Sometimes, difflib returns diff blocks containing multiple lines,
    this is to split them into individual lines.
    """
    new = []
    for seg in diff.splitlines():
        new.append((prefix + seg + suffix) if len(seg) else '')
    return '\n'.join(new)


def markdiff(seqmatcher):
    """
    quote added segments with '{+' and '+}', removed ones with '[-' and '-]'
    """
    line = ''
    for tag, i1, i2, j1, j2 in seqmatcher.get_opcodes():
        if tag == 'replace' or tag == 'insert':
            line += diffsplit(seqmatcher.b[j1:j2], '{+', '+}')
        if tag == 'replace' or tag == 'delete':
            line += diffsplit(seqmatcher.a[i1:i2], '[-', '-]')
        if tag == 'equal':
            line += seqmatcher.a[i1:i2]
    return line


def fastdiff(a, b):
    """
    compare text strictly line by line
    """
    new = []
    for line_a, line_b in zip(a.splitlines(), b.splitlines()):
        s = difflib.SequenceMatcher(a=line_a, b=line_b)
        new.append(markdiff(s))
    return '\n'.join(new)


def strdiff(a, b):
    """
    compare text, keep the changes within one line (see isjunk)
    """
    s = difflib.SequenceMatcher(
        a=a, b=b,
        isjunk=lambda x: x in ' \n',
        autojunk=False
    )
    return markdiff(s)


def splitdiff(a, b, addfmt, delfmt, newline='\n', fast=False):
    """
    show added and deleted changes in separate lines
    """
    delregex = re.compile('\\[-([^]]*)-\\]')
    addregex = re.compile('{\\+([^}]*)\\+}')
    funcdiff = fastdiff if fast else strdiff

    text = []
    for line in funcdiff(a, b).splitlines():
        if line.find('[-') >= 0 or line.find('{+') >= 0:
            old = delregex.sub(delfmt.format('\\1'), line)
            old = addregex.sub('', old)
            if len(old) > 0:
                text.append(old)
            new = addregex.sub(addfmt.format('\\1'), line)
            new = delregex.sub('', new)
            if len(new) > 0:
                text.append(new)
        else:
            text.append(line)
    return newline.join(text)


def htmldiff(a, b, fg, bg, ul, fast):
    start = '''<!DOCTYPE html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" type="image/x-icon" href="/static/favicon.png">
</head>
'''
    addstyle = ''
    delstyle = ''
    if fg:
        addstyle += "color: blue;"
        delstyle += "color: red;"
    if bg:
        addstyle += "background-color: yellow;"
        delstyle += "background-color: yellow;"
    if ul:
        addstyle += "text-decoration-line: underline;"
        addstyle += "text-decoration-color: blue;"
        addstyle += "text-decoration: underline blue;"
        delstyle += "text-decoration-line: underline;"
        delstyle += "text-decoration-color: red;"
        delstyle += "text-decoration-style: wavy;"
        delstyle += "text-decoration: underline red wavy;"

    addfmt = f'<span style="{addstyle}">{{}}</span>'
    delfmt = f'<span style="{delstyle}">{{}}</span>'

    return start + splitdiff(a=a.replace('\r\n', '\n'),
                             b=b.replace('\r\n', '\n'),
                             addfmt=addfmt,
                             delfmt=delfmt,
                             newline='<br>\n',
                             fast=fast)


def flask_app():
    from flask import Flask, request, send_file

    app = Flask('docdiff')

    @app.route('/')
    def index():
        return send_file('docdiff.html')

    @app.route('/result', methods=['POST', 'GET'])
    def process_file():
        return htmldiff(request.files['old'].read().decode(),
                        request.files['new'].read().decode(),
                        request.form.get('fg') == 'on',
                        request.form.get('bg') == 'on',
                        request.form.get('ul') == 'on',
                        request.form.get('fast') == 'on')

    return app


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", nargs=2, metavar=('old', 'new'),
                        help="Input files, new file after old file")
    parser.add_argument("-l", action="store_true",
                        help="Fast line-by-line comparison")
    parser.add_argument("-r", action="store_true",
                        help="Run built-in flask app in terminal")
    args = parser.parse_args()
    if not args.run_flask:
        if args.files is None or args.files == []:
            print("Use -f option to provide 2 files.")
        else:
            print(splitdiff(open(args.files[0]).read(),
                            open(args.files[1]).read(),
                            addfmt='\033[4;34m{}\033[0m',
                            delfmt='\033[9;31m{}\033[0m',
                            fast=args.line))
    else:
        flask_app().run(debug=True)
else:
    app = flask_app()
