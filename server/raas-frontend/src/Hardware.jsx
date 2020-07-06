import React from 'react';
import HardwareList from './HardwareList.jsx'
import './App.css';
import { Container, Image, Row, Col, Jumbotron } from 'react-bootstrap';


function TwoColumn() {
    return (
        <Container>
            <Row>
                <Col>
                    <HardwareList></HardwareList>
                </Col>
                <Col>
                    <div id="twitch-player" className="position-sticky">
                        <iframe src="https://player.twitch.tv/?channel=perciplex&muted=true" width="100%" height="100%"
                            frameBorder={0} scrolling="no" allowFullScreen={true}>
                        </iframe>
                    </div>
                </Col>
            </Row>
        </Container>
    );
}

export default TwoColumn;
