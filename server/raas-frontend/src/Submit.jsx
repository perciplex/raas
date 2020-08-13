import React from 'react';
import JobForm from './JobForm.jsx'
import { Container, Row, Col, Card } from 'react-bootstrap';


function Submit() {
    return (
        <Container>
            <Row>
                <Col>
                    <Card>
                        <Card.Header>What do I do?</Card.Header>
                        <Card.Body>
                            Start by forking <a href="https://github.com/perciplex/raas-starter">our starter repository on GitHub</a>, or build your own repository. Either way, you must include <code>run.py</code> at the root directory. We use the same interface as OpenAI Gym with a <a href="https://github.com/perciplex/gym-raas">custom environment</a>.
                                <pre><code>
                                {`
                                 
import gym
import gym_raas

env = gym.make('raaspendulum-v0')
env.reset()

for _ in range(1000):
    env.render()
    env.step(env.action_space.sample()) # take a random action

env.close()`}
                            </code></pre>
                            When run locally, the above code performs a Gym simulation with physical parameters set to
                            match our hardware. When run at RaaS, the code controls an actual robot!
                        </Card.Body>
                    </Card>
                </Col>
                <Col>
                    <JobForm></JobForm>
                </Col>
            </Row>
        </Container>
    );
}

export default Submit;
