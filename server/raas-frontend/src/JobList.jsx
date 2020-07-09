import React from 'react';
import TimeAgo from 'javascript-time-ago'
import en from 'javascript-time-ago/locale/en'
import { Badge, Table } from 'react-bootstrap';



class JobList extends React.Component {
    constructor(props) {
        super(props);
        this.state = { queued: [], running: [], completed: [] };
        TimeAgo.addLocale(en)
        this.time_ago = new TimeAgo('en-US')
    }

    componentDidMount() {
        this.update()
        this.timerID = setInterval(
            () => this.update(),
            1000
        );
    }

    update() {
        fetch("job")
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        isLoaded: true,
                        queued: result.queued,
                        completed: result.completed,
                        running: result.running
                    });
                },
                (error) => {
                    this.setState({
                        isLoaded: true,
                        error
                    });
                }
            )
    }

    go_to_job_page(job) {
        window.document.location = `job/${job.id}`
    }

    get_job_row(job) {
        var badge_type = "";
        var text = job.status;

        var time = false;
        switch (job.status) {
            case "COMPLETED":
                badge_type = "success"
                time = job.end_time
                break;
            case "RUNNING":
                badge_type = "primary"
                text = ` ${text}@${job.hardware_name}`
                time = job.start_time
                break;
            case "QUEUED":
                badge_type = "warning"
                time = job.submit_time
                break;
            case "FAILED":
                badge_type = "danger"
                time = job.end_time
                break;
            default:
                badge_type = "warning"
                time = job.submit_time
        }
        return (
            <tr className="table-row clickable-row link" key={job.id} onClick={() => this.go_to_job_page(job)} >
                <td>{this.time_ago.format(Date.parse(time))}</td>
                <td>{job.git_user}</td>
                <td>{job.project_name}
                    <Badge pill variant={badge_type} className={"float-right"}>{text}</Badge>
                </td>
            </tr >
        )

    }

    render() {
        var jobs = this.state.queued.concat(this.state.running, this.state.completed)
        const listItems = jobs.map((job) => this.get_job_row(job));
        return (
            <Table hover striped>
                <thead>
                    <tr>
                        <th scope="col">time</th>
                        <th scope="col">user</th>
                        <th scope="col">project name</th>
                    </tr>
                </thead>
                <tbody id="jobs">
                    {listItems}
                </tbody>
            </Table>
        );

    }
}

export default JobList;


