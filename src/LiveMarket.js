import { useEffect, useState } from "react";
import { connectMarketWS } from "../services/wsClient";

function LiveMarket() {
    const [data, setData] = useState(null);

    useEffect(() => {
        const ws = connectMarketWS(setData);
        return () => ws.close();
    }, []);

    if (!data) return <p>Loading...</p>;

    return (
        <div>
            <h2>{data.symbol}</h2>
            <p>Price: {data.price}</p>
            <p>Prediction: {data.prediction}</p>
            <p>RMSE: {data.metrics.RMSE}</p>
            <p>{data.explanation}</p>
        </div>
    );
}

export default LiveMarket;
