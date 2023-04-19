import argparse
from docdiff import wrap_htmldiff, wrap_splitdiff


def flask_app():
    from flask import Flask, request, send_file

    app = Flask('docdiff')

    @app.route('/')
    def index():
        return send_file('index.html')

    @app.route('/docdiff.html')
    def docdiff_page():
        return send_file('docdiff.html')

    @app.route('/docdiff_result', methods=['POST'])
    def process_file():
        return wrap_htmldiff(request)

    @app.route('/docdiff.html')
    def tablegen_page():
        return send_file('docdiff.html')

    return app


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("old", help="Old file")
    parser.add_argument("new", help="New file")
    parser.add_argument("-l", "--line", action="store_true",
                        help="Fast line-by-line comparison")
    parser.add_argument("-r", "--run-flask", action="store_true",
                        help="Run built-in flask app in terminal")
    args = parser.parse_args()
    if not args.run_flask:
        print(wrap_splitdiff(args.old, args.new, args.line))
    else:
        flask_app().run(debug=True)
else:
    app = flask_app()
