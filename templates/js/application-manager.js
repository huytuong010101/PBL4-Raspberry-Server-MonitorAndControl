class AppService {
    static async get_all_app(){
        let error = null
        let apps = null
        try {
            const res = await axios.get(`/apps/`)
            apps = res.data
            
        } catch (err){
            if (err.response){
                error = err.response.data.detail
            } else {
                error = "Lỗi không xác định"
            }
            
        } finally {
            return [error, apps]
        }
        
    }

    static async remove_app(name){
        let error = null
        try {
            await axios.delete(`/apps/${name}`)   
        } catch (err){
            if (err.response){
                error = err.response.data.detail
            } else {
                error = "Lỗi không xác định"
            }   
        } finally {
            return error
        }
        
    }

    static async render_app(){
        let content = ""
        const [errors, apps] = await AppService.get_all_app()
        if (errors){
            alert(errors)
        } else {
            apps.forEach(item => {
                content += 
                `<div id="${item.name}" class="col-4 col-md-4 col-sm-12">
                    <div class="app-content">
                        <div class="row">
                            <div class="app-content-title">
                                <div class="col-2 col-md-3 col-sm-3 app-content-icon">
                                    <i class='bx bxl-discord-alt'></i>
                                </div>
                                <div class="col-5 col-md-5 col-sm-6 app-content-name">
                                    ${item.name}
                                </div>
                                <div class="col-2 col-md-1 col-sm-1"></div>
                                <div class="col-3 col-md-3 col-sm-2 app-content-info">
                                    
                                </div>
                            </div> 
                        </div>
                        <div class="row app-contain-btn">
                            <input class="app-btn" type="button" value="Modify" disabled>
                            <input class="app-btn" onClick="AppService.remove_event(this)" data-app="${item.name}" type="button" value="Uninstall">
                        </div>
                    </div>   
                </div>`
            })
            document.querySelector("#all-apps").innerHTML = content
        }
        
    }

    static async remove_event(event){
        JsLoadingOverlay.show()
        const error = await AppService.remove_app(event.dataset.app)
        JsLoadingOverlay.hide()
        if (error){
            toastr.error("Cannot uninstall this package", "Uninstall error")
        } else {
            document.querySelector("#" + event.dataset.app).remove()
            toastr.success(event.dataset.app + " was removed", "Uninstall success")
        }

    }
}