import React from 'react';
import HardwareList from './HardwareList.jsx'
import Twitch from './Twitch.jsx'
import './App.css';
import { Container, Row, Col } from 'react-bootstrap';


function Hardware() {
    return (
        <Container>
            <Row>
                <Col>
                    <HardwareList></HardwareList>
                </Col>
                <Col>
                    <Twitch></Twitch>
                </Col>
            </Row>
        </Container>
    );
}

export default Hardware;
