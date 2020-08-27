import React from 'react';
import JobList from './JobList.jsx'
import Twitch from './Twitch.jsx'

import './App.css';
import { Container, Row, Col, Jumbotron, Button } from 'react-bootstrap';
import {
    Link
} from "react-router-dom";

function TwoColumn() {
    return (
        <Container id="content-container">
            <Jumbotron id="info">
                <h3 className="display-4">Reality as a Service</h3>
                <p>
                    We built real-life versions of the OpenAI Gym environments, and you can use them! To start, fork <a href="https://github.com/perciplex/raas-starter">our starter repository on GitHub</a> and build your controller inside <code>run.py</code>. <Link to="/status">Our robots</Link> use the same Gym interface you're used to. Just import our custom environment and you're ready to go. Check out <a href="https://perciplex.github.io/raas/">our documentation</a> for more info.</p>
            </Jumbotron>
            <Row>
                <Col md={6} sm={12}>
                    <JobList></JobList>
                </Col>
                <Col md={6} className="d-none d-md-block">
                    <Link to="/submit"><Button size="lg" block>
                        Try it out for yourself!
                    </Button></Link>
                    <Twitch></Twitch>
                </Col>
            </Row>
        </Container>
    );
}

export default TwoColumn;
