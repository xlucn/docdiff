import os
from subprocess import run, PIPE
from flask import Flask, request, send_file

app = Flask("Latex")


@app.route('/')
def hello_world():
    return send_file('docdiff.html')


@app.route('/doc-compare', methods=['POST', 'GET'])
def process_file():
    assert request.method == 'POST'
    print(request.files.keys(), request.values.get('getpdf'), request.values.get('gettex'))

    request.files['old'].save('old_file.txt')
    request.files['new'].save('new_file.txt')

    result = run([
        'gitdiff2pdf', '-cm', '-o', 'diff.tex',
        '-f', 'old_file.txt', 'new_file.txt'
    ], stdout=PIPE, stderr=PIPE)
    if result.returncode != 0 or os.path.exists('output/diff.pdf'):
        return '<code>{}</code>'.format(result.stderr)

    return send_file('output/diff.pdf')


if __name__ == '__main__':
    app.run(host='::', port=9000, debug=False)
