from flaskr import create_app, socketio

app = create_app()

if __name__ == '__main__':
    print("🏰 Tower Defense — Serveur démarré sur http://localhost:5000")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
