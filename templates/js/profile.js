document.querySelector("#btn-save-profile").onclick = async (event) => {
    JsLoadingOverlay.show()
    event.preventDefault()
    let error = null
    let res = null
    try {
        const data = {
            "username": current_user.sub,
            "fullname": document.querySelector("#fullname").value.trim(),
            "email": document.querySelector("#email").value.trim(),
            "is_admin": document.querySelector("#is-admin").checked
        }
        res = await axios.put(`/user/${current_user.sub}`, data)
    } catch (err){
        if (err.response){
            error = err.response.data.detail
        } else {
            error = "Lỗi không xác định"
        } 
    } finally {
        JsLoadingOverlay.hide()
        if (res.response && res.response.status >= 400){
            showError(res.response.data.detail, "Update error")
            return;
        }
        if (error) toastr.error(error, "Update error")
        else {
            toastr.success("Your profile was updated", "Update success")
            localStorage.setItem("msg", "Login again is require")
            window.location.href = "login"
        } 
    } 

}

document.querySelector("#btn-change-password").onclick = async (event) => {
    JsLoadingOverlay.show()
    event.preventDefault()
    let error = null
    let res = null;
    try {
        const data = {
            "old_password": document.querySelector("#old-pwd").value,
            "new_password": document.querySelector("#new-pwd").value,
            "re_password": document.querySelector("#re-pwd").value
        }
        res = await axios.put(`/user/${current_user.sub}/change-password`, data)
    } catch (err){
        if (err.response){
            error = err.response.data.detail
        } else {
            error = "Lỗi không xác định"
        } 
    } finally {
        JsLoadingOverlay.hide()
        if (res.response && res.response.status >= 400){
            showError(res.response.data.detail, "Update error")
            return;
        }
        if (error) toastr.error(error, "Update error")
        else {
            toastr.success("The password was changed", "Update success")
            localStorage.setItem("msg", "Login again is require")
            window.location.href = "login"
        } 
    } 

}