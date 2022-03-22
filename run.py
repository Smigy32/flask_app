from app.__init__ import init_app

if __name__ == '__main__':
    init_app().run(debug=True, port=5000, host='0.0.0.0')

