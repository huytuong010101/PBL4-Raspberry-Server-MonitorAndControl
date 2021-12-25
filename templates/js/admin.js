class AdminService {
    static async get_all_user() {
        let error = null
        let users = null
        try {
            const res = await axios.get(`/user`)
            users = res.data

        } catch (err) {
            if (err.response) {
                error = err.response.data.detail
            } else {
                error = "Lỗi không xác định"
            }

        } finally {
            return [error, users]
        }
    }

    static async load_user_update(username) {
        let error = null
        let profile = null
        try {
            const res = await axios.get(`/user/${username}`)
            profile = res.data
        } catch (err) {
            if (err.response) {
                error = err.response.data.detail
            } else {
                error = "Lỗi không xác định"
            }
        } finally {
            if (error) toastr.error(error, "Load profile user error")
            else {
                document.querySelector("#update-username").value = profile.username
                document.querySelector("#update-fullname").value = profile.fullname
                document.querySelector("#update-email").value = profile.email
                document.querySelector("#update-is-admin").checked = profile.is_admin
                document.querySelector("#update-created_at").innerText = profile.created_at
            }
        }
    }

    static async render_user() {
        let content = ""
        const [errors, users] = await AdminService.get_all_user()
        if (errors) {
            alert(errors)
        } else {
            content +=
                `<tr class="user-tr">
                    <th>Username</th>
                    <th>Fullname</th>
                    <th>Email</th>
                    <th>Created at</th>
                    <th>Modify</th>
                </tr>`;
            users.forEach(item => {
                content +=
                    `<tr>
                        <td>${item.username}</td>
                        <td>${item.fullname}</td>
                        <td>${item.email}</td>
                        <td>${item.created_at}</td>
                        <td>
                            <a href="#" class="btn-user btn-update" onclick="updateUser(event, '${item.username}')">Update</a>
                            <a href="#" class="btn-user btn-delete" data-toggle="modal" onclick="deleteUser(event, '${item.username}')">
                                Delete
                            </a>
                        </td>
                    </tr>`
            })

            document.querySelector(".user-table").innerHTML = content
        }
    }

}


// Update modal
const modalProfileUser = document.querySelector('.modal-user');
const profileUser = document.querySelector('.profile-user');
const closeModalProfileUser = document.querySelector('.close-profile-user');
const addUserBtn = document.querySelector('.btn-add');

closeModalProfileUser.onclick = () => {
    modalProfileUser.classList.add('hide');
}

profileUser.onclick = (e) => {
    e.stopImmediatePropagation();
}

modalProfileUser.onclick = () => {
    modalProfileUser.classList.add('hide');
}

// Add modal
const modalProfileAddUser = document.querySelector('.modal-add-user');
const profileAddUser = document.querySelector('.profile-add-user');
const closeModalProfileAddUser = document.querySelector('.close-profile-add-user');
const addNewUserBtn = document.querySelector('.btn-add');

closeModalProfileAddUser.onclick = () => {
    modalProfileAddUser.classList.add('hide');
}

profileAddUser.onclick = (e) => {
    e.stopImmediatePropagation();
}

modalProfileAddUser.onclick = () => {
    modalProfileUser.classList.add('hide');
}

addNewUserBtn.onclick = (e) => {
    e.preventDefault();
    modalProfileAddUser.classList.remove('hide');
    Validator({
        form: '#add-user-form',
        formGroupSelector: '.profile-info__group',
        errorSelector: '.error-message',
        rules: [
            Validator.isRequired('#add-username', 'Please enter your username!'),
            Validator.minLength('#add-username', 5, 'Username'),
            Validator.isRequired('#add-fullname', 'Please enter your fullname!'),
            Validator.isRequired('#add-email'),
            Validator.isEmail('#add-email'),
            Validator.isRequired('#add-pwd'),
            Validator.minLength('#add-pwd', 5, 'Password'),
            Validator.isRequired('#add-re-pwd'),
            Validator.isConfirmed('#add-re-pwd', function () {
                return document.querySelector('#add-user-form #add-pwd').value;
            }, 'Password'),
        ],
        onsubmit: addUser,
    });
}

