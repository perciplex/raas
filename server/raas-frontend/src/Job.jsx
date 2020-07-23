import React from 'react';
import { Container, Row, Col, Card, Badge, Spinner, Media } from 'react-bootstrap';
import { withRouter } from 'react-router';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faListOl, faPlay, faFlagCheckered } from '@fortawesome/free-solid-svg-icons'
//import Plot from 'react-plotly.js';
import createPlotlyComponent from 'react-plotly.js/factory';
import Plotly from 'plotly.js-basic-dist';
import Slider, { Range } from 'rc-slider';
import 'rc-slider/assets/index.css';


import { Stage, Layer, Rect, Image, Circle } from 'react-konva';
import Konva from 'konva';
import clockwise from './clockwise.png'


import useImage from 'use-image';


const Plot = createPlotlyComponent(Plotly);


class Job extends React.Component {
    constructor(props) {
        super(props);

        this.plot = React.createRef();

        this.state = {
            id: props.match.params.jobId,
            obs: [[0], [0], [0], [0]],
            times: [],
            actions: [],
            rewards: [],
            stdout: "",
            submit_time: false,
            start_time: false,
            end_time: false,
            frame: 0,
            config: {},
            frames: [],
            layout: {},
            data: [],
            data_loaded: false,
            metadata_loaded: false
        }
    }

    getPendulum() {
        var angle = 0
        const width = 14
        const length = 120
        const window_width = 250
        const window_height = 500

        if (this.state.data_loaded) {
            angle = Math.PI + Math.atan2(this.state.obs[1][this.state.frame], this.state.obs[0][this.state.frame])
        }
        return <Stage width={window_width} height={window_height}>
            <Layer>
                <Rect
                    x={window_width / 2 - width / 2 * Math.cos(angle) + width / 2 * Math.sin(angle)}
                    y={window_height / 2 - width / 2 * Math.sin(angle) - width / 2 * Math.cos(angle)}
                    width={width}
                    height={length}
                    rotation={180 * angle / Math.PI}
                    fill="#ca4d4b"
                    cornerRadius={width / 2}
                />
                <Circle
                    x={window_width / 2}
                    y={window_height / 2}
                    fill="#000200"
                    radius={width / 4}
                />
            </Layer>
        </Stage>
    }

    changeSliderValue = (new_value) => {
        this.setState({ frame: new_value })
    }

    componentDidMount() {
        this.update()
        this.timerID = setInterval(
            () => {
                if (this.state.end_time === false) {
                    this.update()
                }
            },
            5000
        );
    }

    update() {
        fetch(`/api/job/${this.state.id}`)
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
                job.metadata_loaded = true
                this.setState(job)
            })

        fetch(`https://raas-results.s3.us-east-2.amazonaws.com/run_results/${this.state.id}.json`)
            .then(res => res.json())
            .then(output => {
                output.times.shift()
                output.obs.shift()
                output.actions.shift()
                output.costs.shift()

                const t0 = output.times[0]
                output.times = output.times.map(t => t - t0);
                output.obs = output.obs[0].map((col, i) => output.obs.map(row => row[i]));
                output.data_loaded = true
                this.setState(output)

                this.setState({
                    data:
                        [
                            {
                                x: this.state.times,
                                y: this.state.costs,
                                type: 'scatter',
                                name: 'cost',
                            },
                            {
                                x: this.state.times,
                                y: this.state.actions,
                                type: 'scatter',
                                name: 'action',
                            },
                            {
                                x: this.state.times,
                                y: this.state.obs[0],
                                type: 'scatter',
                                name: 'y',
                            },
                            {
                                x: this.state.times,
                                y: this.state.obs[1],
                                type: 'scatter',
                                name: 'x',
                            },
                            {
                                x: this.state.times,
                                y: this.state.obs[2],
                                type: 'scatter',
                                name: 'dθ/dt',
                            },
                        ]
                })

                var seconds_per_frame = this.state.times / this.state.times.length

                setInterval(
                    () => {
                        var shapes = [{
                            type: 'line',
                            x0: this.state.times[this.state.frame],
                            x1: this.state.times[this.state.frame],
                            y0: 0,
                            y1: 1
                        }]


                        this.setState({
                            frame: (this.state.frame + 1) % (this.state.times.length - 1)
                        })
                        this.setState({
                            layout: {
                                margin: {
                                    l: 30,
                                    r: 0,
                                    b: 100,
                                    t: 10,
                                    pad: 0
                                },
                                height: 500,
                                legend: { orientation: "h" },
                                shapes: shapes

                            },
                        })
                    }, seconds_per_frame
                )
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
                                <Row>
                                    <Col lg={9} md={12}>
                                        <Plot ref={this.plot} id="plot" className="plot"
                                            data={this.state.data}
                                            layout={this.state.layout}
                                            frames={this.state.frames}
                                            config={this.state.config}
                                            onInitialized={(figure) => this.setState(figure)}
                                        />
                                    </Col>
                                    <Col lg={3} className="d-none d-lg-block">
                                        <center>
                                            {this.getPendulum()}

                                        </center>
                                    </Col>
                                </Row>
                                <Row>
                                    <Col>
                                        <Card.Text as="pre" dangerouslySetInnerHTML={{ __html: this.state.stdout.replace(/\\n/g, "<br/>").replace(/\\t/g, "	") }}>
                                        </Card.Text>
                                    </Col>
                                </Row>
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>
            </Container >
        );
    }
}

export default withRouter(Job);
