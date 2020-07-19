import React from 'react';
import HardwareList from './HardwareList.jsx'
import Twitch from './Twitch.jsx'
import './App.css';
import { Container, Row, Col } from 'react-bootstrap';


function Hardware() {
    return (
        <Container>
            <Row>
                <Col md={6} sm={12}>
                    <HardwareList></HardwareList>
                </Col>
                <Col md={6} className="d-none d-md-block">
                    <Twitch></Twitch>
                </Col>
            </Row>
        </Container>
    );
}

export default Hardware;
