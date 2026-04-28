import { useEffect, useRef, useState, useCallback } from 'react';
import { io } from 'socket.io-client';
import { ON } from '../utils/socketEvents';

const SOCKET_URL = 'http://localhost:5000';

/**
 * Hook custom pour gérer la connexion Socket.IO.
 * Retourne le socket, l'état de connexion et les fonctions utilitaires.
 */
export function useSocket() {
  const socketRef = useRef(null);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const socket = io(SOCKET_URL, {
      transports: ['websocket', 'polling'],
      autoConnect: true,
    });

    socketRef.current = socket;

    socket.on('connect', () => {
      console.log('✅ Connecté au serveur');
      setIsConnected(true);
      setError(null);
    });

    socket.on('disconnect', () => {
      console.log('❌ Déconnecté du serveur');
      setIsConnected(false);
    });

    socket.on(ON.CONNECTION_SUCCESS, (data) => {
      console.log('🔑 Session ID:', data.sid);
    });

    socket.on(ON.ERROR, (data) => {
      console.error('⚠️ Erreur serveur:', data.message);
      setError(data.message);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  /**
   * Émet un événement vers le serveur.
   */
  const emit = useCallback((event, data) => {
    if (socketRef.current) {
      socketRef.current.emit(event, data);
    }
  }, []);

  /**
   * S'abonne à un événement du serveur. Retourne une fonction de nettoyage.
   */
  const on = useCallback((event, callback) => {
    if (socketRef.current) {
      socketRef.current.on(event, callback);
      return () => socketRef.current.off(event, callback);
    }
  }, []);

  return {
    socket: socketRef.current,
    isConnected,
    error,
    emit,
    on,
  };
}
