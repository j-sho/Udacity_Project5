function PreviewImage() {
  setTimeout(function () {
        var srcLink;
        srcLink = document.getElementById("uploadImage").value;
        document.getElementById("uploadPreview").src = srcLink;
    }, 2000);
};
