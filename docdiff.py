import difflib
import re
import sys


def diffsplit(diff, prefix, suffix):
    """
    Sometimes, difflib returns diff blocks containing multiple lines,
    this is to split them into individual lines.
    """
    new = []
    for seg in diff.splitlines():
        if len(seg) > 0:
            new.append(prefix + seg + suffix)
        else:
            new.append('')
    return '\n'.join(new)


def markdiff(seqmatcher):
    """
    quote added segments with '{+' and '+}', removed ones with '[-' and '-]'
    """
    line = ''
    for tag, i1, i2, j1, j2 in seqmatcher.get_opcodes():
        if tag == 'replace' or tag == 'insert':
            line += '{+' + seqmatcher.b[j1:j2] + '+}'
        if tag == 'replace' or tag == 'delete':
            line += '[-' + seqmatcher.a[i1:i2] + '-]'
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
    compare text, keep the changes within one line
    """
    s = difflib.SequenceMatcher(
        a=a, b=b,
        isjunk=lambda x: x in ' \n',
        autojunk=False
    )
    return markdiff(s)


def splitdiff(a, b, addfmt, delfmt, newline, fast=False):
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

    return start + splitdiff(a=a, b=b,
                             addfmt=addfmt,
                             delfmt=delfmt,
                             newline='<br>\n',
                             fast=fast)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        print(htmldiff(open(sys.argv[1]).read(),
                       open(sys.argv[2]).read()))
    else:
        print('Please pass two plain text files as arguments')
else:
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
