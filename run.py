from flaskr import create_app, socketio

app = create_app()

if __name__ == '__main__':
    print("🏰 Tower Defense — Serveur démarré sur http://localhost:5001")
    socketio.run(app, debug=True, host='127.0.0.1', port=5001)
