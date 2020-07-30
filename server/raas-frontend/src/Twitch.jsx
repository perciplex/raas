import React from 'react';
import './App.css';

function Twitch() {
    return (<div id="twitch-player" className="position-sticky">
        <iframe title="twitch stream" src="https://player.twitch.tv/?channel=perciplex&muted=true&parent=raas.perciplex.com" width="100%" height="100%"
            frameBorder={0} scrolling="no" allowFullScreen={true}>
        </iframe>
    </div>

    );
}

export default Twitch;
