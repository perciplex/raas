import React from 'react';

class HardwareList extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hardware: [] };
    }

    componentDidMount() {
        this.update()
        this.timerID = setInterval(
            () => this.update(),
            1000
        );
    }

    update() {
        fetch("hardware")
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        isLoaded: true,
                        hardware: result,
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

    get_hardware_row(hardware) {
        var badge_type = "";
        switch (hardware.status) {
            case "ONLINE":
                badge_type = "badge-success"
                break;
            case "OFFLINE":
                badge_type = "badge-warning"
                break;
            default:
                badge_type = "badge-warning"
        }

        return (
            <tr className="table-row" key={hardware.name}>
                <td>{hardware.name}
                    <span className={`float-right badge ${badge_type}`}>{hardware.status}</span>
                </td>
            </tr >
        )

    }

    render() {
        const listItems = this.state.hardware.map((hardware) => this.get_hardware_row(hardware));
        return (
            <table className="table table-hover table-striped table-body-scroll">
                <thead>
                    <tr>
                        <th scope="col">hardware status</th>
                    </tr>
                </thead>
                <tbody id="hardware">
                    {listItems}
                </tbody>
            </table>
        );

    }
}

export default HardwareList;
