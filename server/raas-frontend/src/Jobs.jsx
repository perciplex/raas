import React from 'react';
import JobList from './JobList.jsx'
import './App.css';
import { Container, Image, Row, Col, Jumbotron, Button } from 'react-bootstrap';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
} from "react-router-dom";

function TwoColumn() {
    return (
        <Container id="content-container">
            <Jumbotron id="info">
                <h3 className="display-4">Reality as a Service</h3>
                <p>
                    We built real-life versions of the OpenAI Gym environments, and you can use them! To start, fork <a href="https://github.com/perciplex/raas-starter">our starter repository on GitHub</a> and edit <code>run.py</code>. <Link to="/status">Our robots</Link> use the same Gym interface you're used to. Just import our custom environment and you're ready to go.</p>
            </Jumbotron>
            <Row>
                <Col>
                    <JobList></JobList>
                </Col>
                <Col>
                    <Link to="/submit"><Button block>
                        Try it out for yourself!
                    </Button></Link>

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
