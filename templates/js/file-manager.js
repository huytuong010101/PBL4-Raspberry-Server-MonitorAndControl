class FileService {
    static async get_all_file(dir_path){
        let error = null
        let res = null
        try {
            res = await axios.get(`/files/`, {
                params: {
                    "base_path": dir_path
                }
            })
        } catch (err){
            if (err.response){
                error = err.response.data.detail
            } else {
                error = "Lỗi không xác định"
            }
        } finally{
            if (res.response && res.response.status >= 400){
                error = res.response.data.detail
            }
            return [error, res.data]
        }
        
    }

    static async rename_file(file_path, new_name){
        let error = null
        let res = null;
        try {
            res = await axios.put(`/files/`, {
                "name": new_name,
                "path": file_path
            })
        } catch (err){
            if (err.response){
                error = err.response.data.detail
            } else {
                error = "Lỗi không xác định"
            } 
        } finally {
            if (res.response && res.response.status >= 400){
                error = res.response.data.detail
            }
            return error
        }
        
    }

    static async delete_file(file_path){
        let error = null
        let res = null
        try {
            res = await axios.delete(`/files/${file_path}`)
        } catch (err){
            if (err.response){
                error = err.response.data.detail
            } else {
                error = "Lỗi không xác định"
            }   
        } finally {
            if (res.response && res.response.status >= 400){
                error = res.response.data.detail
            }
            return error
        }
        
    }

    static async create_dir(base_path, dir_name){
        let error = null
        let res = null
        try {
            res = await axios.post(`/files/dir`, {base_path, dir_name})
        } catch (err){
            if (err.response){
                error = err.response.data.detail
            } else {
                error = "Lỗi không xác định"
            }
        } finally {
            if (res.response && res.response.status >= 400){
                error = res.response.data.detail
            }
            return error
        }
        
    }

    static async upload_file(base_path, file){
        let error = null
        let res = null
        try {
            const formData = new FormData()
            formData.append("file", file)
            res = await axios.post(
                `/files/upload_file?base_path=${base_path}`, 
                formData, 
                {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                }
            )
        } catch (err){
            if (err.response){
                error = err.response.data.detail
            } else {
                error = "Lỗi không xác định"
            }
            
        } finally {
            if (res.response && res.response.status >= 400){
                error = res.response.data.detail
            }
            return error
        }
        
    }

    static async render_file(path="/"){
        const [error, files] = await FileService.get_all_file(path) 
        if (error != null){
            toastr.error(error, "Load error")
            await FileService.back_click()
            return;
        }
        let html = ""
        files.forEach(item => {
            if (item.type == "dir"){
                html += 
                `<div class="col-3 col-md-4 col-sm-12">
                    <div class="folder-container">
                        <div class="folder-top">
                            <i class='bx bxs-folder folder-icon' ></i>
                            <div class="folder-options">
                                <select data-file="${item.name}" onchange="FileService.action_file(this)" class="folder-select" name="folder-select" id="">
                                    <option class="folder-select" value="">Action</option>
                                    <option class="folder-select" value="remove">Remove</option>
                                    <option class="folder-select" value="rename">Rename</option>
                                </select>
                            </div>
                        </div>
                        <div class="folder-content" onclick="FileService.dir_click('${item.name}')">
                            <div class="folder-name">
                                ${item.name}
                            </div>
                            <div class="folder-date">
                                ${new Date(item.modified_at).toLocaleString()}
                            </div>
                        </div>     
                    </div>
                </div>`
            } else {
                html +=
                `<div class="col-3 col-md-4 col-sm-12">
                    <div class="folder-container">
                        <div class="folder-top">
                            <i class='bx bxs-file-blank file-icon'></i>
                            <div class="folder-options">
                                <select data-file="${item.name}" onchange="FileService.action_file(this)" class="folder-select" name="folder-select" id="">
                                    <option class="folder-select" value="">Action</option>
                                    <option class="folder-select" value="download">Download</option>
                                    <option class="folder-select" value="remove">Remove</option>
                                    <option class="folder-select" value="rename">Rename</option>
                                </select>
                            </div>
                        </div>
                        <div class="folder-content">
                            <div class="folder-name">
                                ${item.name}
                            </div>
                            <div class="folder-date">
                                ${new Date(item.modified_at).toLocaleString()}
                            </div>
                        </div>     
                    </div>
                </div>`
            }
        })
        document.querySelector("#list-file").innerHTML = html
    }
    static async dir_click(name){
        JsLoadingOverlay.show()
        const current_path = document.querySelector("#current-path").innerText
        const new_path = current_path + "/" + name
        document.querySelector("#current-path").innerText = new_path
        await FileService.render_file(new_path)
        JsLoadingOverlay.hide()
    }

    static async back_click(){
        const current_path = document.querySelector("#current-path").innerText
        if (current_path.length == 1){
            toastr.info("You are at the roor", "File info")
            return 
        }
        const new_path = current_path.slice(0, current_path.lastIndexOf("/"))
        document.querySelector("#current-path").innerText = new_path
        JsLoadingOverlay.show()
        await FileService.render_file(new_path)
        JsLoadingOverlay.hide()
    }

    static async action_file(event){
        const current_path = document.querySelector("#current-path").innerText
        const path = current_path + "/" + event.dataset.file
        let error = null;
        switch (event.value){
            case "remove":
                if (!confirm("This actiuon cannot ctrl z, are you suare?")){
                    event.selectedIndex = 0
                    return;
                }
                JsLoadingOverlay.show()
                error = await FileService.delete_file(path)
                JsLoadingOverlay.hide()
                if (error){
                    toastr.error(error, "Delete error")
                } else {
                    await FileService.render_file(current_path)
                    toastr.success("The file was removed", "Delete success")
                }
                break
            case "rename":
                const new_name = prompt("Type new name").trim()
                JsLoadingOverlay.show()
                error = await FileService.rename_file(path, new_name)
                JsLoadingOverlay.hide()
                if (error){
                    toastr.error(error, "Rename error")
                } else {
                    await FileService.render_file(current_path)
                    toastr.success("The file was rename to " + new_name, "Rename success")
                }
                break
            case "download":
                const [err, token] = await FileService.create_downlaod_token(path)
                if (error){
                    toastr.error(err, "Download error")
                } else {
                    window.open(`http://${HOST}:${PORT}/files/stream-file/${token}`, "_black").focus()
                }
                event.selectedIndex = 0
                break
            default:
                break
        }
    }

    static async create_downlaod_token(path){
        let error = null
        let res = null;
        try {
            res = await axios.get(`/files/download/${path}`)
        } catch (err){
            if (err.response){
                error = err.response.data.detail
            } else {
                error = "Lỗi không xác định"
            } 
        } finally {
            console.log(res.response)
            if (res.response && res.response.status >= 400){
                error = res.response.data.detail
            }
            return [error, res.data]
        }
    }
    static async make_dir_click(){
        const name = prompt("Type directory name")
        if (!name) return;
        const current_path = document.querySelector("#current-path").innerText
        JsLoadingOverlay.show()
        const error = await FileService.create_dir(current_path, name)
        JsLoadingOverlay.hide()
        if (error){
            toastr.error(error, "Create error")
        } else {
            await FileService.render_file(current_path)
            toastr.success("The directory was created", "Create success")
        }
    }

    static async upload_file_event(event){
        const file = event.target.files[0]
        if (!confirm(`Are you sure to upload ${file.name} to current directory?`)) return;
        const current_path = document.querySelector("#current-path").innerText
        JsLoadingOverlay.show()
        const error = await FileService.upload_file(current_path, file)
        JsLoadingOverlay.hide()
        if (error){
            toastr.error(error, "Upload error")
        } else {
            await FileService.render_file(current_path)
            toastr.success("The file was uploaded", "Upload success")
        }
    }
}