async function addUser(event) {
    event.preventDefault()
    let error = null
    let res = null
    try {
        let username = document.querySelector("#add-username").value.trim()
        let fullname = document.querySelector("#add-fullname").value.trim()
        let avatar = ""
        let email = document.querySelector("#add-email").value.trim()
        let is_admin = document.querySelector("#add-is-admin").checked
        let password = document.querySelector("#add-pwd").value.trim()
        res = await axios.post(`/user`, {
            username,
            fullname,
            avatar,
            email,
            is_admin,
            password,
        })
    } catch (err) {
        if (err.response) {
            error = err.response.data.detail
        } else {
            error = "Lỗi không xác định"
        }
    } finally {
        JsLoadingOverlay.hide()
        if (res.response && res.response.status >= 400) {
            showError(res.response.data.detail, "Add error")
            return;
        }
        if (error) toastr.error(error, "Add error")
        else {
            toastr.success("Add user successful", "Add success")
            AdminService.render_user()
            document.querySelector('#add-user-form').focus();
            document.querySelector('#add-user-form').reset();
        }
    }
}

async function updateUser(event, username) {
    event.preventDefault();
    modalProfileUser.classList.remove('hide');
    JsLoadingOverlay.show()
    await AdminService.load_user_update(username);
    JsLoadingOverlay.hide()
    Validator({
        form: '#update-info-form',
        formGroupSelector: '.profile-info__group',
        errorSelector: '.error-message',
        rules: [
            Validator.isRequired('#update-fullname', 'Please enter your fullname!'),
            Validator.isRequired('#update-email'),
            Validator.isEmail('#update-email'),
        ],
    });
    Validator({
        form: '#change-password-form',
        formGroupSelector: '.profile-info__group',
        errorSelector: '.error-message',
        rules: [
            Validator.isRequired('#update-new-pwd'),
            Validator.minLength('#update-new-pwd', 5, 'Password'),
            Validator.isRequired('#update-re-pwd'),
            Validator.isConfirmed('#update-re-pwd', function () {
                return document.querySelector('#change-password-form #update-new-pwd').value;
            }, 'Password'),
        ],
    });

    document.querySelector("#update-btn-save-profile").onclick = async (event) => {
        JsLoadingOverlay.show()
        event.preventDefault()
        let error = null
        let res = null
        try {
            const data = {
                "username": username,
                "fullname": document.querySelector("#update-fullname").value.trim(),
                "email": document.querySelector("#update-email").value.trim(),
                "is_admin": document.querySelector("#update-is-admin").checked
            }
            res = await axios.put(`/user/${username}`, data)
        } catch (err) {
            if (err.response) {
                error = err.response.data.detail
            } else {
                error = "Lỗi không xác định"
            }
        } finally {
            JsLoadingOverlay.hide()
            if (res.response && res.response.status >= 400) {
                showError(res.response.data.detail, "Update error")
                return;
            }
            if (error) toastr.error(error, "Update error")
            else {
                toastr.success("This user was updated", "Update success")
                AdminService.render_user()
                document.querySelector('#update-info-form').focus();
                document.querySelector('#update-info-form').reset();
                modalProfileUser.classList.add('hide')
            }
        }
    }

    document.querySelector("#update-btn-change-password").onclick = async (event) => {
        JsLoadingOverlay.show()
        event.preventDefault()
        let error = null
        let res = null
        try {
            const data = {
                "old_password": "",
                "new_password": document.querySelector("#update-new-pwd").value.trim(),
            }
            res = await axios.put(`/user/${username}/change-password`, data)
        } catch (err) {
            if (err.response) {
                error = err.response.data.detail
            } else {
                error = "Lỗi không xác định"
            }
        } finally {
            JsLoadingOverlay.hide()
            if (res.response && res.response.status >= 400) {
                showError(res.response.data.detail, "Update error")
                return;
            }
            if (error) toastr.error(error, "Update error")
            else {
                toastr.success("This user was updated", "Update success")
                AdminService.render_user()
                document.querySelector('#update-info-form').focus();
                document.querySelector('#update-info-form').reset();
                modalProfileUser.classList.add('hide')
            }
        }

    }

}


