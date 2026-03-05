import { useState, useEffect, useRef, useCallback } from 'react';

export const useWebSocket = (url) => {
    const [data, setData] = useState(null);
    const [status, setStatus] = useState('connecting');
    const ws = useRef(null);

    const connect = useCallback(() => {
        setStatus('connecting');
        ws.current = new WebSocket(url);

        ws.current.onopen = () => {
            console.log('WebSocket Connected');
            setStatus('connected');
        };

        ws.current.onmessage = (event) => {
            const message = JSON.parse(event.data);
            if (message.error) {
                console.error('WebSocket Data Error:', message.error);
            } else {
                setData(message);
            }
        };

        ws.current.onclose = () => {
            console.log('WebSocket Disconnected');
            setStatus('disconnected');
            // Attempt to reconnect after 5 seconds
            setTimeout(connect, 5000);
        };

        ws.current.onerror = (error) => {
            console.error('WebSocket Error:', error);
            ws.current.close();
        };
    }, [url]);

    useEffect(() => {
        connect();
        return () => {
            if (ws.current) {
                ws.current.close();
            }
        };
    }, [connect]);

    return { data, status };
};
