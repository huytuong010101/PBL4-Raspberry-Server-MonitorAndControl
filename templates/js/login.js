axios.defaults.baseURL = `http://${HOST}:${PORT}`;

const msg = localStorage.getItem("msg")
if (msg){
    toastr.info(msg, "Alert")
    localStorage.removeItem("msg")
} 

document.querySelector("#btn-login").onclick = async (event) => {
    event.preventDefault()
    let error = null
    let res = null
    try {
        const params = new URLSearchParams();
        params.append('username', document.querySelector("#username").value.trim());
        params.append('password', document.querySelector("#password").value);
        res = await axios.post("/token", params)
    } catch (err){
        if (err.response){
            error = err.response.data.detail
        } else {
            error = "Lỗi không xác định"
        }
    } finally {
        if (error) toastr.error(error, "Login fail")
        else {
            localStorage.setItem("token", res.data.token_type + " " + res.data.access_token)
            window.location.href = "/"
        }
    }
}