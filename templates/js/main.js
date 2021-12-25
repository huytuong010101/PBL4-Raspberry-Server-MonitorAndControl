JsLoadingOverlay.show()
axios.defaults.baseURL = `http://${HOST}:${PORT}`;
axios.interceptors.response.use(response => {
    return response; 
 }, error => {
    if (error.response && error.response.status === 401) {
        localStorage.setItem("msg", error.response.data.detail)
        window.location.href = "login"
    }
    return error;
 });
const socketService = new SocketService(`ws://${HOST}:${PORT}/${token}`)
socketService.init_socket()
/* Init data */
AppService.render_app()
FileService.render_file()
AdminService.render_user()
JsLoadingOverlay.hide()
/* Event assign*/
document.querySelector("#terminal-input").onkeydown = (event) => {
    if (event.key == "Enter"){
        const input = document.querySelector("#terminal-input")
        input.disabled = true
        try {
            socketService.execute_command(input.value.trim())
            input.value = ""
        } catch (e){
            toastr("Cannot execute command", "Terminal error")
        } finally {
            input.disabled = false
        }
        
    }
}

document.querySelector("#btn-cancel").onclick = async (event) => {
    try{
        socketService.cancel_command()
    } catch(e){
        toastr("Cannot execute command", "Terminal error")
    }
    
}

document.querySelector("#back-btn").onclick = async (event) => {
    await FileService.back_click()
}


document.querySelector("#make-dir-btn").onclick = async (event) => {
    await FileService.make_dir_click()
}

document.querySelector("#file-upload").onchange = async (event) => {
    await FileService.upload_file_event(event)
}

