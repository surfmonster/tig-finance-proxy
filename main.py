from rest.poxy_controller import get_flask_app
import client.register

client.register.register_all()
app = get_flask_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
