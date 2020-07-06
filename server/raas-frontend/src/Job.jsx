import React from 'react';
import { Container, Image, Row, Col, Card, Badge, Alert } from 'react-bootstrap';
import { withRouter } from 'react-router';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faListOl, faPlay, faFlagCheckered } from '@fortawesome/free-solid-svg-icons'
import Plot from 'react-plotly.js';



class Job extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            id: props.match.params.jobId,

        };
    }

    componentDidMount() {
        var data = fetch(`/job/${this.state.id}`)
            .then(res => res.json())
            .then(job => {
                var alert_variant = "danger";

                switch (job.status) {
                    case "COMPLETED":
                        alert_variant = "success"
                        break;
                    case "RUNNING":
                        alert_variant = "primary"
                        break;
                    case "QUEUED":
                        alert_variant = "warning"
                        break;
                    case "FAILED":
                        alert_variant = "danger"
                        break;
                    default:
                        alert_variant = "danger"
                }
                job.alert_variant = alert_variant
                this.setState(job)
            })

        var output = fetch(`https://raas-results.s3.us-east-2.amazonaws.com/run_results/${this.state.id}.json`)
            .then(res => res.json())
            .then(output => {
                console.log(output)
            })
    }

    render() {
        return (
            <Container>
                <Row>
                    <Col>
                        <Alert variant={this.state.alert_variant} id="job-status-bar">
                            <h4>
                                {this.state.status}
                                <span className="float-right">{this.state.hardware_name}</span>
                            </h4>
                        </Alert>
                    </Col>
                </Row>
                <Row>
                    <Col>
                        <Card>
                            <Card.Header>{this.state.git_user}<span className="float-right">{this.state.project_name}</span></Card.Header>
                            <Card.Body>
                                <Badge variant="warning"><FontAwesomeIcon icon={faListOl} /> {this.state.submit_time}</Badge>
                                <Badge variant="primary"><FontAwesomeIcon icon={faPlay} /> {this.state.start_time}</Badge>
                                <Badge variant="success"><FontAwesomeIcon icon={faFlagCheckered} /> {this.state.end_time}</Badge>
                            </Card.Body>
                        </Card>
                    </Col>
                    <Col>
                    </Col>
                </Row>
            </Container >
        );
    }
}

export default withRouter(Job);