function deleteUser(event, username) {
    event.preventDefault();
    swal({
            title: "Are you sure?",
            text: "Once deleted, you will not be able to recover this user!",
            icon: "warning",
            buttons: true,
            dangerMode: true,
        })
        .then(async (willDelete) => {
            if (willDelete) {
                let error = null
                let res = null
                try {
                    res = await axios.delete(`/user/${username}`)
                } catch (err) {
                    if (err.response) {
                        error = err.response.data.detail
                    } else {
                        error = "Lỗi không xác định"
                    }
                } finally {
                    JsLoadingOverlay.hide()
                    if (res.response && res.response.status >= 400) {
                        showError(res.response.data.detail, "Delete error")
                        return;
                    }
                    if (error) toastr.error(error, "Delete error")
                    else {
                        swal("Poof! This user has been deleted!", {
                            icon: "success",
                        });
                        AdminService.render_user()
                    }
                }
            } else {
                swal("This user is safe!");
            }
        });

}


// Tracking ---------------------------------------------------------------------------------------
document.querySelector("#btn-filter-action").onclick = async () => {
    JsLoadingOverlay.show()
    let error = null
    let res = null;
    try {
        const start = document.querySelector("#time-start-action").value
        const end = document.querySelector("#time-end-action").value
        const data = {
            "start_time": start ? start : null,
            "end_time": end ? end : null
        }
        res = await axios.get(`/tracking/action-tracking`, {
            params: data
        })
    } catch (err) {
        if (err.response) {
            error = err.response.data.detail
        } else {
            error = "Lỗi không xác định"
        }
    } finally {
        JsLoadingOverlay.hide()
        if (res != null && res.response && res.response.status >= 400) {
            showError(res.response.data.detail, "Get error")
            return;
        }
        if (error) toastr.error(error, "Update error")
        else {
            document.querySelector('#table-action-content').classList.add('active');
            const table = document.querySelector("#table-action")
            table.innerHTML = ""
            let html = `
            <thead>
                <tr>
                    <th>Action ID</th>
                    <th>Time</th>
                    <th>Action</th>
                    <th>User</th>
                </tr>
            </thead>
            <tbody>`;
            res.data.forEach(item => {
                html +=
                    `<tr class="user-tr">
                    <td>${item.act_id}</td>
                    <td>${item.time}</td>
                    <td>${item.action}</td>
                    <td>${item.user ? item.user.username : "Unknow"}</td>
                </tr>`
            })
            html += `</tbody>`;
            table.innerHTML = html
        }
    }
}

document.querySelector("#btn-filter-login").onclick = async () => {
    JsLoadingOverlay.show()
    let error = null
    let res = null;
    try {
        const start = document.querySelector("#time-start-login").value
        const end = document.querySelector("#time-end-login").value
        const data = {
            "start_time": start ? start : null,
            "end_time": end ? end : null
        }
        res = await axios.get(`/tracking/login-logs`, {
            params: data
        })
    } catch (err) {
        if (err.response) {
            error = err.response.data.detail
        } else {
            error = "Lỗi không xác định"
        }
    } finally {
        JsLoadingOverlay.hide()
        if (res != null && res.response && res.response.status >= 400) {
            showError(res.response.data.detail, "Get error")
            return;
        }
        if (error) toastr.error(error, "Update error")
        else {
            document.querySelector('#table-login-content').classList.add('active');
            const table = document.querySelector("#table-login")
            table.innerHTML = ""
            let html = `
            <thead>
                <tr>
                    <th>Time</th>
                    <th>Device</th>
                    <th>User (username)</th>
                </tr>
            </thead>
            <tbody>`
            res.data.forEach(item => {
                html +=
                    `<tr class="user-tr">
                    <td>${item.time}</td>
                    <td>${item.device}</td>
                    <td>${item.user ? item.user.username : "Unknow"}</td>
                </tr>`
            })
            html += `</tbody>`;
            table.innerHTML = html
        }
    }
}

