HOST = "42.113.41.118"
PORT = 8000

const showError = (detail, title) => {
    if ((typeof detail) == "string"){
        toastr.error(detail, title);
    } else {
        detail.forEach((item) => {
            toastr.error(item.loc.pop() + ": " + item.msg, title)
        })
    }
}