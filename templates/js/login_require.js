// Get token
let save_token = localStorage.getItem("token")
if (!save_token){
    localStorage.setItem("msg", "You must login first")
    window.location.href = "login"
} 
// Set header to authen
axios.defaults.headers.common['Authorization'] = save_token
const token = save_token.split(" ")[1]
// Parse token
let current_user = JSON.parse(atob(token.split('.')[1]))
// Check if expire
if (current_user.exp * 1000 < new Date().valueOf()){
    localStorage.setItem("msg", "Loggin session is expire!")
    window.location.href = "login"
} 
// Set fullname
document.querySelector("#current-name").innerText = current_user.fullname
// Hide admin feature
const admin_feature = document.querySelectorAll(".admin-feature")
if (current_user.is_admin){
    admin_feature[0].style.display = "block"
    admin_feature[1].style.display = "block"
} else {
    admin_feature[0].remove()
    admin_feature[1].remove()
}
// Logout action
document.querySelector("#btn-logout").onclick = (event) => {
    current_user = null;
    localStorage.setItem("token", null)
    window.location.href = "login"
}

const load_profile = async () => {
    let error = null
    let profile = null
    try {
        const res = await axios.get(`/user/profile`)
        profile = res.data   
    } catch (err){
        if (err.response){
            error = err.response.data.detail
        } else {
            error = "Lỗi không xác định"
        }    
    } finally{
        if (error) toastr.error(error, "Load profile error")
        else {
            document.querySelector("#username").value = profile.username
            document.querySelector("#fullname").value = profile.fullname
            document.querySelector("#email").value = profile.email
            document.querySelector("#is-admin").checked = profile.is_admin
            document.querySelector("#username").value = profile.username
            document.querySelector("#created_at").innerText = profile.created_at
        }
    }
} 