HOST = "42.119.188.219"
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