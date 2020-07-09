import React from 'react';
import { Container, Row, Col, Card, Badge, Spinner } from 'react-bootstrap';
import { withRouter } from 'react-router';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faListOl, faPlay, faFlagCheckered } from '@fortawesome/free-solid-svg-icons'
//import Plot from 'react-plotly.js';
import createPlotlyComponent from 'react-plotly.js/factory';
import Plotly from 'plotly.js-basic-dist';
const Plot = createPlotlyComponent(Plotly);


class Job extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            id: props.match.params.jobId,
            obs: [],
            times: [],
            actions: [],
            rewards: [],
            stdout: "",
            submit_time: false,
            start_time: false,
            end_time: false,

        };
    }

    componentDidMount() {
        this.update()
        this.timerID = setInterval(
            () => this.update(),
            5000
        );
    }

    update() {
        fetch(`/job/${this.state.id}`)
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
                job.submit_time = this.date_to_string(job.submit_time)
                job.start_time = this.date_to_string(job.start_time)
                job.end_time = this.date_to_string(job.end_time)
                this.setState(job)
            })

        fetch(`https://raas-results.s3.us-east-2.amazonaws.com/run_results/${this.state.id}.json`)
            .then(res => res.json())
            .then(output => {
                const t0 = output.times[0]
                output.times = output.times.map(t => t - t0);
                output.obs = output.obs[0].map((col, i) => output.obs.map(row => row[i]));
                this.setState(output)
            })
            .catch(err => { })
    }

    date_to_string(date) {
        if (date === null) return false;
        return new Date(date).toLocaleString()
    }

    render() {
        return (
            <Container>

                <Row>
                    <Col>
                        <Card id="results" border={this.state.alert_variant}>
                            <Card.Header bg={this.state.alert_variant}>
                                <h4>{this.state.git_user}/{this.state.project_name}<span className="float-right">{this.state.status}@{this.state.hardware_name}</span></h4></Card.Header>
                            <Card.Body>
                                <Badge variant="warning" className="time-badge"><FontAwesomeIcon icon={faListOl} /> {this.state.submit_time || <Spinner animation="border" size="sm" />}</Badge>
                                <Badge variant="primary" className="time-badge"><FontAwesomeIcon icon={faPlay} /> {this.state.start_time || <Spinner animation="border" size="sm" />}</Badge>
                                <Badge variant="success" className="time-badge"><FontAwesomeIcon icon={faFlagCheckered} /> {this.state.end_time || <Spinner animation="border" size="sm" />}</Badge>
                                <Plot id="plot" className="plot"
                                    layout={{
                                        margin: {
                                            l: 30,
                                            r: 0,
                                            b: 100,
                                            t: 10,
                                            pad: 0
                                        }
                                    }}
                                    data={
                                        [
                                            {
                                                x: this.state.times,
                                                y: this.state.costs,
                                                type: 'scatter',
                                                name: 'costs',
                                            },
                                            {
                                                x: this.state.times,
                                                y: this.state.actions,
                                                type: 'scatter',
                                                name: 'actions',
                                            },
                                            {
                                                x: this.state.times,
                                                y: this.state.obs[0],
                                                type: 'scatter',
                                                name: 'x',
                                            },
                                            {
                                                x: this.state.times,
                                                y: this.state.obs[1],
                                                type: 'scatter',
                                                name: 'y',
                                            },
                                            {
                                                x: this.state.times,
                                                y: this.state.obs[2],
                                                type: 'scatter',
                                                name: 'z',
                                            },
                                        ]}
                                />
                                <Card.Text as="pre" dangerouslySetInnerHTML={{ __html: this.state.stdout.replace(/\\n/g, "<br/>").replace(/\\t/g, "	") }}>
                                </Card.Text>
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>
            </Container >
        );
    }
}

export default withRouter(Job);
