export const connectMarketWS = (onMessage) => {
    const socket = new WebSocket("ws://localhost:8000/ws/market");

    socket.onmessage = (event) => {
        onMessage(JSON.parse(event.data));
    };

    return socket;
};