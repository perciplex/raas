import React from 'react';
import { Col, Button, Form, InputGroup, Alert } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faGithub } from '@fortawesome/free-brands-svg-icons'


class JobForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = { git_url: '', git_user: '', project_name: '', valid: false, error: "" };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    resetState(error) {
        this.setState({ git_url: '', git_user: '', project_name: '', valid: false, error: error });
    }

    handleChange(event) {
        var re = RegExp('^(?:https://|http://)?(?:www.)?github.com/([a-zA-Z0-9-_]*)/([a-zA-Z0-9-_]*)(?:/)?(?:.git)?$')

        var git_user
        var project_name

        var github_url_candidate = event.target.value
        if (re.test(github_url_candidate)) {
            var groups = github_url_candidate.match(re)

            git_user = groups[1]
            project_name = groups[2]

            this.setState({
                git_url: groups[0],
                git_user: git_user,
                project_name: project_name,
                error: "none",
                valid: true
            });
        } else {
            this.resetState("invalid_url")
            return
        }
        fetch(`https://raw.githubusercontent.com/${git_user}/${project_name}/master/run.py`)
            .then(
                (result) => {
                    console.log(result)
                    if (result.ok) {
                        this.setState({
                            valid: true,
                            error: "none"
                        })
                    } else {
                        this.setState({
                            valid: false,
                            error: "repo_not_found"
                        });
                    }
                }
            ).catch(
                (error) => {
                    this.setState({
                        valid: false,
                        error: "unknown"
                    });
                }
            )

    }

    run_exists(files) {
        // returns if the file list contains run.py
        var found = false;
        for (var i = 0, len = files.length; i < len; i++) {
            if (files[i].path === "run.py") {
                found = true;
            }
        }
        return found
    }

    handleSubmit(event) {
        event.preventDefault();
        var form_data = new FormData();

        for (var key in this.state) {
            form_data.append(key, this.state[key]);
        }

        fetch('/api/job', {
            method: 'POST',
            body: form_data,
        });
        window.document.location = "/"
    }

    render() {
        return (
            <Form noValidate onSubmit={this.handleSubmit} validated={this.state.valid}>
                <Form.Row>
                    <Form.Group as={Col} md={12}>
                        <Form.Label>git repository</Form.Label>
                        <InputGroup>
                            <InputGroup.Prepend>
                                <InputGroup.Text><FontAwesomeIcon icon={faGithub} /></InputGroup.Text>
                            </InputGroup.Prepend>
                            <Form.Control
                                placeholder="GitHub url"
                                id="github-input"
                                name="git_url"
                                onChange={this.handleChange}></Form.Control>
                        </InputGroup>
                    </Form.Group>
                </Form.Row>
                <Form.Row>
                    <Form.Group as={Col} md={6}>
                        <Form.Label>username</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="GitHub username"
                            readOnly
                            value={this.state.git_user}></Form.Control>
                    </Form.Group>
                    <Form.Group as={Col} md={6}>
                        <Form.Label>project name</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="GitHub repo name"
                            readOnly
                            value={this.state.project_name}></Form.Control>
                    </Form.Group>
                </Form.Row>
                <Button type="submit" className="btn btn-primary float-right" id="submit" disabled={!this.state.valid}>
                    <span id="submit-word">Submit</span>
                </Button>

                {this.state.valid && <Alert variant={'success'} className="float-left"> looks ready to go! </Alert>}
                {this.state.error === "invalid_url" && <Alert variant={'danger'} className="float-left">please enter a valid repository url</Alert>}
                {this.state.error === "repo_not_found" && <Alert variant={'danger'} className="float-left">repository or <code>run.py</code> not found</Alert>}
                {this.state.error === "no_run" && <Alert variant={'danger'} className="float-left">please check repository structure</Alert>}

            </Form>
        );
    }
}

export default JobForm;
