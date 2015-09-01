/**
 * Created by RaPoSpectre on 15/9/1.
 */
function fileSelected() {
    var file = document.getElementById('new_video').files[0];
    if (file) {
        var fileSize = 0;
        if (file.size > 1024 * 1024)
            fileSize = (Math.round(file.size * 100 / (1024 * 1024)) / 100).toString() + 'MB';
        else
            fileSize = (Math.round(file.size * 100 / 1024) / 100).toString() + 'KB';
        document.getElementById('fileName').innerHTML = file.name;
        document.getElementById('fileSize').innerHTML = fileSize;
    }
}
function uploadFile() {
    var fd = new FormData();
    fd.append("new_video", document.getElementById('new_video').files[0]);
    fd.append("csrfmiddlewaretoken", $("input[name='csrfmiddlewaretoken']").val());
    var xhr = new XMLHttpRequest();
    xhr.upload.addEventListener("progress", uploadProgress, false);
    xhr.addEventListener("load", uploadComplete, false);
    xhr.addEventListener("error", uploadFailed, false);
    xhr.addEventListener("abort", uploadCanceled, false);
    xhr.open("POST", "/admin/index/new_video");
    xhr.send(fd);
    document.getElementById('fileStatus').innerHTML = '本地上传中...'
}
function uploadProgress(evt) {
    if (evt.lengthComputable) {
        var percentComplete = Math.round(evt.loaded * 100 / evt.total);
        document.getElementById('progressNumber').innerHTML = percentComplete.toString() + '%';
        if (percentComplete == 100) {
            document.getElementById('fileStatus').innerHTML = '七牛云上传中...';
        }
    }
    else {
        document.getElementById('progressNumber').innerHTML = 'unable to compute';
    }
}
function uploadComplete(evt) {
    /* 服务器端返回响应时候触发event事件*/
    alert('上传成功！');
    document.getElementById('fileStatus').innerHTML = '上传成功！';
    location.reload();
}
function uploadFailed(evt) {
    alert("There was an error attempting to upload the file.");
}
function uploadCanceled(evt) {
    alert("The upload has been canceled by the user or the browser dropped the connection.");
}