const create_chart = async (x, y, id, name) => {
    // Line chart Network
    var options_linechart = {
        colors: ['#ff764d', '#E91E63'],
        series: y,
        chart: {
            foreColor: '#bc7ec2',
            height: 300,
            width: '300%',
            type: 'line',
            zoom: {
                enabled: false
            },
        },
        dataLabels: {
            enabled: false,
        },
        stroke: {
            width: [3, 3],
            curve: 'straight',
            dashArray: [0, 0, 0],
            colors: ['#ff764d', '#E91E63'],
        },
        title: {
            text: name,
            align: 'left',
        },
        legend: {
            tooltipHoverFormatter: function (val, opts) {
                return val + ' - ' + opts.w.globals.series[opts.seriesIndex][opts.dataPointIndex] + ''
            },
        },
        markers: {
            size: 0,
            hover: {
                sizeOffset: 5
            },
            colors: ['#ff764d', '#E91E63'],
        },
        xaxis: {
            color: '#888',
            axisBorder: {
                color: text_chart_color,
            },
            axisTicks: {
                borderType: 'solid',
                color: text_chart_color,
            },
            categories: x
        },
        tooltip: {
            y: [{
                    title: {
                        formatter: function (val) {
                            return val + " (times):"
                        }
                    }
                },
                {
                    title: {
                        formatter: function (val) {
                            return val + " (times):"
                        }
                    }
                },
            ]
        },
        grid: {
            borderColor: text_chart_color,
            strokeDashArray: 2,
        }
    };
    await new ApexCharts(document.querySelector(id), options_linechart).render();
}

document.querySelector("#btn-filter-resource").onclick = async () => {
    JsLoadingOverlay.show()
    let error = null
    let res = null;
    try {
        const start = document.querySelector("#time-start-resource").value
        const end = document.querySelector("#time-end-resource").value
        const data = {
            "start_time": start ? start : null,
            "end_time": end ? end : null
        }
        res = await axios.get(`/tracking/resource-tracking`, {
            params: data
        })
    } catch (err) {
        if (err.response) {
            error = err.response.data.detail
        } else {
            error = "Lỗi không xác định"
        }
    } finally {
        JsLoadingOverlay.hide()
        if (res != null && res.response && res.response.status >= 400) {
            showError(res.response.data.detail, "Get error")
            return;
        }
        if (error) toastr.error(error, "Update error")
        else {
            document.querySelector('#resoure-content').innerHTML = `
            <div class="col-12 col-md-12 col-sm-12">
                <div class="box box-hover">
                    <div id="linechart-cpu-log">
                    </div>
                </div>
            </div>
            <div class="col-12 col-md-12 col-sm-12">
                <div class="box box-hover">
                    <div id="linechart-network-log">
                    </div>
                </div>
            </div>`
            const y1 = [{
                    name: "CPU",
                    data: []
                },
                {
                    name: "Temperature",
                    data: []
                }
            ]
            const y2 = [{
                    name: "Network send",
                    data: []
                },
                {
                    name: "Network receive",
                    data: []
                }
            ]
            const x = []
            res.data.forEach(item => {
                if (item.cpu_percent) y1[0].data.push(item.cpu_percent)
                if (item.temperature_percent) y1[1].data.push(item.temperature_percent)
                if (item.network_send) y2[0].data.push(item.network_send)
                if (item.network_receive) y2[1].data.push(item.network_receive)
                x.push(item.time)

            })
            document.querySelector("#linechart-cpu-log").innerHTML = ""
            document.querySelector("#linechart-network-log").innerHTML = ""
            await create_chart(x, y1, "#linechart-cpu-log", "CPU performance & Temperaturer")
            await create_chart(x, y2, "#linechart-network-log", "Network traffics")
        }
    }
}