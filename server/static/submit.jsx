'use strict';

const e = React.createElement;


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
        var re = RegExp('^(?:https:\/\/|http:\/\/|)(?:www.|)github.com\/([a-z0-9]*)\/([a-z0-9-_]*)(?:\/|)(?:.git|)$')

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
        /*
        fetch(`https://api.github.com/repos/${git_user}/${project_name}/contents`)
            .then(
                (result) => {
                    console.log(result)
                    if (result.ok) {
                        result.json().then((data) => {
                            if (!this.run_exists(data)) {
                                this.setState({
                                    valid: false,
                                    error: "no_run"
                                });
                            } else {
                                this.setState({
                                    valid: true,
                                    error: "none"
                                });
                            }
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
            */

    }

    run_exists(files) {
        // returns if the file list contains run.py
        var found = false;
        for (var i = 0, len = files.length; i < len; i++) {
            if (files[i].path == "run.py") {
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

        fetch('/job', {
            method: 'POST',
            body: form_data,
        });
        window.document.location = "/"
    }

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <div className="form-row">
                    <div className="form-group col-md-12">
                        <label className="form-control-label">git repository</label>
                        <div className="input-group mb-2">
                            <div className="input-group-prepend">
                                <div className="input-group-text"><i className="fa fa-lg fa-github"></i></div>
                            </div>
                            <input type="text" placeholder="GitHub url" className="form-control" id="github-input"
                                name="git_url" onChange={this.handleChange}></input>

                        </div>
                    </div>
                </div>
                <div className="form-row">

                    <div className="form-group col-md-6">
                        <label className="control-label" >username</label>
                        <input className="form-control" id="username" type="text" placeholder="GitHub username"
                            readOnly name="git_user" value={this.state.git_user}></input>
                    </div>

                    <div className="form-group col-md-6">
                        <label className="control-label" >project name</label>
                        <input className="form-control" id="name" type="text" placeholder="GitHub repo name"
                            readOnly name="project_name" value={this.state.project_name}></input>
                    </div>
                </div>
                <button type="submit" className="btn btn-primary float-right" id="submit" disabled={!this.state.valid}>
                    <span id="submit-word">Submit</span>
                </button>

                <div id="valid" className="feedback float-left text-success" style={{ display: this.state.valid ? "float" : "none" }}>looks ready to go! </div>
                <div id="invalid-url" className="feedback float-left text-danger" style={{ display: this.state.error == "invalid_url" ? "float" : "none" }}>please enter a valid repository url</div>
                <div id="invalid-not-found" className="feedback float-left text-danger" style={{ display: this.state.error == "repo_not_found" ? "float" : "none" }}>GitHub repository not found
                        </div>
                <div id="invalid-git" className="feedback float-left text-danger" style={{ display: this.state.error == "no_run" ? "float" : "none" }}>please check repository structure
                        </div>

            </form>
        );
    }
}


const domContainer = document.querySelector('#hardware_form');
ReactDOM.render(e(JobForm), domContainer);