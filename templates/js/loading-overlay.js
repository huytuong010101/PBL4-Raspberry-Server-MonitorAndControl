class JsLoadingOverlay {
    static async show() {
        let loader = document.querySelector('.loader_bg');
        loader.style.display = 'block';
    }

    static async hide() {
        let loader = document.querySelector('.loader_bg');
        loader.style.display = 'none';
    }
}

window.JsLoadingOverlay = new JsLoadingOverlay();